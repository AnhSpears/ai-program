from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def init_limiter(app):
    """
    Khởi tạo Flask-Limiter với:
      - giới hạn mặc định 100 req/phút/user
      - key dựa trên IP (hoặc bạn có thể đổi sang session/user-id)
    """
    return Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["100 per minute"]
    )
