from flask import Flask
from lib.dog_repository import DogRepository
from lib.breed_repository import BreedRepository
import os
from flask import Flask, request, render_template, redirect, session, url_for
from lib.database_connection import get_flask_database_connection

app = Flask(__name__)

@app.route("/")
def homepage_welcome():
    return render_template("homepage.html")

@app.route("/breedleaderboard")
def breed_leaderboard():
    connection = get_flask_database_connection(app)
    dog_repository = DogRepository(connection)
    breeds = dog_repository.get_breed_popularity()
    return render_template("breed_leaderboard.html", breeds=breeds)

@app.route("/nameleaderboard")
def name_leaderboard():
    connection = get_flask_database_connection(app)
    dog_repository = DogRepository(connection)
    names = dog_repository.get_name_popularity()
    return render_template("name_leaderboard.html", names=names)

@app.route("/likesleaderboard")
def likes_leaderboard():
    connection = get_flask_database_connection(app)
    dog_repository = DogRepository(connection)
    likes = dog_repository.get_likes_popularity()
    return render_template("likes_leaderboard.html", likes=likes)

@app.route("/searchbybreed", methods=["POST", "GET"])
def search_by_breed():
    if request.method == 'POST':
        breed = request.form.get('breed')  # Safely fetch the form data
        if not breed:
            return render_template("search_by_breed.html", error="Please enter a breed.")

        connection = get_flask_database_connection(app)
        dog_repository = DogRepository(connection)
        dogs = dog_repository.find_by_breed(breed)
        return render_template("search_by_breed_results.html", dogs=dogs, breed=breed)

    return render_template("search_by_breed.html")

# @app.route("/searchbybreed/<breed>")
# def search_by_breed_results(breed):
#     connection = get_flask_database_connection(app)
#     dog_repository = DogRepository(connection)
#     dogs = dog_repository.find_by_breed(breed)
#     return render_template("search_by_breed_results.html", dogs=dogs, breed=breed)

@app.route("/searchbyname", methods=["POST", "GET"])
def search_by_name():
    if request.method == 'POST':
        name = request.form.get('name')  # Safely fetch the form data
        if not name:
            return render_template("search_by_name.html", error="Please enter a name.")

        connection = get_flask_database_connection(app)
        dog_repository = DogRepository(connection)
        dogs = dog_repository.find_by_name(name)
        return render_template("search_by_name_results.html", dogs=dogs, name=name)

    return render_template("search_by_name.html")

# @app.route("/dog/<dog_name>")
# def search_by_dog_name(dog_name):
#     connection = get_flask_database_connection(app)
#     dog_repository = DogRepository(connection)
#     return dog_repository.find_by_name(dog_name)

@app.route("/breeds")
def display_all_breeds():
    connection = get_flask_database_connection(app)
    breed_repository = BreedRepository(connection)
    breeds = breed_repository.get_breed_alphabetically()
    return render_template("alphabetical_breeds.html", breeds=breeds)
        
@app.route("/neverseen")
def display_never_seen_breeds():
    connection = get_flask_database_connection(app)
    breed_repository = BreedRepository(connection)  
    breeds = breed_repository.all_zeros()
    return render_template("never_seen_breeds.html", breeds=breeds)

@app.route("/randomdog")
def display_random_dog():
    connection = get_flask_database_connection(app)
    dog_repository = DogRepository(connection)
    dogs = dog_repository.random_dog()
    return render_template("random_dog.html", dogs=dogs)

@app.route("/dog")
def dog():
    return "<p>Welcome to the dog page!</p>"

@app.route("/dog/<dog_id>")
def individual_dog(dog_id):
    return "Welcome to the specific dog page for dog " + str(dog_id)

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)