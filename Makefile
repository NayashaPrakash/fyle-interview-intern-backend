.PHONY: server test

server:
	@echo "Running server..."
	@bash run.sh

test:
	@echo "Running tests..."
	@pytest -vvv -s tests/
	@pytest --cov tests/
