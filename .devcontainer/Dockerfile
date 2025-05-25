FROM python:3.11-bookworm

ENV DEBIAN_FRONTEND="noninteractive"

RUN apt-get -y update
RUN apt-get -y install --no-install-recommends ca-certificates sudo curl less
RUN apt-get -y install --no-install-recommends build-essential git-core
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

RUN useradd -d /workspace/quest-agent -N -m -s /bin/bash agent
RUN echo "agent ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/agent
RUN chown -R agent: /workspace/quest-agent

USER agent
WORKDIR /workspace/quest-agent

ENV UV_LINK_MODE="copy"
ENV HOME="/workspace/quest-agent"
ENV PATH="${HOME}/.local/bin:${PATH}"

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
