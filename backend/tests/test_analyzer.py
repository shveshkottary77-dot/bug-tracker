import pytest
from analyzer.ast_analyzer import analyze_source


def test_analyze_good_code():
    with open('sample_code/good_code.py','r',encoding='utf-8') as f:
        src = f.read()
    res = analyze_source(src, 'good_code.py')
    assert 'metrics' in res
    assert res['overall_score'] >= 0


def test_syntax_error():
    src = 'def bad(:\n    pass'
    with pytest.raises(SyntaxError):
        analyze_source(src, 'bad.py')


def test_long_function_detection():
    src = '\n'.join(['def lf():'] + ['    x=0']*60 + ['    return x'])
    res = analyze_source(src, 'lf.py')
    issues = res.get('issues', [])
    assert any(i['title']=='Long Function' for i in issues)


def test_duplicate_detection():
    src = open('sample_code/poor_code.py','r',encoding='utf-8').read()
    res = analyze_source(src, 'poor_code.py')
    issues = res.get('issues', [])
    assert any(i['category']=='Duplication' for i in issues)
