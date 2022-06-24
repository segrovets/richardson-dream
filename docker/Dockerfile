FROM ubuntu:20.04

# Document the docker image
LABEL maintainer="segrovets.i.aa@m.titech.ac.jp"
LABEL version="0.1"
LABEL description="This is a custom Docker Image for richardson-dream. Please dont build image on lab proxy network"

# Disable prompt durring installation (ENV DEB.. = "noninteractive" may also work)
ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /workspace

# update Ubuntu Software Repo Docker image gets bloated if you initialise with many commands, better to bundle all setup into one.
# remove cache to reduce size of custom image
# https://stackoverflow.com/questions/55313610/importerror-libgl-so-1-cannot-open-shared-object-fle-no-such-file-or-directo
# https://github.com/SumoLogic/sumologictoolbox/issues/11 for source of reason for inclusion of lib below libgl1
# added packages for generating firmware files
# https://microbit-micropython.readthedocs.io/en/v1.0.1/devguide/installation.html#microbit-linux

RUN apt update && \
    apt install -yV \
        python3.8 \
        python3-pip \
        libgl1 \
        libqt5dbus5 \
        libqt5widgets5 \
        libqt5network5 \
        libqt5gui5 \
        libqt5core5a \
        libxcb-xinerama0 \     
        cmake \
        ninja-build \
        gcc-arm-none-eabi \
        srecord \
        libssl-dev \
        xauth  && \
    apt-get autoremove -y && \ 
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY Pipfile Pipfile.lock ${HOME}/

RUN pip install -U pip pipenv && \
    pipenv install --system --dev --ignore-pipfile