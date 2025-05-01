from flask import Flask
from lib.dog_repository import DogRepository
from lib.breed_repository import BreedRepository
import os
from flask import Flask, request, render_template, redirect, session
from lib.database_connection import get_flask_database_connection

app = Flask(__name__)

@app.route("/")
def homepage_welcome():
    return "<p>Welcome to The Dogist! What would you like to do?</p>"

@app.route("/leaderboard")
def leaderboard():
    connection = get_flask_database_connection(app)
    dog_repository = DogRepository(connection)
    breed_repository = BreedRepository(connection)
    return "\n".join(dog_repository.get_breed_popularity())


@app.route("/dog")
def dog():
    return "<p>Welcome to the dog page!</p>"

@app.route("/dog/<dog_id>")
def individual_dog(dog_id):
    return "Welcome to the specific dog page for dog " + str(dog_id)

if __name__ == '__main__':
    app.run()