FROM ubuntu:22.04

WORKDIR /

RUN apt-get update \
 && apt-get install -yq --no-install-recommends \
    wget \
    bzip2 \
    ca-certificates \
    sudo \
    locales \
    fonts-liberation \
    run-one \
    openssh-client \
    sshpass \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

# Configure environment
ENV SHELL=/bin/bash \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8
ENV PATH=$CONDA_DIR/bin:$PATH 

ENV TZ=Pacific/Auckland
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

USER root

RUN apt-get update && apt-get install -yq --no-install-recommends build-essential git libpq-dev python3-dev python3-pip nano && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install pandas numpy flask flask_cors psycopg2 timeout_decorator
COPY start /home/
COPY Monitor_FitbitFlask /home/
COPY fitbit.py /home/

# set display port to avoid crash
CMD [ "/home/start" ]
