from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    kind = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(80), default="Other")
    transaction_date = db.Column(db.Date, default=date.today)
