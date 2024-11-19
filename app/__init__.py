from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('../config.py')

from . import views  # noqa: E402, F401
from app.posts import post_bp  # noqa: E402, F401
from .users import user_bp  # noqa: E402, F401
app.register_blueprint(post_bp)
app.register_blueprint(user_bp)

def create_app(config_name="config"):

    app = Flask(__name__)
    app.config.from_object(config_name)

    with app.app_context():
        from . import views

        from .posts import post_bp
        from .users import bp as user_bp
        app.register_blueprint(post_bp)
        app.register_blueprint(user_bp, url_prefix="/users")
        
    return app