from typing import List, Dict, Any


def generate_suggestions(issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    suggestions = []
    for iss in issues:
        s = {
            'issue_id': iss.get('id'),
            'title': iss.get('title'),
            'suggestion': iss.get('suggestion')
        }
        # small actionable expansion
        if iss.get('title') == 'Long Function':
            s['example'] = 'Split the function into smaller functions each handling a single task.'
        if iss.get('title') == 'Deep Nesting':
            s['example'] = 'Use early return guards to reduce nesting.'
        suggestions.append(s)
    return suggestions
