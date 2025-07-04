.EXPORT_ALL_VARIABLES:
.PHONY: build up stop down restart check-env adr help

PROJECT_NAME = "task_tracker"
ADR_DIR = docs/ADRs
ADR_TEMPLATE = $(ADR_DIR)/template.md
ADR_GIT_AUTHOR_FULL := $(shell git config user.name) <$(shell git config user.email)>
p := "all"  # profile to launch the required containers
s := "development"  # the stage for launching the necessary layers in dockerfile

export PYTHONPATH := $(shell pwd):$(PYTHONPATH)

# Check OS name
UNAME_S := $(shell uname -s)

# Setting the correct flag for sed, depending on the OS
ifeq ($(UNAME_S),Linux)
    SED_I := sed -i
endif
ifeq ($(UNAME_S),Darwin)
    SED_I := sed -i ''
endif

# Additional functions
adr_number = $(shell printf "%04d" $$(( \
    $(shell find $(ADR_DIR) -maxdepth 1 -name '[0-9]*_*.md' | wc -l) + 1 \
)))
current_date = $(shell date +'%Y-%m-%d')

default: help

help: Makefile
	@echo "\n Choose a command run in "$(PROJECT_NAME)" project:"
	@sed -n 's/^##//p' $< | column -t -s ':' | sed -e 's/^/ /'

check-env:
	@if [ ! -f ./.env ]; then \
		echo "Missing .env (.env) file"; \
		exit 1; \
	fi

## :
## <<< MAIN COMMANDS >>>:

## make build: build a new project
build:
	docker compose -p ${PROJECT_NAME} build

## make up <optional p=all or main> <optional s=production or development>: command to start project (default (profile) p=main)
up:
	BUILD_STAGE=${s} docker compose -p ${PROJECT_NAME} --profile ${p} up -d --remove-orphans

## make stop: command to stop a specific container
stop:
	docker compose stop ${PROJECT_NAME}

## make down: command to stop the container and clear the images
down:
	docker compose -p ${PROJECT_NAME} -v down --rmi all

## make restart: command to restart a specific container
restart:
	docker compose -p ${PROJECT_NAME} restart

## :
## <<< DEVS COMMANDS >>>:

## make adr name='Your Decision Title': command to create an ADR file to describe an architectural solution
adr:
ifndef name
	$(error "Please specify name: make adr name='Your Decision Title'")
endif
	@if [ -z "$(ADR_GIT_AUTHOR_FULL)" ]; then \
		echo "Warning: Git author not configured. Using 'Unknown'"; \
		ADR_GIT_AUTHOR_FULL="Unknown"; \
	fi
	@mkdir -p $(ADR_DIR)
	@filename="$(ADR_DIR)/$(adr_number)_$(shell echo $(name) | tr '[:upper:]' '[:lower:]' | tr ' ' '_').md"; \
	cp $(ADR_TEMPLATE) $$filename; \
	$(SED_I) \
		-e 's/{{N}}/$(adr_number)/g' \
		-e 's/{{TITLE}}/$(name)/g' \
		-e 's/{{YYYY-MM-DD}}/$(current_date)/g' \
		-e 's/{{AUTHOR}}/$(ADR_GIT_AUTHOR_FULL)/g' \
		$$filename; \
	echo "Created new ADR: $$filename"
