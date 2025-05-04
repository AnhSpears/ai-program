import os

# OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# Git repo & updater
REPO_PATH       = os.path.dirname(os.path.abspath(__file__))
UPDATE_INTERVAL = int(os.getenv('UPDATE_INTERVAL', 3600))

# Redis & Rate-limit
REDIS_URL       = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
RATE_LIMIT      = os.getenv('RATE_LIMIT', '200/hour')

# Admin
ADMIN_API_KEY   = os.getenv('ADMIN_API_KEY')

# Discord
DISCORD_TOKEN   = os.getenv('DISCORD_TOKEN')
DISCORD_CHANNEL = os.getenv('DISCORD_CHANNEL')  # optional cụm channel ID

# Upload
UPLOAD_FOLDER   = os.getenv('UPLOAD_FOLDER', 'uploads')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

# Embedding
EMBED_DIM       = 1536

