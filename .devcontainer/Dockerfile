FROM mcr.microsoft.com/vscode/devcontainers/base:0-bullseye

ARG DRAWIO_VERSION="19.0.3"

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
     && apt-get -y install --no-install-recommends python3 python3-pip python3-setuptools 
RUN pip3 install wheel mkdocs mkdocs-material BeautifulSoup4
