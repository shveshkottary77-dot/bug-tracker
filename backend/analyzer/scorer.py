from typing import Dict, Any, List
from radon.metrics import mi_visit


def score_analysis(metrics: Dict[str, Any], functions: List[Dict[str, Any]], classes: List[Dict[str, Any]], issues: List[Dict[str, Any]], complexities: Dict[str, Any]) -> Dict[str, Any]:
    # Maintainability (radon MI)
    try:
        mi = mi_visit('\n'.join([''] + []))
    except Exception:
        mi = 50
    # if possible, get mi from metrics - fallback
    # compute component scores
    complexity_score = 100
    if functions:
        avg_cc = 0
        for f in functions:
            avg_cc += f.get('cyclomatic_complexity', 0)
        avg_cc = avg_cc / max(1, len(functions))
        # scale: lower complexity -> higher score
        complexity_score = max(0, int(100 - (avg_cc * 4)))
    maintainability_score = int(mi)
    doc_count = sum(1 for f in functions if f.get('docstring'))
    documentation_score = int(100 * (doc_count / max(1, len(functions))))
    naming_penalty = 0
    for iss in issues:
        if iss.get('category') == 'Naming':
            naming_penalty += 5
    naming_score = max(0, 100 - naming_penalty)
    duplication_penalty = sum(1 for iss in issues if iss.get('category') == 'Duplication') * 5
    duplication_score = max(0, 100 - duplication_penalty)
    code_smell_penalty = 0
    for iss in issues:
        sev = iss.get('severity')
        if sev == 'CRITICAL':
            code_smell_penalty += 20
        elif sev == 'HIGH':
            code_smell_penalty += 10
        elif sev == 'MEDIUM':
            code_smell_penalty += 5
        else:
            code_smell_penalty += 1
    code_smell_score = max(0, 100 - code_smell_penalty)
    # Weighted overall
    overall = int((complexity_score * 0.25) + (maintainability_score * 0.2) + (code_smell_score * 0.2) + (documentation_score * 0.1) + (naming_score * 0.1) + (duplication_score * 0.1))
    # quality_level
    if overall >= 90:
        q = 'EXCELLENT'
    elif overall >= 75:
        q = 'GOOD'
    elif overall >= 60:
        q = 'MODERATE'
    elif overall >= 40:
        q = 'POOR'
    else:
        q = 'CRITICAL'
    return {
        'overall_score': overall,
        'component_scores': {
            'complexity_score': complexity_score,
            'maintainability_score': maintainability_score,
            'documentation_score': documentation_score,
            'naming_score': naming_score,
            'duplication_score': duplication_score,
            'code_smell_score': code_smell_score
        },
        'quality_level': q
    }
