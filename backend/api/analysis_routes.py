import json
import datetime
from flask import Blueprint, request, jsonify
from analyzer.ast_analyzer import analyze_source
from models.database import init_db, get_session
from models.analysis import Analysis

analysis_bp = Blueprint('analysis', __name__)

# initialize DB
init_db()

MAX_FILE_SIZE = 200 * 1024  # 200 KB

@analysis_bp.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json() or {}
    filename = data.get('filename', 'snippet.py')
    code = data.get('code', '')
    if not code:
        return jsonify({"success": False, "error": "Empty code"}), 400
    if len(code.encode('utf-8')) > MAX_FILE_SIZE:
        return jsonify({"success": False, "error": "File too large"}), 413
    try:
        analysis = analyze_source(code, filename)
    except SyntaxError as e:
        return jsonify({"success": False, "error": "Syntax Error", "detail": str(e)}), 400
    # save to DB
    session = get_session()
    a = Analysis(
        filename=filename,
        timestamp=datetime.datetime.utcnow(),
        score=analysis.get('overall_score', 0),
        quality_level=analysis.get('quality_level', 'UNKNOWN'),
        lines=analysis.get('metrics', {}).get('total_lines', 0),
        functions=len(analysis.get('functions', [])),
        classes=len(analysis.get('classes', [])),
        issue_count=len(analysis.get('issues', [])),
        analysis_summary=json.dumps(analysis)
    )
    session.add(a)
    session.commit()
    result = {"success": True, "analysis": analysis}
    return jsonify(result)

@analysis_bp.route('/history', methods=['GET'])
def history():
    session = get_session()
    items = session.query(Analysis).order_by(Analysis.timestamp.desc()).limit(200).all()
    out = []
    for it in items:
        out.append({
            "id": it.id,
            "filename": it.filename,
            "timestamp": it.timestamp.isoformat(),
            "score": it.score,
            "quality_level": it.quality_level,
            "lines": it.lines,
            "functions": it.functions,
            "classes": it.classes,
            "issue_count": it.issue_count,
        })
    return jsonify({"success": True, "history": out})

@analysis_bp.route('/history/<int:item_id>', methods=['GET'])
def get_history(item_id):
    session = get_session()
    it = session.query(Analysis).get(item_id)
    if not it:
        return jsonify({"success": False, "error": "Not found"}), 404
    return jsonify({"success": True, "analysis": json.loads(it.analysis_summary)})

@analysis_bp.route('/history/<int:item_id>', methods=['DELETE'])
def delete_history(item_id):
    session = get_session()
    it = session.query(Analysis).get(item_id)
    if not it:
        return jsonify({"success": False, "error": "Not found"}), 404
    session.delete(it)
    session.commit()
    return jsonify({"success": True})

@analysis_bp.route('/settings', methods=['GET', 'PUT'])
def settings():
    # Simple settings stored in a JSON file for now
    import os
    path = os.path.join(os.path.dirname(__file__), '..', 'settings.json')
    path = os.path.abspath(path)
    if request.method == 'GET':
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return jsonify({"success": True, "settings": json.load(f)})
        else:
            default = {
                "max_function_length": 50,
                "max_parameters": 5,
                "max_nesting": 3,
                "max_line_length": 88,
                "high_complexity": 10,
                "duplicate_similarity": 0.85
            }
            return jsonify({"success": True, "settings": default})
    else:
        payload = request.get_json() or {}
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(payload, f, indent=2)
        return jsonify({"success": True, "settings": payload})
