import csv
import random
import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, exc
from app import *

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "may.db")) 

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)  # соединяем наш код с нашей бд


@app.route('/', methods=['GET'])
def fff():
	return render_template ('index.html')


def index():
	f = open("flights.csv")
	reader = csv.reader(f)  # взял файл csv оттуда все линии текста сохранил в буфер и сохранили это в reader
	for origin, destination, duration in reader:
		flight = Flight(origin=origin, destination=destination, duration=duration)
		fs = Flight.query.all()
		if flight.origin and flight.destination and flight.duration in fs:
			print("Error, this flights in db, yet")
		else:
			db.session.add(flight)  # записать записи в бд  
			print(f"Added flight from {origin} to {destination} lasting {duration} minutes")
			db.session.commit()  # сохранить наши записи в бд


def show():
	#flights = Flight.query.filter(and_(Flight.origin=="Masdoas", Flight.id == 10)).all()  # делаем запрос(query) к таблице Flight, показать все( all() ) 
	flights = Flight.query.all()
	for flight in flights:
		print(f"{flight.origin} to {flight.destination}, {flight.duration} minutes")
	passengers = Passenger.query.all()
	for i in passengers:
		print(f"Name: {i.name}, flight_id is: {i.flight_id}, id: {i.id}")

@app.route('/nus', methods=["POST"])
def show_json():
	n = request.form.get('index_id')
	
	try:
		flight = Flight.query.get(n)
		passengers = Passenger.query.filter_by(flight_id=n).all()
		names = []

		for passenger in passengers:
			names.append(passenger.name)

		return ( jsonify({
			"origin": flight.origin,
			"destination": flight.destination,
			"duration": flight.duration,
			"passengers": names
		}))
	except:
		return "Error, invalid flight number"


@app.route('/add_passenger', methods=['POST'])
def add_passenger():
	k = Flight.query.order_by(Flight.id.desc()).first()
	l = request.form.get("Name_passenger")
	n = Passenger(name=l, flight_id=random.randint(1, k.id))
	db.session.add(n)
	db.session.commit()
	return ( jsonify({
		"id": n.id,
		"name": n.name,
		"flight_id" : n.flight_id
		}))

def delete_passengers():
	n = int(input("Enter a passenger u want to delete: "))
	
	try:
		passenger = Passenger.query.get(n)
		db.session.delete(passenger)
		db.session.commit()

	except:
		print ("Error, there is nothing to delete")
	


def delete_flight():
	n = int(input("Number of flight u want to delete: "))
	#p = db.session.query(Flight.id).all()  # не работает если поставить Flight.query.(Flight.id)
	#print(p)			
	try:
		flight = Flight.query.get(n)
		db.session.delete(flight)
		db.session.commit()

	except :
		print("Error, there is nothing to delete")
	

if __name__=='__main__':
	with app.app_context():
		app.run(debug=True)
		#print("""
		#	Menu:
		#	|1.add a passenger
		#	|2.delete a passenger	
		#	|3.show all
		#	|4.show json object
		#	""")  
		#	 
		#index()
		#delete_flight()
		#delete_passengers()
		#add_passenger()
		#print()
		#show()
		#show_json()
		#print()
