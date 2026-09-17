import ast
from typing import List, Dict, Any
from difflib import SequenceMatcher


BAD_NAMES = set(["x","y","z","a","b","tmp","foo","bar"])


def _count_nesting(node: ast.AST, depth=0) -> int:
    max_depth = depth
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.If, ast.For, ast.While, ast.Try, ast.With)):
            d = _count_nesting(child, depth + 1)
            if d > max_depth:
                max_depth = d
        else:
            d = _count_nesting(child, depth)
            if d > max_depth:
                max_depth = d
    return max_depth


def detect_code_smells(source: str, tree: ast.AST, functions: List[Dict[str, Any]], classes: List[Dict[str, Any]], metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
    issues: List[Dict[str, Any]] = []
    lines = source.splitlines()
    # Long functions
    for f in functions:
        if f['lines'] > 50:
            issues.append({
                'id': f"LONG_FUNC_{f['name']}",
                'category': 'Complexity',
                'severity': 'HIGH',
                'title': 'Long Function',
                'description': f"Function {f['name']} contains {f['lines']} lines.",
                'line': f.get('lineno', 0),
                'function': f['name'],
                'suggestion': 'Break this function into smaller functions with single responsibilities.'
            })
        if f.get('parameters', 0) > 5:
            issues.append({
                'id': f"TOO_MANY_PARAMS_{f['name']}",
                'category': 'Maintainability',
                'severity': 'MEDIUM',
                'title': 'Too Many Parameters',
                'description': f"Function {f['name']} has {f.get('parameters')} parameters.",
                'line': f.get('lineno', 0),
                'function': f['name'],
                'suggestion': 'Refactor to use objects or smaller helper functions.'
            })
    # Nesting
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            depth = _count_nesting(node, 0)
            if depth > 3:
                issues.append({
                    'id': f"DEEP_NEST_{node.name}",
                    'category': 'Complexity',
                    'severity': 'MEDIUM' if depth<=5 else 'HIGH',
                    'title': 'Deep Nesting',
                    'description': f"Function {node.name} contains nesting depth of {depth}.",
                    'line': node.lineno,
                    'function': node.name,
                    'suggestion': 'Use early returns, helper functions, or guard clauses.'
                })
    # Missing docstrings
    for f in functions:
        if not f.get('docstring') and not f['name'].startswith('_'):
            issues.append({
                'id': f"MISSING_DOC_{f['name']}",
                'category': 'Documentation',
                'severity': 'LOW',
                'title': 'Missing Documentation',
                'description': f"Function {f['name']} has no docstring.",
                'line': f.get('lineno', 0),
                'function': f['name'],
                'suggestion': 'Document what the function does, its parameters, and return value.'
            })
    for c in classes:
        if not c.get('docstring'):
            issues.append({
                'id': f"MISSING_DOC_CLASS_{c['name']}",
                'category': 'Documentation',
                'severity': 'LOW',
                'title': 'Missing Class Documentation',
                'description': f"Class {c['name']} has no docstring.",
                'line': c.get('lineno', 0),
                'function': c['name'],
                'suggestion': 'Add a class docstring explaining its purpose.'
            })
    # Long lines
    for i, line in enumerate(lines, start=1):
        if len(line) > 88:
            issues.append({
                'id': f"LONG_LINE_{i}",
                'category': 'Style',
                'severity': 'LOW',
                'title': 'Long Line',
                'description': f"Line {i} exceeds recommended length ({len(line)} > 88).",
                'line': i,
                'function': None,
                'suggestion': 'Wrap long lines or refactor into smaller expressions.'
            })
    # Naming
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            if node.id in BAD_NAMES:
                issues.append({
                    'id': f"BAD_NAME_{node.id}_{node.lineno if hasattr(node,'lineno') else 0}",
                    'category': 'Naming',
                    'severity': 'LOW',
                    'title': 'Poor Identifier Name',
                    'description': f"Identifier {node.id} used; consider more descriptive names.",
                    'line': getattr(node, 'lineno', 0),
                    'function': None,
                    'suggestion': 'Use descriptive variable and parameter names.'
                })
    # Unused imports (conservative): if import name never appears as attribute or name
    imports = []
    used_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.Name):
            used_names.add(node.id)
        elif isinstance(node, ast.Attribute):
            used_names.add(node.attr)
    for imp in set(imports):
        if imp not in used_names:
            issues.append({
                'id': f"UNUSED_IMPORT_{imp}",
                'category': 'Style',
                'severity': 'LOW',
                'title': 'Unused Import',
                'description': f"{imp} appears to be unused.",
                'line': 0,
                'function': None,
                'suggestion': 'Remove unused imports.'
            })
    # Duplicate detection (functions similarity)
    funcs = [f for f in functions]
    for i in range(len(funcs)):
        for j in range(i+1, len(funcs)):
            a = funcs[i].get('source','')
            b = funcs[j].get('source','')
            if not a or not b:
                continue
            s = SequenceMatcher(None, a, b).ratio()
            if s > 0.85:
                issues.append({
                    'id': f"DUPLICATE_{funcs[i]['name']}_{funcs[j]['name']}",
                    'category': 'Duplication',
                    'severity': 'MEDIUM',
                    'title': 'Possible Duplicate Code',
                    'description': f"Functions {funcs[i]['name']} and {funcs[j]['name']} similarity: {int(s*100)}%.",
                    'line': funcs[i].get('lineno',0),
                    'function': funcs[i]['name'],
                    'suggestion': 'Consider extracting common logic into a shared helper.'
                })
    # Unused variables: conservative: assigned but never used
    assigned = {}
    used = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assigned[target.id] = getattr(target, 'lineno', 0)
        elif isinstance(node, ast.Name):
            used.add(node.id)
    for name, ln in assigned.items():
        if name not in used:
            # skip single-letter common loop vars like i, j
            if len(name) <= 1:
                continue
            issues.append({
                'id': f"UNUSED_VAR_{name}",
                'category': 'Style',
                'severity': 'LOW',
                'title': 'Unused Variable',
                'description': f"Variable {name} assigned but never used.",
                'line': ln,
                'function': None,
                'suggestion': 'Remove or use the assigned variable.'
            })
    return issues
