lint:
	@echo "Running Ruff linter and formatter"
	@uv run ruff check .
	@uv run ruff format --check .

format-code:
	@uv run ruff format .
	@uv run ruff check --select I --fix .