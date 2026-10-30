# Certix Passport — Backend BEYREM

## Prerequisites

Install the following tools:

- Git
- Docker Desktop
- Python
- Poetry

## 1. Clone the project

```bash
git clone https://github.com/beyremagrebi/certix_passport_server.git
cd certix-passport
```

Replace `https://github.com/beyremagrebi/certix_passport_server.git` with the actual Git repository URL.

## 2. Configure the root `.env`

Create a `.env` file in the project root, next to `docker-compose.yml`:

```env
POSTGRES_DB=certix_dev
POSTGRES_USER=certix
POSTGRES_PASSWORD=your_local_password
```

Use the same PostgreSQL password in the User Service `.env`.

## 3. Start Docker services

From the project root, run:

```bash
docker compose up -d db gateway
```

Check that PostgreSQL is running:

```bash
docker compose ps
```

## 4. Create the database if it does not exist

Run this command from the project root:

```bash
docker compose run --rm ensure-db
```

This checks whether `certix_dev` exists. If it does not exist, it creates the database.

## 5. Configure the User Service `.env`

Go to the User Service directory:

```bash
cd services/user-service
```

Create a `.env` file in this directory:

```env
PORT=8001

# Database
DATABASE_URL=postgresql+psycopg://certix:your_local_password@127.0.0.1:5432/certix_dev

# Application
SECRET_KEY=replace_with_a_secure_random_secret

# JWT
JWT_SECRET_KEY=replace_with_a_secure_random_secret
JWT_ACCESS_TOKEN_EXPIRES_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRES_DAYS=30
PROFILE_PHOTO_STORAGE_DIR=./storage/profile-photos
PROFILE_PHOTO_MAX_BYTES=5242880
PROFILE_PHOTO_MAX_WIDTH=2048
PROFILE_PHOTO_MAX_HEIGHT=2048
PROFILE_PHOTO_ALLOWED_FORMATS=JPEG,PNG,WEBP
```

Replace `your_local_password` with the same password used in the root `.env`.

Generate secure random secrets for `SECRET_KEY` and `JWT_SECRET_KEY`. Do not commit real secrets to Git.

Email delivery can use the local console logger, Brevo, or SMTP. For SMTP
deployment, set `EMAIL_PROVIDER=smtp`, use a verified sender address, and
provide the SMTP server credentials through deployment secrets:

```env
EMAIL_PROVIDER=smtp
EMAIL_FROM_ADDRESS=no-reply@example.com
EMAIL_FROM_NAME=Certix Passport
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=your-smtp-username
SMTP_PASSWORD=your-smtp-password
SMTP_USE_TLS=true
SMTP_USE_SSL=false
```

Use port `465` with `SMTP_USE_SSL=true` and `SMTP_USE_TLS=false` when required
by the provider. Never commit SMTP credentials.

## 6. Install dependencies

From `services/user-service`:

```bash
poetry install
```

On Windows, starting from the repository root, use:

```powershell
cd services\user-service
poetry install
```

## 7. Run database migrations

Run this from `services\user-service` (the directory containing
`pyproject.toml`):

```bash
poetry run flask --app app db upgrade
```

On Windows, starting from the repository root:

```powershell
cd services\user-service
poetry run flask --app app db upgrade
```

This applies the existing migrations and creates or updates the database tables.

If migrations have not been generated yet, create an initial migration before running `upgrade`:

```bash
poetry run flask --app app db migrate -m "Initial migration"
poetry run flask --app app db upgrade
```

Only generate a migration if the project does not already have the required migration files.

## 8. Start the User Service

```bash
poetry run user-service
```

On Windows, if you are at the repository root:

```powershell
cd services\user-service
poetry run user-service
```

The service should run on:

```text
http://127.0.0.1:8001
```

Use the actual routes defined in the application to test the API.

### Profile photo upload

Authenticated clients can upload a profile photo as multipart form data:

```text
POST /users/me/profile-photo
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
photo=<image>
```

The service validates the image bytes, format, file size, and dimensions before
storing it in the configured file store. The response contains an opaque
`asset_ref`; the internal storage path is never exposed.

## Quick Start

For subsequent starts, from the project root:

```bash
docker compose up -d db
docker compose run --rm ensure-db
```

Then start the User Service:

```bash
cd services/user-service
poetry run flask --app app db upgrade
poetry run user-service
```

## Stop Docker services

From the project root:

```bash
docker compose stop
```

To stop and remove the containers without deleting the database volume:

```bash
docker compose down
```

**Important:** Do not use `docker compose down -v` unless you intentionally want to delete the PostgreSQL volume and its stored data.
