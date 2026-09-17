from analyzer.metrics import compute_metrics
from analyzer.code_smells import detect_code_smells
import ast


def test_compute_metrics_counts():
    src = 'import os\n\n# comment\n\ndef f(a):\n    x=1\n    return x\n'
    tree = ast.parse(src)
    metrics = compute_metrics(src, tree)
    assert metrics['total_lines'] == 7
    assert metrics['imports'] == 1
    assert len(metrics['functions']) == 1


def test_detect_missing_docstring():
    src = 'def f():\n    return 1\n'
    tree = ast.parse(src)
    metrics = compute_metrics(src, tree)
    issues = detect_code_smells(src, tree, metrics['functions'], metrics['classes'], metrics)
    assert any(i['title']=='Missing Documentation' for i in issues)
 