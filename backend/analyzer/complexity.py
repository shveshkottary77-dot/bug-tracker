from radon.complexity import cc_visit
from radon.complexity import cc_rank
from typing import Dict, Any


def compute_complexities(source: str) -> Dict[str, Dict[str, Any]]:
    results = cc_visit(source)
    out = {}
    for item in results:
        # item.name might be like 'function_name'
        out[item.name] = {
            'complexity': item.complexity,
            'lineno': item.lineno,
            'rank': cc_rank(item.complexity)
        }
    return out
