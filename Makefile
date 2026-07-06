.PHONY: install lint test up down train-churn train-clv

install:
	uv sync --all-extras
	uv run pre-commit install
	uv run dvc init --no-scm || true

lint:
	uv run ruff check .
	uv run ruff format .

test:
	uv run pytest

up:
	docker compose up --build -d

down:
	docker compose down

train-churn:
	uv run python services/churn_pipeline/src/churn_pipeline/pipelines/training_pipeline.py

train-clv:
	uv run python services/clv_pipeline/src/clv_pipeline/pipelines/training_pipeline.py
