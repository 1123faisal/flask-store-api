# Stores REST API

A Flask REST API for managing stores, items, tags, and users. The API uses
SQLAlchemy for persistence, JWTs for authentication, and Flask-Smorest to
provide an OpenAPI specification and Swagger UI.

## Requirements

- Python 3.14 or newer
- [uv](https://docs.astral.sh/uv/)

## Setup

Install the project dependencies and create the local virtual environment:

```powershell
uv sync
```

The application uses SQLite at `src/instance/data.db` by default. Set
`DATABASE_URI` to use another SQLAlchemy-compatible database URL, for example:

```powershell
$env:DATABASE_URI = "sqlite:///data.db"
```

## Run locally

Start the development server with:

```powershell
uv run flask --app py_rest_api run --debug
```

The API is available at <http://127.0.0.1:5000>. Interactive API documentation
is available at <http://127.0.0.1:5000/swagger-ui>, and the OpenAPI document is
available at <http://127.0.0.1:5000/openapi.json>.

The project also exposes a console script:

```powershell
uv run py-rest-api
```

## Docker

Build and run the container:

```powershell
docker build -t py-rest-api .
docker run --rm -p 5000:5000 py-rest-api
```

The container runs Gunicorn and listens on `0.0.0.0`. It uses the `PORT`
environment variable provided by Render, or falls back to port `5000` locally.

## Database migrations

The application creates missing tables when it starts. For schema changes,
Flask-Migrate is configured with the `migrations/` directory:

```powershell
uv run flask --app py_rest_api db migrate -m "describe the change"
uv run flask --app py_rest_api db upgrade
```

## Authentication

Create a user and log in:

```powershell
curl -X POST http://127.0.0.1:5000/register `
	-H "Content-Type: application/json" `
	-d '{"username":"demo","password":"secret"}'

curl -X POST http://127.0.0.1:5000/login `
	-H "Content-Type: application/json" `
	-d '{"username":"demo","password":"secret"}'
```

Use the returned `access_token` for protected endpoints:

```powershell
curl http://127.0.0.1:5000/store `
	-H "Authorization: Bearer <access_token>"
```

## Endpoints

| Method | Path | Authentication | Description |
| --- | --- | --- | --- |
| `POST` | `/register` | No | Create a user |
| `POST` | `/login` | No | Get access and refresh tokens |
| `POST` | `/refresh` | Refresh token | Get a new access token |
| `POST` | `/logout` | Access token | Revoke the current access token |
| `GET`, `POST` | `/store` | Access token | List or create stores |
| `GET`, `PUT`, `DELETE` | `/store/{store_id}` | Access token | Read, update, or delete a store |
| `GET`, `POST` | `/item` | Access token | List or create items |
| `GET`, `PUT`, `DELETE` | `/item/{item_id}` | Access token | Read, update, or delete an item |
| `GET`, `POST` | `/store/{store_id}/tag` | Access token | List or create store tags |
| `GET`, `DELETE` | `/tag/{tag_id}` | Access token | Read or delete a tag |
| `POST`, `DELETE` | `/item/{item_id}/tag/{tag_id}` | Access token | Link or unlink a tag from an item |
| `GET`, `DELETE` | `/user/{user_id}` | Access token | Read or delete a user |

## Project layout

```text
src/py_rest_api/
├── __init__.py       # Flask application factory and CLI entry point
├── db.py              # SQLAlchemy instance
├── models/            # Database models
└── resources/         # HTTP resources and route definitions
migrations/            # Flask-Migrate/Alembic migrations
Dockerfile             # Production container image
```
