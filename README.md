# Stores REST API

A Flask REST API for managing stores, items, tags, and users. The API uses
SQLAlchemy (via psycopg3 for Postgres) for persistence, JWTs for
authentication, Flask-Smorest for an OpenAPI spec and Swagger UI, and RQ with
Redis for background email delivery via Mailgun.

## Requirements

- Python 3.14 or newer
- [uv](https://docs.astral.sh/uv/)
- A Redis instance (used for the JWT blocklist and the background email queue)

## Setup

Install the project dependencies and create the local virtual environment:

```powershell
uv sync
```

Copy `.env.example` to `.env` and fill in the values:

```powershell
cp .env.example .env
```

| Variable | Required | Description |
| --- | --- | --- |
| `DATABASE_URI` | No | SQLAlchemy database URL. Defaults to `sqlite:///data.db`. A `postgresql://...` URL is automatically rewritten to use the psycopg3 driver (`postgresql+psycopg://`). |
| `JWT_SECRET_KEY` | **Yes** | Secret used to sign JWTs. The app fails to start without it. |
| `REDIS_URL` | No | Redis connection URL for the JWT blocklist and the email queue. Defaults to `redis://localhost:6379`. |
| `MAILGUN_API_KEY` | No | Mailgun API key used to send the registration confirmation email. |

Apply database migrations before running the app for the first time (and
after pulling any change that touches `migrations/`):

```powershell
uv run flask --app py_rest_api db upgrade
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

### Background worker

User registration triggers a confirmation email sent via an RQ background job
(queue name `emails`) instead of blocking the request. Run a worker alongside
the app for these jobs to actually be processed:

```powershell
uv run py-rest-api-worker
```

The worker automatically uses RQ's `SimpleWorker` on Windows (since
`os.fork()` isn't available there) and the standard forking `Worker`
everywhere else.

## Docker

Build and run the container:

```powershell
docker build -t py-rest-api .
docker run --rm -p 5000:5000 `
	-e DATABASE_URI="..." `
	-e JWT_SECRET_KEY="..." `
	-e REDIS_URL="..." `
	-e MAILGUN_API_KEY="..." `
	py-rest-api
```

The container runs `docker-entrypoint.sh`, which applies pending database
migrations (`flask db upgrade`) and then starts Gunicorn, bound to `0.0.0.0`.
It listens on the `PORT` environment variable provided by Render, or falls
back to port `5000` locally.

To run the email worker as a separate process (e.g. a Render Background
Worker service using the same image), override the container's start command
with:

```text
uv run py-rest-api-worker
```

## Database migrations

Schema changes are managed with Flask-Migrate/Alembic via the `migrations/`
directory. The application does **not** auto-create or auto-update tables on
startup — migrations are the only source of truth for the schema.

```powershell
uv run flask --app py_rest_api db migrate -m "describe the change"
uv run flask --app py_rest_api db upgrade
```

## Authentication

Create a user and log in:

```powershell
curl -X POST http://127.0.0.1:5000/register `
	-H "Content-Type: application/json" `
	-d '{"username":"demo","email":"demo@example.com","password":"secret"}'

curl -X POST http://127.0.0.1:5000/login `
	-H "Content-Type: application/json" `
	-d '{"username":"demo","password":"secret"}'
```

Use the returned `access_token` for protected endpoints:

```powershell
curl http://127.0.0.1:5000/store `
	-H "Authorization: Bearer <access_token>"
```

Logging out revokes the current access token by adding its JTI to a
Redis-backed blocklist (with a TTL matching the token's own expiry), so
revocation works correctly even with multiple Gunicorn worker processes.

## Endpoints

| Method | Path | Authentication | Description |
| --- | --- | --- | --- |
| `POST` | `/register` | No | Create a user (queues a confirmation email) |
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
├── __init__.py       # Flask application factory
├── db.py              # SQLAlchemy instance
├── block_list.py      # Redis-backed JWT blocklist helpers
├── tasks.py           # Email rendering/sending, run as RQ jobs
├── worker.py          # RQ worker entry point (py-rest-api-worker)
├── schemas.py          # Marshmallow request/response schemas
├── models/            # Database models
└── resources/         # HTTP resources and route definitions
templates/email/        # Jinja2 templates for outgoing emails
migrations/            # Flask-Migrate/Alembic migrations
Dockerfile             # Production container image
docker-entrypoint.sh   # Applies migrations, then starts Gunicorn
.env.example           # Documents required/optional environment variables
```
