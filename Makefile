# Makefile to kickoff terraform.
# ####################################################
#

NAME := "nitindas/flask-tutorial"
TAG := $$(git log --pretty=format:'' | wc -l)
# TAG  := $$(git log -1 --pretty=%h)
IMG := ${NAME}:${TAG}
LATEST := ${NAME}:latest

## Before we start test that we have the mandatory executables available
	EXECUTABLES = git docker
	K := $(foreach exec,$(EXECUTABLES),\
		$(if $(shell which $(exec)),some string,$(error "No $(exec) in PATH, consider apt-get install $(exec)")))

.PHONY: build

build:
	@echo "Docker build using Dockerfile"
	docker build --rm --force-rm --compress -t ${IMG} .
	docker tag ${IMG} ${LATEST}

push:
	@echo "Docker push to github"
	docker push ${NAME}

login:
	@echo "Docker login setup"
	docker login --username ${DOCKER_USER} --password ${DOCKER_PASS}

clean-all:
	@echo "Cleaning unsed container and images"
	docker container prune --force
	docker image prune --force