.PHONY: dev test migrate seed down logs backend-shell db-shell

# Start all services
dev:
	docker-compose up --build -d
	@echo "✅ SIGAP is running!"
	@echo "   Frontend: http://localhost:5173"
	@echo "   Backend:  http://localhost:8000"
	@echo "   API Docs: http://localhost:8000/docs"

# Stop all services
down:
	docker-compose down

# Run database migrations
migrate:
	docker-compose exec backend alembic upgrade head

# Seed database with sample data
seed:
	docker-compose exec backend python -m scripts.seed_kelurahan
	docker-compose exec backend python -m scripts.seed_dummy_indicators
	docker-compose exec backend python -m scripts.run_initial_uss

# Run all tests
test:
	docker-compose exec backend pytest tests/ -v --tb=short
	cd frontend && npm test -- --run

# View logs
logs:
	docker-compose logs -f

# Backend shell
backend-shell:
	docker-compose exec backend bash

# Database shell
db-shell:
	docker-compose exec postgres psql -U sigap -d sigap_db
