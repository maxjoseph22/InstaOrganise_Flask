from flask import Flask
from lib.dog_repository import DogRepository
from lib.breed_repository import BreedRepository
import os
from flask import Flask, request, render_template, redirect, session
from lib.database_connection import get_flask_database_connection

app = Flask(__name__)

@app.route("/")
def homepage_welcome():
    return """
    <h1>Welcome to The Dogist!</h1>
    <p>What would you like to do?</p>
    <ul>
        <li><a href="/breedleaderboard">View Breed Leaderboard</a></li>
        <li><a href="/nameleaderboard">View Name Leaderboard</a></li>
        <li><a href="/likesleaderboard">View Likes Leaderboard</a></li>
        <li><a href="/breeds">View All Breeds</a></li>
        <li><a href="/neverseen">View Never Seen Breeds</a></li>
        <li><a href="/randomdog">View a Random Dog</a></li>
    </ul>
    """

@app.route("/breedleaderboard")
def breed_leaderboard():
    connection = get_flask_database_connection(app)
    dog_repository = DogRepository(connection)
    return dog_repository.get_breed_popularity()

@app.route("/nameleaderboard")
def name_leaderboard():
    connection = get_flask_database_connection(app)
    dog_repository = DogRepository(connection)
    return dog_repository.get_name_popularity()

@app.route("/likesleaderboard")
def likes_leaderboard():
    connection = get_flask_database_connection(app)
    dog_repository = DogRepository(connection)
    return dog_repository.get_likes_popularity()

@app.route("/dog/<dog_breed>")
def search_by_breed(dog_breed):
    connection = get_flask_database_connection(app)
    dog_repository = DogRepository(connection)
    return dog_repository.find_by_breed(dog_breed)

# THIS ISN'T WORKING AS EXPECTED, NOT GETTING AN ERROR BUT THE SERVER ISN'T DISPLAYING THE DOGS WITH MATCHING NAMES. JUST BLANK
@app.route("/dog/<dog_name>")
def search_by_name(dog_name):
    connection = get_flask_database_connection(app)
    dog_repository = DogRepository(connection)
    return dog_repository.find_by_name(dog_name)

@app.route("/breeds")
def display_all_breeds():
    connection = get_flask_database_connection(app)
    breed_repository = BreedRepository(connection)
    return breed_repository.get_breed_alphabetically()
    
@app.route("/neverseen")
def display_never_seen_breeds():
    connection = get_flask_database_connection(app)
    breed_repository = BreedRepository(connection)  
    return breed_repository.all_zeros()

@app.route("/randomdog")
def display_random_dog():
    connection = get_flask_database_connection(app)
    dog_repository = DogRepository(connection)
    return dog_repository.random_dog()

@app.route("/dog")
def dog():
    return "<p>Welcome to the dog page!</p>"

@app.route("/dog/<dog_id>")
def individual_dog(dog_id):
    return "Welcome to the specific dog page for dog " + str(dog_id)

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)