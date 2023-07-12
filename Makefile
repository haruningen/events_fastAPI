.DEFAULT_GOAL := help
COMPOSE_RUN_APP := docker-compose run --rm app
pyproject = ../pyproject.toml

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build:  ## Build application
	docker-compose  build

cli:  ## Make CLI app command. Using: make cli args='some args'
	$(COMPOSE_RUN_APP) python manage.py $(args)

generate_migrations:  ## Generate new migrations. Using: make generate_migrations NAME='migration_name'
	$(COMPOSE_RUN_APP) alembic revision --autogenerate -m '$(NAME)'

migrate:  ## Apply migrations
	$(COMPOSE_RUN_APP) alembic upgrade head

downgrade_migration:  ## Downgrade latest migration
	$(COMPOSE_RUN_APP) alembic downgrade -1

start:  ## Start application
	docker-compose up -d

mypy:  ## Run mypy
	$(COMPOSE_RUN_APP) mypy .