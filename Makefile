up:
	@docker-compose -f local.yml up -d
	@docker images -q -f dangling=true | xargs docker rmi -f

up-build:
	@docker-compose -f local.yml up -d --build
	@docker images -q -f dangling=true | xargs docker rmi -f

down:
	@docker-compose -f local.yml down

shell:
	@docker-compose -f local.yml exec django python manage.py shell_plus

# If the first argument is "test"...
ifeq (test,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "test"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif
test:
	@docker-compose -f local.yml run -e PYTHONDONTWRITEBYTECODE=1 --rm django pytest -p no:cacheprovider $(RUN_ARGS) -s -vv --create-db

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

######
# CI/CD
######


AWS_CLI_PROFILE:=
# default value is empty in order to use the command from bitbucket pipeline
# to activate preset profile use AWS_CLI_PROFILE="--profile test"

services = market-app market-celeryworker market-celerybeat

define upload_config_common
	envsubst '$$SERVER_NAME $$ENV_CIDR' < $(1) > default-$(2).conf
	aws s3 cp . ${AWS_S3_CONFIGS}/$(2)/$(3)/$(4) --recursive --exclude "*" --include "default-$(2).conf"
endef

define build_common
	docker build -t ${DOCKER_REGISTRY}/kuailian/$(2):$(1) -f ./etc/Dockerfile --build-arg ENV=production .
	docker save -o tmp-$(1)-image.docker ${DOCKER_REGISTRY}/kuailian/$(2):$(1)
endef

define push_common
	docker load -i tmp-$(1)-image.docker
	docker tag ${DOCKER_REGISTRY}/kuailian/$(2):$(1) ${DOCKER_REGISTRY}/kuailian/$(2):$(1)-${BITBUCKET_COMMIT}
	docker push ${DOCKER_REGISTRY}/kuailian/$(2):$(1)
	docker push ${DOCKER_REGISTRY}/kuailian/$(2):$(1)-${BITBUCKET_COMMIT}
endef

define deploy_common
    $(foreach i,$(services),aws ecs update-service --cluster kuailian-$(1) --service kuailian-$(i)-$(1) --force-new-deployment;)
endef

upload-config-nginx:
	$(call upload_config_common,etc/nginx/conf.d/default.conf,${ENV_NAME},apps,nginx)

build-app:
	$(call build_common,${ENV_NAME},${ECR_NAME})

push-app:
	$(call push_common,${ENV_NAME},${ECR_NAME})

deploy-app:
	$(call deploy_common,${ENV_NAME})

slack-notification:
	curl -s -X POST https://hooks.slack.com/services/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 \
	-H "content-type:application/json" \
    -d '{"text":"[market] [${BITBUCKET_BRANCH}] ${MESSAGE}"}'

generate-mnemonic:
	pip3 install mnemonic
	python tools/mnemonic.py
