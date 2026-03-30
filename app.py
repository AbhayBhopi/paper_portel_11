from flask import Flask
from config import Config
from models import db, init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Register blueprints
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.teacher import teacher_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(teacher_bp, url_prefix='/teacher')

    return app


app = create_app()

if __name__ == '__main__':
    init_db(app)
    app.run(debug=True)