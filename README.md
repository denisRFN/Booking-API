## Booking API (FastAPI)

Backend API for the desk booking application. Provides authentication, desk management, reservations, availability, and admin features.

### Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL (Azure Database for PostgreSQL) 
- JWT authentication
- Docker support 

### Configuration
Configuration is driven via environment variables:

- `DATABASE_URL` – PostgreSQL connection string (Azure). Example :
  `postgresql+psycopg2://user:password@host:5432/dbname`
- `SECRET_KEY` – strong secret key used for JWT signing
- `ACCESS_TOKEN_EXPIRE_MINUTES` – JWT expiration in minutes (default: 60)
- `ALGORITHM` – JWT algorithm (default: HS256)
- `ENVIRONMENT` – `dev` or `prod` (optional)

You will set the real values in Azure App Service configuration.

### Local Development

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set `DATABASE_URL` (pointing to your local or Azure PostgreSQL).
4. Run the app:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

### Docker

Build and run using Docker:

```bash
docker build -t booking-api .
docker run -p 8000:8000 --env-file .env booking-api
```

`.env` should contain at least `DATABASE_URL` and `SECRET_KEY`.

### Azure Deployment (Overview)

This repository includes a GitHub Actions workflow under `.github/workflows/api-azure-deploy.yml` that can:

- Build the application
- Run tests (if added)
- Deploy to Azure Web App

You will need to configure the following GitHub secrets in your API repository:

- `AZURE_CREDENTIALS` – JSON output from `az ad sp create-for-rbac`
- `AZURE_WEBAPP_NAME_API` – Azure Web App name for the backend
- `AZURE_WEBAPP_RESOURCE_GROUP` – Resource group name

In Azure Web App configuration, set:

- `DATABASE_URL`
- `SECRET_KEY`
- any other environment variables you need

