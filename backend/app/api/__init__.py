from backend.app.api.analytics.analytics import bp as analytics_bp
from .auth import bp as auth_bp
from .responses import bp as responses_bp
from .surveys import bp as surveys_bp
from .visitors import bp as visitors_bp

def init_api(app):
    app.register_blueprint(analytics_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(responses_bp)
    app.register_blueprint(surveys_bp)
    app.register_blueprint(visitors_bp)