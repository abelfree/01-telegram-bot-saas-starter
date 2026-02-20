.PHONY: run test lint

run:
	uvicorn app.main:app --reload --app-dir src

test:
	pytest -q

lint:
	ruff check src tests