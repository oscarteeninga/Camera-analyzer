FROM python:3.7-alpine

LABEL maintainer="Michal Orzechowski <morzech@agh.edu.pl>"

# Metadata schema args
ARG SCHEMA_NAME
ARG SCHEMA_DESCRIPTION
ARG SCHEMA_URL
ARG SCEHMA_VENDOR
ARG SCHEMA_VSC_URL
ARG SCHEMA_VCS_REF
ARG SCHEMA_BUILD_DATE
ARG SCHEMA_BUILD_VERSION
ARG SCHEMA_CMD

# Metadata
LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.name=$SCHEMA_NAME
LABEL org.label-schema.description=$SCHEMA_DESCRIPTION
LABEL org.label-schema.url=$SCHEMA_VSC_URL
LABEL org.label-schema.vendor=$SCEHMA_VENDOR
LABEL org.label-schema.vcs-url=$SCHEMA_VSC_URL
LABEL org.label-schema.vcs-ref=$SCHEMA_VCS_REF
LABEL org.label-schema.build-date=$SCHEMA_BUILD_DATE
LABEL org.label-schema.version=$SCHEMA_BUILD_VERSION
LABEL org.label-schema.docker.cmd=$SCHEMA_CMD

WORKDIR /code

RUN apk add --no-cache gcc musl-dev linux-headers

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0

COPY . .

CMD ["flask", "run"]