# CodeSense

Intelligent Python Code Quality Analyzer

[![Accessibility Audit](https://github.com/codesense-bot/CodeSense/actions/workflows/accessibility-audit.yml/badge.svg)](https://github.com/codesense-bot/CodeSense/actions/workflows/accessibility-audit.yml)

This repository contains a Flask backend that performs local static analysis of Python code using the AST and Radon libraries. It is designed to be extended with a React + TypeScript frontend (not fully scaffolded here yet).

Key features implemented in this initial version:

- AST parsing and metrics extraction
- Cyclomatic complexity via Radon
- Code smell detection: long functions, too many parameters, deep nesting, missing docstrings, long lines, naming issues, unused imports/variables, duplicate functions
- Scoring engine that computes component scores and an overall quality score
- REST API endpoints: `POST /api/analyze`, `GET /api/history`, `GET /api/history/<id>`, `DELETE /api/history/<id>`, `GET|PUT /api/settings`
- SQLite persistence of analyses
- Sample code files: `sample_code/good_code.py`, `moderate_code.py`, `poor_code.py`

Security: the analyzer uses `ast.parse()` only and does not execute uploaded code.

Installation (backend):

```bash
cd backend
python -m venv venv
venv\Scripts\activate    # Windows
pip install -r requirements.txt
python app.py
```

API: POST `/api/analyze` with JSON `{ "filename": "app.py", "code": "..." }`.

Frontend: a professional React + TypeScript + Tailwind frontend is planned next. The backend is ready to be connected.

Future work:

- Implement full React frontend with Monaco Editor, Tailwind, charts
- Add unit tests and CI
- Improve analyzer rules and ML feature extractor

