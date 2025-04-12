FROM python:3.12-slim AS python-base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=true \
    UV_PROJECT_ENVIRONMENT=/app/.venv/ \
    UV_CACHE_DIR=/tmp/.cache/uv \
    PATH=/app/.venv/bin:${PATH}


FROM python-base AS python-nonroot
ARG USERNAME=nonroot
ARG UID=1000
ARG GID=1000

RUN groupadd -g ${GID} ${USERNAME} \
 && useradd -M -s /bin/sh -u ${UID} -g ${GID} ${USERNAME}
USER ${USERNAME}


FROM python-base AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=cache,target=${UV_CACHE_DIR},sharing=locked \
    uv sync --frozen

COPY . /app


FROM python-nonroot AS dev
WORKDIR /app

COPY --from=builder /usr/bin/uv /usr/bin/uvx /usr/bin/
COPY --from=builder --chown=${UID}:${GID} /app /app
