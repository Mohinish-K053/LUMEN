from flask import Flask
from flask_cors import CORS
from config import Config
from models import db
from routes.auth import auth_bp
from routes.study import study_bp
from routes.analytics import analytics_bp

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(study_bp, url_prefix="/api")
app.register_blueprint(analytics_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)


    print(app.url_map)

