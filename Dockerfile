FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
EXPOSE 5000

COPY pyproject.toml uv.lock README.md ./
RUN uv sync --locked --no-install-project

COPY src ./src
RUN uv sync --locked

CMD ["uv", "run", "--no-dev", "flask", "--app", "py_rest_api", "run", "--host", "0.0.0.0", "--port", "5000"]