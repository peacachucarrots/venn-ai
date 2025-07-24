from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_migrate import Migrate
migrate = Migrate()

def init_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)