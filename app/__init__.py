from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('../config.py')

from . import views  # noqa: E402, F401
from app.posts import post_bp  # noqa: E402, F401
from .users import user_bp  # noqa: E402, F401
app.register_blueprint(post_bp)
app.register_blueprint(user_bp)