from flask import Flask
from lib.dog_repository import DogRepository
from lib.breed_repository import BreedRepository
import os
from flask import Flask, request, render_template, redirect, session, url_for
from lib.database_connection import get_flask_database_connection
from urllib.parse import unquote

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

@app.route("/searchbybreed/<path:breed>")  # Use <path:> to allow slashes in URL parameters
def search_by_breed_results(breed):
    connection = get_flask_database_connection(app)
    dog_repository = DogRepository(connection)

    # Decode the URL-encoded breed name
    decoded_breed = unquote(breed)
    print(f"Encoded breed: {breed}")  # Debugging: Print the received value
    print(f"Decoded breed: {decoded_breed}")  # Debugging: Print the decoded value

    # Find dogs by the decoded breed name
    dogs = dog_repository.find_by_breed(decoded_breed)
    return render_template("search_by_breed_results.html", dogs=dogs, breed=decoded_breed)

@app.route("/viewalldogs")  # Use <path:> to allow slashes in URL parameters
def view_all_dogs():
    connection = get_flask_database_connection(app)
    dog_repository = DogRepository(connection)
    dogs = dog_repository.all()
    return render_template("view_all_dogs.html", dogs=dogs)

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

@app.route("/searchbyname/<dog_name>")
def search_by_dog_name(dog_name):
    connection = get_flask_database_connection(app)
    dog_repository = DogRepository(connection)
    dogs = dog_repository.find_by_name(dog_name)
    return render_template("search_by_name_results.html", dogs=dogs, name=dog_name)

@app.route("/searchbydogid/<id>")
def search_by_dog_id(id):
    connection = get_flask_database_connection(app)
    dog_repository = DogRepository(connection)
    dogs = dog_repository.find(id)
    return render_template("search_by_name_results.html", dogs=dogs, id=id)

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

@app.route("/rarebreeds")
def display_rarely_seen_breeds():
    connection = get_flask_database_connection(app)
    dog_repository = DogRepository(connection)  
    breeds = dog_repository.get_rare_breeds()
    return render_template("rare_breeds.html", breeds=breeds)

@app.route("/rarepurebreeds")
def display_rarely_seen_purebreeds():
    connection = get_flask_database_connection(app)
    dog_repository = DogRepository(connection)  
    breeds = dog_repository.get_rare_purebreeds()
    return render_template("rare_purebreeds.html", breeds=breeds)

@app.route("/randomdog")
def display_random_dog():
    connection = get_flask_database_connection(app)
    dog_repository = DogRepository(connection)
    dogs = dog_repository.random_dog()
    return render_template("random_dog.html", dogs=dogs)

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)