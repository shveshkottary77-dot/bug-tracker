import ast
from typing import Any, Dict, List, Tuple
from .metrics import compute_metrics
from .complexity import compute_complexities
from .code_smells import detect_code_smells
from .scorer import score_analysis
from .suggestions import generate_suggestions


def analyze_source(source: str, filename: str = 'snippet.py') -> Dict[str, Any]:
    try:
        tree = ast.parse(source, filename=filename)
    except SyntaxError as e:
        raise
    metrics = compute_metrics(source, tree)
    functions = metrics.pop('functions', [])
    classes = metrics.pop('classes', [])
    complexities = compute_complexities(source)
    # attach complexity to function entries
    for f in functions:
        name = f['name']
        if name in complexities:
            f['cyclomatic_complexity'] = complexities[name]['complexity']
            f['cc_rank'] = complexities[name]['rank']
        else:
            f['cyclomatic_complexity'] = 0
            f['cc_rank'] = 'A'
    issues = detect_code_smells(source, tree, functions, classes, metrics)
    suggestions = generate_suggestions(issues)
    scored = score_analysis(metrics, functions, classes, issues, complexities)
    result = {
        'filename': filename,
        'metrics': metrics,
        'functions': functions,
        'classes': classes,
        'complexities': complexities,
        'issues': issues,
        'suggestions': suggestions,
    }
    result.update(scored)
    return result
