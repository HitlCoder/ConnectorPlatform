# Deployment Guide

## Prerequisites

- Python 3.11+
- PostgreSQL database
- OAuth credentials for connectors you want to use

## Environment Variables

Set the following environment variables:

```bash
# Database
export DATABASE_URL="postgresql://user:password@host:port/database"

# Gmail Connector
export GMAIL_CLIENT_ID="your-gmail-client-id"
export GMAIL_CLIENT_SECRET="your-gmail-client-secret"

# OneDrive Connector
export ONEDRIVE_CLIENT_ID="your-onedrive-client-id"
export ONEDRIVE_CLIENT_SECRET="your-onedrive-client-secret"

# Dropbox Connector
export DROPBOX_CLIENT_ID="your-dropbox-client-id"
export DROPBOX_CLIENT_SECRET="your-dropbox-client-secret"
```

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Initialize the database:

The database tables will be automatically created on first startup.

3. Start the server:

```bash
python main.py
```

The API will be available at `http://0.0.0.0:5000`

## Production Deployment

### Using Gunicorn

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:5000 main:app
```

### Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
```

Build and run:

```bash
docker build -t connector-platform .
docker run -p 5000:5000 --env-file .env connector-platform
```

### Environment Configuration

For production, use a `.env` file:

```env
DATABASE_URL=postgresql://user:password@host:port/database
GMAIL_CLIENT_ID=xxx
GMAIL_CLIENT_SECRET=xxx
ONEDRIVE_CLIENT_ID=xxx
ONEDRIVE_CLIENT_SECRET=xxx
DROPBOX_CLIENT_ID=xxx
DROPBOX_CLIENT_SECRET=xxx
```

## Monitoring

### Health Check

```bash
curl http://localhost:5000/health
```

### Logs

The application uses uvicorn's logging. Configure log level:

```bash
uvicorn main:app --log-level info
```

## Scaling

### Horizontal Scaling

The platform is stateless and can be scaled horizontally:

```bash
# Start multiple workers
gunicorn -w 8 -k uvicorn.workers.UvicornWorker main:app
```

### Database Connection Pooling

Configure SQLAlchemy connection pooling in `database.py`:

```python
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40
)
```

### Load Balancing

Use nginx as a reverse proxy:

```nginx
upstream connector_platform {
    server 127.0.0.1:5000;
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
    server 127.0.0.1:5003;
}

server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://connector_platform;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Security Hardening

1. **HTTPS Only**: Use SSL/TLS in production
2. **Rate Limiting**: Add rate limiting middleware
3. **CORS**: Configure CORS for specific origins
4. **Token Encryption**: Encrypt tokens in database
5. **API Authentication**: Add API key authentication

## Backup

### Database Backup

```bash
pg_dump -h localhost -U user -d database > backup.sql
```

### Restore

```bash
psql -h localhost -U user -d database < backup.sql
```

## Troubleshooting

### Database Connection Issues

Check `DATABASE_URL` format:
```
postgresql://user:password@host:port/database
```

### OAuth Errors

Verify:
1. Environment variables are set
2. Redirect URIs match OAuth app configuration
3. Scopes are correct

### Port Conflicts

Change the port in `main.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8000)
```
