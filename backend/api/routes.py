from flask import Blueprint, jsonify
from .analysis_routes import analysis_bp

api_bp = Blueprint('api', __name__)
api_bp.register_blueprint(analysis_bp, url_prefix='/')

@api_bp.route('/')
def index():
    return jsonify({"message": "CodeSense API"})
