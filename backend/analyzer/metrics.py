import ast
from typing import Any, Dict, List


class FunctionVisitor(ast.NodeVisitor):
    def __init__(self, source_lines: List[str]):
        self.functions = []
        self.source_lines = source_lines

    def visit_FunctionDef(self, node: ast.FunctionDef):
        start = node.lineno - 1
        end = getattr(node, 'end_lineno', None)
        if end is None:
            end = node.lineno
        src = '\n'.join(self.source_lines[start:end])
        params = len(node.args.args)
        local_vars = set()
        for n in ast.walk(node):
            if isinstance(n, ast.Assign):
                for t in n.targets:
                    if isinstance(t, ast.Name):
                        local_vars.add(t.id)
        doc = ast.get_docstring(node)
        nesting = 0
        for n in ast.walk(node):
            if isinstance(n, (ast.If, ast.For, ast.While, ast.Try, ast.With)):
                nesting += 1
        self.functions.append({
            'name': node.name,
            'lineno': node.lineno,
            'lines': (end - start + 1),
            'parameters': params,
            'local_variables': len(local_vars),
            'nesting': nesting,
            'docstring': doc,
            'source': src
        })
        self.generic_visit(node)


class ClassVisitor(ast.NodeVisitor):
    def __init__(self, source_lines: List[str]):
        self.classes = []
        self.source_lines = source_lines

    def visit_ClassDef(self, node: ast.ClassDef):
        start = node.lineno - 1
        end = getattr(node, 'end_lineno', None)
        if end is None:
            end = node.lineno
        src = '\n'.join(self.source_lines[start:end])
        methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
        attrs = [n for n in node.body if isinstance(n, ast.Assign)]
        doc = ast.get_docstring(node)
        self.classes.append({
            'name': node.name,
            'lineno': node.lineno,
            'methods': len(methods),
            'attributes': len(attrs),
            'lines': (end - start + 1),
            'docstring': doc,
            'source': src
        })
        self.generic_visit(node)


def compute_metrics(source: str, tree: ast.AST) -> Dict[str, Any]:
    lines = source.splitlines()
    total = len(lines)
    blank = sum(1 for l in lines if not l.strip())
    comment = sum(1 for l in lines if l.strip().startswith('#'))
    logical = total - blank - comment
    imports = sum(1 for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom)))
    loops = sum(1 for n in ast.walk(tree) if isinstance(n, (ast.For, ast.While)))
    conditionals = sum(1 for n in ast.walk(tree) if isinstance(n, (ast.If,)))
    returns = sum(1 for n in ast.walk(tree) if isinstance(n, ast.Return))
    vars = sum(1 for n in ast.walk(tree) if isinstance(n, ast.Name))
    fv = FunctionVisitor(lines)
    fv.visit(tree)
    cv = ClassVisitor(lines)
    cv.visit(tree)
    metrics = {
        'total_lines': total,
        'logical_lines': logical,
        'blank_lines': blank,
        'comment_lines': comment,
        'imports': imports,
        'loops': loops,
        'conditionals': conditionals,
        'returns': returns,
        'variables': vars,
        'functions': fv.functions,
        'classes': cv.classes,
    }
    return metrics
