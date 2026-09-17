"""
Placeholder for ML feature extractor. Produces feature vectors for future models.
"""
from typing import Dict

def extract_features(analysis: Dict) -> Dict:
    metrics = analysis.get('metrics', {})
    features = {
        'loc': metrics.get('total_lines', 0),
        'functions': len(metrics.get('functions', [])),
        'classes': len(metrics.get('classes', [])),
        'comment_ratio': (metrics.get('comment_lines',0) / max(1, metrics.get('total_lines',1))),
        'documentation_ratio': (sum(1 for f in metrics.get('functions',[]) if f.get('docstring')) / max(1, len(metrics.get('functions',[])))),
    }
    return features
