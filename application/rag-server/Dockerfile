# create build stage for
FROM python:3.11-slim AS build
ARG APP_DIR=/rag_server

RUN apt-get update \
    && apt-get install -y \
    curl \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.8.2
RUN curl -sSL https://install.python-poetry.org/ | python - --version $POETRY_VERSION
ENV PATH=/root/.local/bin:$PATH

WORKDIR ${APP_DIR}
COPY pyproject.toml poetry.lock ./

# RUN poetry install
## Included poetry options argument for dev and prod builds
RUN python -m venv --copies ${APP_DIR}/venv

ENV POETRY_OPTIONS="--no-dev"
RUN . ${APP_DIR}/venv/bin/activate && poetry install $POETRY_OPTIONS

# create deployment stage
FROM python:3.11-slim AS run
ARG APP_DIR=/rag_server

COPY --from=build ${APP_DIR}/venv ${APP_DIR}/venv/
ENV PATH=${APP_DIR}/venv/bin:$PATH

WORKDIR ${APP_DIR}
COPY . ./

EXPOSE 8000

CMD ["python", "rag_server/main.py"]
#CMD ["uvicorn", "rag_server.main:app", "--host", "0.0.0.0"]
#CMD ["sleep","3600"]
