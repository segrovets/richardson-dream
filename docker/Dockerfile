FROM ubuntu:20.04

# Document the docker image
LABEL maintainer="segrovets.i.aa@m.titech.ac.jp"
LABEL version="0.1"
LABEL description="This is a custom Docker Image for richardson-dream. Please dont build image on lab proxy network"

# Disable prompt durring installation (ENV DEB.. = "noninteractive" may also work)
ARG DEBIAN_FRONTEND=noninteractive

# update Ubuntu Software Repo Docker image gets bloated if you initialise with many commands, better to bundle all setup into one.
# remove cache to reduce size of custom image
RUN apt update && \
    apt install -yV firefox \
        python3.8 \
        python3-pip \
        xauth  && \
    apt-get autoremove -y && \ 
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* 
