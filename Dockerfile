FROM python:3.10-slim

LABEL org.opencontainers.image.title="SafeCrossAI"
LABEL org.opencontainers.image.description="Reproducible container for smart-intersection VRU prediction and risk demos."
LABEL org.opencontainers.image.source="https://github.com/panagiotagrosdouli/SafeCrossAI"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /workspace

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg git \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY src ./src
COPY scripts ./scripts
COPY tests ./tests
COPY configs ./configs
COPY examples ./examples

RUN python -m pip install --upgrade pip \
    && python -m pip install -e .[dev,demo]

CMD ["pytest", "--cov=safecrossai", "--cov-report=term-missing"]
