from flask import Flask
from flask_session import Session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis
from utils.logger import setup_logging
from utils.auth import require_api_key
from utils.limiter import init_limiter
def create_app():
    app = Flask(__name__)
    limiter = init_limiter(app)
    app.config.from_pyfile('config.py')

    # Session (Redis)
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS'] = redis.from_url(app.config['REDIS_URL'])
    Session(app)

    # Rate limit
    limiter = Limiter(app, key_func=get_remote_address, default_limits=["100 per minute"])

    # Logging
    setup_logging(app)

    # Blueprints
    from routes.chat import chat_bp
    from routes.upload import upload_bp
    from routes.upgrade import upgrade_bp
    app.register_blueprint(chat_bp, url_prefix='/chat')
    app.register_blueprint(upload_bp, url_prefix='/upload')
    app.register_blueprint(upgrade_bp, url_prefix='/upgrade')

    @app.route('/health')
    def health():
        return {'status':'ok'}, 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
