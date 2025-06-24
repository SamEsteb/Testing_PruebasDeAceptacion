from app import create_app
from DBManager import db
from database import models  

app = create_app()

with app.app_context():
    db.create_all()
    db.session.commit()
    print("Database created successfully.")
