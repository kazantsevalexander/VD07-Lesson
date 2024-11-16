from app import db, app
from app.models import User

with app.app_context():  # Используем app_context вместо app_content
    db.create_all()
