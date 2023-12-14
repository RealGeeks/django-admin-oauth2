FROM python:3.10-slim-bullseye

RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  curl \
  git \
  # requirements to install Python with asdf: https://github.com/pyenv/pyenv/wiki#suggested-build-environment
  build-essential \
  libssl-dev \
  zlib1g-dev \
  libbz2-dev \
  libreadline-dev \
  libsqlite3-dev \
  libncursesw5-dev \
  xz-utils \
  tk-dev \
  libxml2-dev \
  libxmlsec1-dev \
  libffi-dev \
  liblzma-dev\
  && rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 https://github.com/asdf-vm/asdf.git $HOME/.asdf
ENV PATH="$PATH:/root/.asdf/bin"
ENV PATH="$PATH:/root/.asdf/shims"

WORKDIR /opt/app

COPY .tool-versions .

RUN asdf plugin-add python
RUN asdf install python

ARG REQUIREMENTS_FILE=requirements-test.txt

COPY $REQUIREMENTS_FILE .
RUN pip install pip-tools==7.3.0 && \
  pip install -r $REQUIREMENTS_FILE

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
