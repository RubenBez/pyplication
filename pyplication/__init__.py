from flask import Flask

from ai import AI

_ai = None

def create_app():
    app = Flask(__name__)

    from . import routes
    app.register_blueprint(routes.bp)
    return app

def ai():
    global _ai
    if _ai == None:
        _ai = AI()
    return _ai