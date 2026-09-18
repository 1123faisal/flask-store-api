FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
EXPOSE 5000

COPY pyproject.toml uv.lock README.md ./
RUN uv sync --locked --no-install-project

COPY src ./src
RUN uv sync --locked

CMD ["sh", "-c", "exec uv run --no-dev gunicorn --bind 0.0.0.0:${PORT:-5000} --access-logfile - --error-logfile - 'py_rest_api:create_app()'"]