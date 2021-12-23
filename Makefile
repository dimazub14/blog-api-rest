up:
	@docker-compose -f local.yml up -d
	@docker images -q -f dangling=true | xargs docker rmi -f

up-build:
	@docker-compose -f local.yml up -d --build
	@docker images -q -f dangling=true | xargs docker rmi -f

down:
	@docker-compose -f local.yml down

shell:
	@docker-compose -f local.yml exec django python manage.py shell

# If the first argument is "test"...
ifeq (test,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "test"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif
test:
	@docker-compose -f local.yml run -e PYTHONDONTWRITEBYTECODE=1 --rm django python3 manage.py test $(RUN_ARGS) --settings=config.settings.test

ps:
	@docker-compose -f local.yml ps

sh:
	@docker-compose -f local.yml exec django sh

bash:
	@docker-compose -f local.yml exec django bash

validate:
	@docker-compose -f local.yml run -e PRE_COMMIT_HOME=/tmp --rm django pre-commit run --all-files -c .pre-commit-config.yaml

# If the first argument is "logs"...
ifeq (logs,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "logs"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif
logs:
	@docker-compose -f local.yml logs -f $(RUN_ARGS)

requirements:
	@docker-compose -f local.yml exec django pip3 install -r requirements/base.txt

migrate:
	@docker-compose -f local.yml exec django python manage.py migrate

makemigrations:
	@docker-compose -f local.yml exec django python manage.py makemigrations
