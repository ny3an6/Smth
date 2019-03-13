from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Flight(db.Model):
	__tablename__ = "flights"
	id = db.Column(db.Integer, primary_key=True)
	origin = db.Column(db.String, nullable=True)
	destination = db.Column(db.String, nullable=True)
	duration = db.Column(db.Integer, nullable=True)


class Passenger(db.Model):
	__tablename__ = "passengers"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=True, unique=True)
	flight_id = db.Column(db.Integer, db.ForeignKey("flights.id"), nullable=False)

