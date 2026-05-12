# Telegram Sound Bot 🎵

A modern, async Telegram bot for managing and sharing sound files with inline queries. Features include audio storage, keyword-based retrieval, and inline query support.

## ✨ Features

- 🎵 Store and manage audio files with custom keywords
- 🔍 Search sounds using inline queries in any chat
- 💾 Persistent storage with PostgreSQL
- ⚡ Fully async with aiogram 3.x
- 🐳 Docker & docker-compose ready
- 🔐 Environment-based configuration
- 📝 Comprehensive error handling
- 🚀 Production-ready

## Requirements

- Python 3.10+
- PostgreSQL 12+ (for production)
- Or Docker & Docker Compose

## Quick Start

### Option 1: Local Installation

```bash
# Clone repository
git clone https://github.com/Mental98971/telegram-sound-bot.git
cd telegram-sound-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your BOT_TOKEN and DATABASE_URL

# Run
python main.py
```

### Option 2: Docker Installation

```bash
# Clone repository
git clone https://github.com/Mental98971/telegram-sound-bot.git
cd telegram-sound-bot

# Setup environment
cp .env.example .env
# Edit .env with your BOT_TOKEN

# Run with docker-compose (includes PostgreSQL)
docker-compose up -d

# View logs
docker-compose logs -f bot
```

## Configuration

Create `.env` file (copy from `.env.example`):

```env
# Required
BOT_TOKEN=your_telegram_bot_token

# Database (choose one)
# For SQLite (development):
DATABASE_URL=sqlite:///./sounds.db

# For PostgreSQL (production):
DATABASE_URL=postgresql+asyncpg://user:password@localhost/sound_bot
DB_PASSWORD=your_password  # For docker-compose
```

## Usage

### Adding Sounds

1. Send an audio file to the bot
2. Bot asks for a keyword
3. Reply with the keyword
4. Sound is saved and searchable

### Using Inline Queries

1. Open any chat
2. Type: `@your_bot_username keyword`
3. Select sound from results
4. Sound is sent to the chat

## API Reference

### Database Schema

```sql
CREATE TABLE sounds (
    keyword VARCHAR PRIMARY KEY,
    file_id VARCHAR NOT NULL,
    owner_id BIGINT NOT NULL,
    deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `BOT_TOKEN` | Yes | Telegram Bot Token from @BotFather |
| `DATABASE_URL` | Yes | Database connection string |
| `LOG_LEVEL` | No | Logging level (default: INFO) |

## Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f bot

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Rebuild image
docker-compose build --no-cache

# Execute command in container
docker-compose exec bot python main.py
```

## Development

### Setup dev environment

```bash
pip install -r requirements.txt -e .[dev]
```

### Code formatting

```bash
black .
isort .
```

### Linting

```bash
flake8 .
mypy main.py
```

### Run tests

```bash
pytest -v
```

## Project Structure

```
telegram-sound-bot/
├── main.py                 # Main bot code
├── requirements.txt        # Python dependencies
├── pyproject.toml         # Modern Python packaging
├── Dockerfile             # Container image
├── docker-compose.yml     # Multi-service orchestration
├── .env.example           # Configuration template
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## Troubleshooting

### Bot not responding

```bash
# Check BOT_TOKEN is correct
echo $BOT_TOKEN

# View logs
docker-compose logs bot

# Verify bot is running
docker-compose ps
```

### Database connection errors

```bash
# Check database is running
docker-compose ps postgres

# Verify DATABASE_URL format
echo $DATABASE_URL

# Test connection
docker-compose exec postgres psql -U soundbot -d sound_bot -c "SELECT 1"
```

### Permission issues

```bash
# Ensure bot has correct permissions in your Telegram chat
# Go to chat settings → Administrators → Add your bot
```

## Performance Tips

1. **Use PostgreSQL** for production (SQLite for development only)
2. **Enable connection pooling** in SQLAlchemy
3. **Set appropriate cache_time** in inline results
4. **Monitor bot resource usage** with `docker stats`

## Deployment

### Using Docker Swarm

```bash
docker swarm init
docker stack deploy -c docker-compose.yml sound-bot
```

### Using Kubernetes

```bash
kubectl create configmap bot-config --from-file=.env
kubectl apply -f k8s-deployment.yaml
```

### Using systemd

```bash
sudo cp systemd/telegram-sound-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable telegram-sound-bot
sudo systemctl start telegram-sound-bot
```

## API Integration

### Get all sounds

```python
async with Session() as s:
    result = await s.execute(Sound.__table__.select())
    sounds = result.fetchall()
```

### Search sounds

```python
async with Session() as s:
    result = await s.execute(
        Sound.__table__.select().where(
            Sound.keyword.contains("search_term")
        )
    )
```

## Logging

Logs are written to `logs/` directory in container and current directory locally.

```bash
# View recent logs
tail -f logs/bot.log

# View errors only
grep ERROR logs/bot.log
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

MIT License - see LICENSE file for details

## Support

- 📖 [aiogram Documentation](https://docs.aiogram.dev/)
- 🚀 [Telegram Bot API](https://core.telegram.org/bots/api)
- 🐘 [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

## Author

**Mental98971** - [GitHub](https://github.com/Mental98971)

---

**Version**: 1.0.0  
**Last Updated**: 2026-05-12  
**Python**: 3.10+  
**aiogram**: 3.2.0+  
**SQLAlchemy**: 2.0.23+
