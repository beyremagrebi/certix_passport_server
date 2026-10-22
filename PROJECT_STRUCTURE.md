# Project structure

Generated from the repository tree. Runtime, cache, dependency, and version-control directories are omitted.

```text
certix_passport_server/
|-- gateway/
|   \-- nginx/
|       \-- nginx.conf
|-- services/
|   |-- achievement-service/
|   |   \-- .gitkeep
|   |-- event-service/
|   |   \-- .gitkeep
|   |-- passport-service/
|   |   \-- .gitkeep
|   \-- user-service/
|       |-- migrations/
|       |   |-- versions/
|       |   |   |-- 0175c26f816b_merge_profile_photo_and_user_role_.py
|       |   |   |-- 2da6b766cdbf_initial_schema.py
|       |   |   |-- 3481ba87b175_add_refresh_tokens.py
|       |   |   |-- 7f8c2d9a4b11_add_profile_photo_reference.py
|       |   |   |-- a1b2c3d4e5f6_add_profile_fields.py
|       |   |   \-- e9001f9ca92e_add_user_role_enum.py
|       |   |-- alembic.ini
|       |   |-- env.py
|       |   |-- README
|       |   \-- script.py.mako
|       |-- src/
|       |   \-- app/
|       |       |-- controllers/
|       |       |   |-- auth.py
|       |       |   |-- profile.py
|       |       |   \-- user.py
|       |       |-- decorators/
|       |       |   \-- authorization.py
|       |       |-- handlers/
|       |       |   \-- error_handlers.py
|       |       |-- middlewares/
|       |       |   \-- jwt_middleware.py
|       |       |-- models/
|       |       |   |-- base.py
|       |       |   |-- refresh_token.py
|       |       |   |-- user.py
|       |       |   \-- user_role.py
|       |       |-- repositories/
|       |       |   \-- user_repository.py
|       |       |-- routes/
|       |       |   |-- __init__.py
|       |       |   |-- admin.py
|       |       |   |-- auth.py
|       |       |   |-- health.py
|       |       |   |-- profile.py
|       |       |   \-- user.py
|       |       |-- services/
|       |       |   |-- auth.py
|       |       |   |-- profile_photo.py
|       |       |   \-- user.py
|       |       |-- utils/
|       |       |   \-- api_response.py
|       |       |-- validators/
|       |       |   |-- auth.py
|       |       |   |-- profile.py
|       |       |   |-- profile_photo.py
|       |       |   \-- user.py
|       |       |-- __init__.py
|       |       |-- cli.py
|       |       |-- config.py
|       |       |-- database.py
|       |       \-- extensions.py
|       |-- .env
|       |-- .env.example
|       |-- poetry.lock
|       \-- pyproject.toml
|-- .env
|-- .env.example
|-- .gitignore
|-- docker-compose.yml
\-- README.md
```
