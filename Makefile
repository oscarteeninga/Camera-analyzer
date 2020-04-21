# Git repo metadata
TAG = $(shell git describe --tags --always)
PREFIX = $(shell git config --get remote.origin.url | tr ':.' '/'  | rev | cut -d '/' -f 3 | rev)
REPO_NAME = $(shell git config --get remote.origin.url | tr ':.' '/'  | rev | cut -d '/' -f 2 | rev)

# Image metadata

# Name of the repository
SCHEMA_NAME = $(PREFIX)/$(REPO_NAME)
SCHEMA_DESCRIPTION = My image!
SCHEMA_URL = http://example.com

# Vendor set to github user name
SCEHMA_VENDOR = $(PREFIX)

SCHEMA_VSC_URL = https://github.com/$(PREFIX)/$(REPO_NAME)

# git commit shirt sha
SCHEMA_VCS_REF = $(shell git rev-parse --short HEAD)

SCHEMA_BUILD_DATE = $(shell date -u +'%Y-%m-%dT%H:%M:%SZ')

SCHEMA_BUILD_VERSION = 
SCHEMA_CMD = 

all: push

image:
  # TODO: this build command is incomplete, add last flag of this command that tags image as latest upon building it
	docker build \
		--build-arg SCHEMA_NAME="$(SCHEMA_NAME)" \
		--build-arg SCHEMA_DESCRIPTION="$(SCHEMA_DESCRIPTION)" \
		--build-arg SCHEMA_URL="$(SCHEMA_URL)" \
		--build-arg SCEHMA_VENDOR="$(SCEHMA_VENDOR)" \
		--build-arg SCHEMA_VSC_URL="$(SCHEMA_VSC_URL)" \
		--build-arg SCHEMA_VCS_REF="$(SCHEMA_VCS_REF)" \
		--build-arg SCHEMA_BUILD_DATE="$(SCHEMA_BUILD_DATE)" \
		--build-arg SCHEMA_BUILD_VERSION="$(SCHEMA_BUILD_VERSION)" \
		--build-arg SCHEMA_CMD="$(SCHEMA_CMD)" \
		--tag oscarteeninga/$(REPO_NAME):latest .\
	
  # TODO: last part of this command that tags just built image with a specyfic tag
	docker build \
		--build-arg SCHEMA_NAME="$(SCHEMA_NAME)" \
		--build-arg SCHEMA_DESCRIPTION="$(SCHEMA_DESCRIPTION)" \
		--build-arg SCHEMA_URL="$(SCHEMA_URL)" \
		--build-arg SCEHMA_VENDOR="$(SCEHMA_VENDOR)" \
		--build-arg SCHEMA_VSC_URL="$(SCHEMA_VSC_URL)" \
		--build-arg SCHEMA_VCS_REF="$(SCHEMA_VCS_REF)" \
		--build-arg SCHEMA_BUILD_DATE="$(SCHEMA_BUILD_DATE)" \
		--build-arg SCHEMA_BUILD_VERSION="$(SCHEMA_BUILD_VERSION)" \
		--build-arg SCHEMA_CMD="$(SCHEMA_CMD)" \
		--tag oscarteeninga/$(REPO_NAME):teeninga .\

	docker tag 

push:
	# TODO: two commands, first pushes the latest image, second pushes the image tagged with specyfic tag
	docker login
	docker push oscarteeninga/$(REPO_NAME):latest
	docker push oscarteeninga/$(REPO_NAME):teeninga

clean:

.PHONY: clean image push all