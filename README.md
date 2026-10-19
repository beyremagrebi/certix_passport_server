# Certix Passport — Backend

Backend infrastructure for the Certix Passport project, built with a microservices architecture.

## Tech Stack

- **Python 3.14** — Backend development
- **FastAPI** — REST API framework
- **Poetry** — Python dependency management
- **PostgreSQL 17** — Relational database
- **SQLAlchemy** — ORM and database interaction
- **Alembic** — Database schema migrations and version control
- **Nginx** — API Gateway
- **Docker Compose** — Infrastructure management

## Project Structure

```text
certix-passport/
├── gateway/
│   └── nginx/
│       └── nginx.conf
├── services/
│   ├── user-service/
│   │   ├── app/
│   │   ├── migrations/
│   │   │   └── versions/
│   │   ├── alembic.ini
│   │   ├── pyproject.toml
│   │   └── .env
│   ├── achievements-service/
│   ├── events-service/
│   └── passport-service/
├── compose.yaml
├── .env
├── .env.example
└── README.md
```

> The User Service is currently under development. The Achievements, Events, and Passport services are planned for future implementation.

## Prerequisites

Install the following tools before starting:

- Python 3.14
- Poetry
- Docker Desktop with WSL 2
- Git
- A code editor such as Visual Studio Code

Verify the installations:

```powershell
python --version
poetry --version
docker --version
docker compose version
git --version
```

## 1. Clone the Repository

```powershell
git clone <YOUR_REPOSITORY_URL>
cd certix-passport
```

Replace `<YOUR_REPOSITORY_URL>` with your Git repository URL.

## 2. Configure Environment Variables

Create a `.env` file in the project root.

Example:

```dotenv
POSTGRES_USER=certix
POSTGRES_PASSWORD=your_local_database_password
POSTGRES_DB=certix_dev
```

Create another `.env` file inside `services/user-service/`.

```dotenv
APP_NAME="Certix Passport - User Service"
APP_VERSION=0.1.0
HOST=0.0.0.0
PORT=8005
DEBUG=true
DATABASE_URL=postgresql+psycopg://certix:your_local_database_password@127.0.0.1:5432/certix_dev
```

Replace `your_local_database_password` with your local database password.

If your password contains special characters such as `@`, `:`, `/`, or `#`, ensure it is correctly URL-encoded in `DATABASE_URL`.

**Important:** Never commit real passwords, tokens, or secret keys to Git. Keep `.env` files out of version control and use `.env.example` to document required variables.

## 3. Start PostgreSQL and the API Gateway

From the project root, run:

```powershell
docker compose up -d db gateway
```

Check the containers:

```powershell
docker compose ps
```

View PostgreSQL logs:

```powershell
docker compose logs db
```

View Gateway logs:

```powershell
docker compose logs gateway
```

Stop the infrastructure:

```powershell
docker compose stop
```

Stop and remove the containers:

```powershell
docker compose down
```

> `docker compose down` preserves the named database volume. Do not use `docker compose down -v` unless you intentionally want to delete the database volume.

## 4. Set Up the User Service

Open a terminal in the User Service directory:

```powershell
cd services/user-service
```

Install the dependencies:

```powershell
poetry install
```

Start the service:

```powershell
poetry run dev
```

The service should be available at:

- API: http://127.0.0.1:8005
- Swagger documentation: http://127.0.0.1:8005/docs
- Health check: http://127.0.0.1:8005/health

To stop the service, press `Ctrl + C`.

## 5. API Gateway

The Nginx API Gateway listens on port `8080` and forwards User Service requests to port `8005`.

Gateway URLs:

- Gateway status: http://localhost:8080
- User Service health: http://localhost:8080/api/users/health

Configuration file:

```text
gateway/nginx/nginx.conf
```

Validate the Nginx configuration:

```powershell
docker compose exec gateway nginx -t
```

Reload Nginx after editing its configuration:

```powershell
docker compose exec gateway nginx -s reload
```

Recreate the Gateway container after relevant Compose changes:

```powershell
docker compose up -d gateway
```

## 6. Database

The project uses PostgreSQL as its relational database and SQLAlchemy as its ORM.

Local connection settings:

| Setting | Value |
|---|---|
| Host | `127.0.0.1` |
| Port | `5432` |
| Database | `certix_dev` |
| Username | `certix` |
| Password | Configured in `.env` |

### SQLAlchemy Models

SQLAlchemy models define the structure of database tables.

For example, the `User` model defines the columns belonging to the `users` table.

However, changing a model in Python does **not** automatically update an existing PostgreSQL table. A database migration is needed to apply schema changes safely and consistently.

### What Is Alembic?

Alembic is a database migration tool designed to work with SQLAlchemy.

It tracks changes to the database schema over time. These changes can include:

- Creating or dropping tables
- Adding or removing columns
- Changing column types
- Adding constraints and indexes

Alembic generates migration scripts that describe how to move the database schema from one version to another.

Each migration has an `upgrade()` function to apply changes and a `downgrade()` function to reverse them when possible.

### Why Do We Use Alembic?

Alembic helps the team keep database schemas consistent across development environments and deployments.

Without migrations, a developer might change a SQLAlchemy model while the actual database remains unchanged. This can cause application errors or differences between teammates' databases.

With Alembic:

