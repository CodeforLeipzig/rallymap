#############################
## Front Matter            ##
#############################

.PHONY: help

.DEFAULT_GOAL := help

include .env
export

#############################
## Targets                 ##
#############################

## Build images for running scripts
build:
	docker build --tag "rallymap-python" src/main/docker/python

## load rallies
load:
	@docker run -it --rm --name rallymap-load-rallies -e "ORS_API_KEY=${ORS_API_KEY}" -v "${PWD}":/usr/src/app -w /usr/src/app rallymap-python python src/main/python/load_rallies.py

#############################
## Help Target             ##
#############################

## Show this help
help:
	@printf "Available targets:\n\n"
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  %-20s %s\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)
