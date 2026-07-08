FROM python:3.10-slim

WORKDIR /workspace

COPY pyproject.toml README.md ./
COPY src ./src
COPY scripts ./scripts
COPY tests ./tests

RUN python -m pip install --upgrade pip && \
    python -m pip install -e .[dev,demo]

CMD ["pytest"]
