# FastAPI Poetry Example

How to run the local server:
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

How to run tests:
```bash
pytest tests
```

How to run tests with coverage:
```bash
pytest tests --cov=api
```

How to generate requirements document:
```bash
poetry export -f requirements.txt --output requirements.txt
```

How to generate dev requirements document:
```bash
poetry export -f requirements.txt --output requirements-dev.txt --with dev
```