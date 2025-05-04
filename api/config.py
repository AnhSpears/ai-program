import os

REDIS_URL       = os.getenv('REDIS_URL', 'redis://redis:6379/0')
OPENAI_API_KEY  = os.getenv('OPENAI_API_KEY')
ADMIN_API_KEY   = os.getenv('ADMIN_API_KEY')
BLOB_CONN_STR   = os.getenv('BLOB_CONN_STR')
