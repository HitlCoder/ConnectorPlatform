# Docker Setup Guide

## Prerequisites

1. **Install Docker Desktop**
   - Windows: https://docs.docker.com/desktop/install/windows-install/
   - Mac: https://docs.docker.com/desktop/install/mac-install/
   - Linux: https://docs.docker.com/desktop/install/linux-install/

2. **Verify Installation**
   ```bash
   docker --version
   docker-compose --version
   ```

## Quick Start

### 1. Start All Services

From the project root directory, run:

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database (port 5432)
- Backend API (port 8000)
- Frontend dashboard (port 5000)

### 2. View Logs

Watch all service logs:
```bash
docker-compose logs -f
```

View specific service logs:
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### 3. Access the Application

- **Frontend Dashboard**: http://localhost:5000
- **Backend API**: http://localhost:8000
- **API Health Check**: http://localhost:8000/health
- **API Docs**: http://localhost:8000/docs (FastAPI auto-generated)

## Management Commands

### Stop All Services
```bash
docker-compose down
```

### Stop and Remove All Data
```bash
docker-compose down -v
```

### Restart a Specific Service
```bash
docker-compose restart backend
docker-compose restart frontend
```

### Rebuild After Code Changes
```bash
docker-compose up -d --build
```

### View Running Containers
```bash
docker-compose ps
```

### Execute Commands in Containers

Python shell in backend:
```bash
docker-compose exec backend python
```

Database shell:
```bash
docker-compose exec postgres psql -U connector_user -d connector_platform
```

Bash shell in backend:
```bash
docker-compose exec backend bash
```

## Configuration

### Environment Variables

Edit `docker-compose.yml` to configure:

**Database Settings:**
```yaml
POSTGRES_USER: your_db_user
POSTGRES_PASSWORD: your_db_password
POSTGRES_DB: your_db_name
```

**OAuth Credentials (for connectors):**
```yaml
ONEDRIVE_CLIENT_ID: your_onedrive_client_id
ONEDRIVE_CLIENT_SECRET: your_onedrive_client_secret
DROPBOX_APP_KEY: your_dropbox_app_key
DROPBOX_APP_SECRET: your_dropbox_app_secret
GMAIL_CLIENT_ID: your_gmail_client_id
GMAIL_CLIENT_SECRET: your_gmail_client_secret
```

**Kafka Settings (if using real Kafka):**
```yaml
KAFKA_ENABLED: "true"
KAFKA_BOOTSTRAP_SERVERS: "kafka:9092"
```

### Adding Kafka (Optional)

To add Kafka to the stack, add this service to `docker-compose.yml`:

```yaml
  kafka:
    image: confluentinc/cp-kafka:latest
    container_name: connector-platform-kafka
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    depends_on:
      - zookeeper

  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    container_name: connector-platform-zookeeper
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
```

Then update backend environment:
```yaml
KAFKA_ENABLED: "true"
KAFKA_BOOTSTRAP_SERVERS: "kafka:9092"
```

## Development Workflow

### Hot Reload

Both frontend and backend support hot reload:

- **Backend**: Code changes in `connector_platform/` and `main.py` are mounted and will reload automatically
- **Frontend**: Changes in `frontend/src/` trigger Vite's hot reload

### Database Migrations

Run database migrations:
```bash
docker-compose exec backend python -c "from connector_platform.database import init_db; init_db()"
```

Or access database directly:
```bash
docker-compose exec postgres psql -U connector_user -d connector_platform
```

### Install New Python Packages

1. Add package to `requirements.txt`
2. Rebuild backend:
   ```bash
   docker-compose up -d --build backend
   ```

### Install New NPM Packages

1. Add package to `frontend/package.json`
2. Rebuild frontend:
   ```bash
   docker-compose up -d --build frontend
   ```

## Troubleshooting

### Port Already in Use

If ports 5000, 8000, or 5432 are already in use, modify `docker-compose.yml`:

```yaml
ports:
  - "8080:8000"  # Change 8000 -> 8080 for backend
  - "3000:5000"  # Change 5000 -> 3000 for frontend
  - "5433:5432"  # Change 5432 -> 5433 for postgres
```

### Database Connection Issues

Check if postgres is healthy:
```bash
docker-compose ps
docker-compose logs postgres
```

Reset database:
```bash
docker-compose down -v
docker-compose up -d
```

### Backend Not Starting

View backend logs:
```bash
docker-compose logs backend
```

Check if database is ready:
```bash
docker-compose exec postgres pg_isready -U connector_user
```

### Frontend Build Errors

Clear node modules and rebuild:
```bash
docker-compose down
docker-compose build --no-cache frontend
docker-compose up -d
```

## Production Deployment

For production, create a `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    environment:
      # Use production database
      DATABASE_URL: ${PROD_DATABASE_URL}
      
      # Enable Kafka
      KAFKA_ENABLED: "true"
      KAFKA_BOOTSTRAP_SERVERS: ${KAFKA_SERVERS}
      
      # Production secrets
      SESSION_SECRET: ${SESSION_SECRET}
      ONEDRIVE_CLIENT_ID: ${ONEDRIVE_CLIENT_ID}
      ONEDRIVE_CLIENT_SECRET: ${ONEDRIVE_CLIENT_SECRET}
    restart: always

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
      args:
        - NODE_ENV=production
    environment:
      VITE_API_URL: ${API_URL}
    restart: always
```

Run with:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Clean Up

Remove all containers, networks, and volumes:
```bash
docker-compose down -v
docker system prune -a
```

## Next Steps

1. Start the services: `docker-compose up -d`
2. Visit http://localhost:5000 to see the dashboard
3. Configure OAuth credentials in `docker-compose.yml`
4. Create your first connection!

For more information, see the main README.md
