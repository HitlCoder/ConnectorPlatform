# Docker Quick Start - 2 Minutes Setup ⚡

Run the entire Connector Platform locally with one command - no Python, Node.js, or PostgreSQL installation needed!

## 1. Install Docker Desktop

Download and install Docker Desktop for your operating system:
- **Windows**: https://docs.docker.com/desktop/install/windows-install/
- **Mac**: https://docs.docker.com/desktop/install/mac-install/
- **Linux**: https://docs.docker.com/desktop/install/linux-install/

## 2. Start the Platform

Open a terminal in the project directory and run:

```bash
docker-compose up -d
```

That's it! 🎉

## 3. Access the Application

- **Dashboard**: http://localhost:5000
- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## What's Running?

The command starts three services:
1. **PostgreSQL Database** (port 5432) - Data storage
2. **Backend API** (port 8000) - FastAPI server
3. **Frontend Dashboard** (port 5000) - React UI

## Useful Commands

### View Logs
```bash
docker-compose logs -f
```

### Stop Everything
```bash
docker-compose down
```

### Restart Services
```bash
docker-compose restart
```

### Rebuild After Changes
```bash
docker-compose up -d --build
```

## Configuration

### Add OAuth Credentials

Edit `docker-compose.yml` and add your API keys:

```yaml
backend:
  environment:
    ONEDRIVE_CLIENT_ID: your_client_id
    ONEDRIVE_CLIENT_SECRET: your_client_secret
    DROPBOX_APP_KEY: your_app_key
    DROPBOX_APP_SECRET: your_app_secret
    GMAIL_CLIENT_ID: your_client_id
    GMAIL_CLIENT_SECRET: your_client_secret
```

Then restart:
```bash
docker-compose restart backend
```

## Troubleshooting

### Port Already in Use?

If ports 5000, 8000, or 5432 are already taken, edit `docker-compose.yml`:

```yaml
ports:
  - "3000:5000"  # Change 5000 -> 3000
  - "8080:8000"  # Change 8000 -> 8080
```

### Database Issues?

Reset the database:
```bash
docker-compose down -v
docker-compose up -d
```

## Next Steps

For detailed Docker documentation, see [docker-setup.md](docker-setup.md)

For platform documentation, see [README.md](README.md)

---

**Happy coding!** 🚀
