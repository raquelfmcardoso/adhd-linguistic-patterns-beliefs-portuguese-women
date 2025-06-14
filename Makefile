lint:
	@echo "Running Ruff linter and formatter"
	@uv run ruff check . --exclude notebooks/other_datasets
	@uv run ruff format --check . --exclude notebooks/other_datasets

format-code:
	@uv run ruff format . --exclude notebooks/other_datasets
	@uv run ruff check --select I --fix . --exclude notebooks/other_datasets