1. A developer updates a SQLAlchemy model.
2. Alembic generates a migration based on the detected schema differences.
3. The developer reviews the migration.
4. The migration file is committed to Git.
5. Other developers pull the changes and apply the migration to their own databases.

**Important:** Alembic manages database schema changes. It does not replace SQLAlchemy, implement CRUD operations, or automatically migrate the database every time the application starts.

## 7. Database Migration Workflow

Run all Alembic commands from the User Service directory:

```powershell
cd services/user-service
```

### 7.1 Check the Current Migration Version

```powershell
poetry run alembic current
```

This displays the migration revision currently recorded in the database.

To see the migration history:

```powershell
poetry run alembic history
```

### 7.2 Modify a SQLAlchemy Model

For example, suppose you want to add a `phone` column to the `User` model:

```python
phone: Mapped[str | None] = mapped_column(
    String(20),
    nullable=True,
)
```

This changes the model definition, but it does not modify the existing database table.

### 7.3 Generate a Migration

Run:

```powershell
poetry run alembic revision --autogenerate -m "add user phone"
```

Alembic compares the SQLAlchemy model metadata with the database schema and generates a new migration file inside:

```text
migrations/versions/
```

The filename includes a unique revision identifier.

**Autogeneration is not perfect.** Always review the generated migration before applying it. Some changes, data transformations, and database-specific operations may require manual editing.

If the generated migration contains only `pass`, Alembic did not detect a schema difference. Check that the model is imported into `migrations/env.py`, the correct database is configured, and the model change is detectable.

### 7.4 Review the Migration

Open the generated migration file and inspect both `upgrade()` and `downgrade()`.

For an added column, the upgrade operation may resemble:

```python
op.add_column(
    "users",
    sa.Column("phone", sa.String(length=20), nullable=True),
)
```

This is an illustrative example; use the actual generated migration and review it before applying.

### 7.5 Apply the Migration

After reviewing the file, run:

```powershell
poetry run alembic upgrade head
```

Alembic applies pending migrations up to the latest revision, called `head`.

### 7.6 Verify the Database Schema

From the project root, you can inspect the table using Docker:

```powershell
docker exec -it certix-postgres psql -U certix -d certix_dev -c "\d users"
```

You can also check the applied revision:

```powershell
poetry run alembic current
```

Run the second command from the User Service directory.

### 7.7 Commit the Model and Migration

After testing, commit both the updated model and the generated migration file.

```powershell
git status
git add services/user-service/app/models/
git add services/user-service/migrations/
git commit -m "Add phone field to user model"
git push
```

Adjust the file paths if your model is located elsewhere.

### 7.8 Apply a Teammate's Migration

After pulling the latest changes:

```powershell
git pull
cd services/user-service
poetry run alembic upgrade head
```

This applies pending migrations to your local database.

Do not generate another migration just because you pulled someone else's migration. Generate one only when you have your own schema changes to make.

### Migration Safety Rules

- Never commit `.env` files or credentials.
- Always commit migration files to Git.
- Do not modify a migration that teammates have already applied or that has already been shared; create a new migration instead.
- Review migrations before applying them.
- Be careful with migrations that drop columns, drop tables, or alter existing data.
- Do not apply destructive migrations to shared or production databases without approval.
- Coordinate changes when multiple developers modify the same schema.
- Ensure a new developer's database is at the expected migration baseline before applying new migrations.

### Existing Database Baseline

If a database already contains tables before Alembic is introduced, its existing schema must be reconciled with the migration history.

For a database that has been checked and confirmed to match the initial migration baseline, Alembic can record the baseline without executing the migration:

```powershell
poetry run alembic stamp head
```

**Warning:** `stamp head` only updates Alembic's version record; it does not create or modify tables. Use it only when the existing schema genuinely matches the intended revision. Otherwise, reconcile the schema first.

## 8. Useful Docker Commands

Check running containers:

```powershell
docker compose ps
```

Start the infrastructure:

```powershell
docker compose up -d
```

Stop the infrastructure:

```powershell
docker compose stop
```

Restart the Gateway:

```powershell
docker compose restart gateway
```

Follow logs:

```powershell
docker compose logs -f db
docker compose logs -f gateway
```

Rebuild or recreate services after relevant configuration changes:

```powershell
docker compose up -d --build
```

## 9. Useful Git Commands

Check modified files:

```powershell
git status
```

Stage changes:

```powershell
git add .
```

Commit changes:

```powershell
git commit -m "Describe your changes"
```

Push changes:

```powershell
git push
```

Before using `git add .`, check `git status` to ensure you are not staging secrets or local-only files.

## Current Status

- [x] PostgreSQL infrastructure
- [x] Nginx API Gateway configuration
- [x] User Service foundation
- [x] SQLAlchemy database connection
- [x] SQLAlchemy User model
- [x] Alembic initialization and migration configuration
- [ ] User CRUD endpoints
- [ ] Complete user authentication and authorization
- [ ] Achievements Service
- [ ] Events Service
- [ ] Passport Service

## Notes

- Run Docker Compose commands from the project root containing `compose.yaml`.
- Run User Service and Alembic commands from `services/user-service`.
- Ensure PostgreSQL is running before applying migrations.
- The other services are placeholders until implemented.
- Keep migration files in Git; exclude local `.env` files.
- Schema changes must be managed through reviewed Alembic migrations rather than relying on SQLAlchemy models to update existing tables automatically.
