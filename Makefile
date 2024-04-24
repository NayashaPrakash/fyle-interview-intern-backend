.PHONY: server test

server:
	@echo "Running server..."
	@bash run.sh

test:
	@echo "Running tests..."
	@pytest -vvv -s tests/
	@pytest --cov tests/

db:
	@echo "Setting up database..."
	@export FLASK_APP=core/server.py
	@rm -f core/store.sqlite3
	@flask db upgrade -d core/migrations/
