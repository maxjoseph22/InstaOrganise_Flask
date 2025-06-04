from flask import Flask, g
from lib.dog_repository import DogRepository
from lib.breed_repository import BreedRepository
from lib.favourite_dog_repository import FavouriteDogRepository
import os
from flask import Flask, request, render_template, redirect, session, url_for
from lib.database_connection import get_flask_database_connection
from urllib.parse import unquote
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from psycopg import sql


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)

@app.before_request
def load_session_data():
    user = session.get("user")
    g.session_data = {
        "session": user if user else {},
        "pretty": json.dumps(user, indent=4) if user else "",
    }

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    # Extract token and user info
    token = oauth.auth0.authorize_access_token()
    session["user"] = token

    # Extract user info from Auth0
    auth0_user_id = token["userinfo"]["sub"]  # Example: auth0|12345
    email = token["userinfo"].get("email")    # Email may not always be present

    # Get database connection
    connection = get_flask_database_connection(app)

    # Check if user exists in the database
    user = connection.execute(
        "SELECT id FROM users WHERE auth0_id = %s",
        (auth0_user_id,)
    )

    if not user:  # User not found, insert a new user
        inserted_user = connection.execute(
            "INSERT INTO users (auth0_id, email) VALUES (%s, %s) RETURNING id",
            (auth0_user_id, email)
        )
        user_id = inserted_user[0]["id"]  # Fetch the new user ID
    else:
        user_id = user[0]["id"]  # Existing user ID

    # Store user ID in session
    session["user_id"] = user_id

    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("homepage_welcome", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route("/")
def homepage_welcome():
    return render_template("homepage.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

@app.route("/breedleaderboard")
def breed_leaderboard():
    connection = get_flask_database_connection(app)
    dog_repository = DogRepository(connection)
    breeds = dog_repository.get_breed_popularity()
    return render_template("breed_leaderboard.html", breeds=breeds, **g.session_data)

@app.route("/nameleaderboard")
def name_leaderboard():
    connection = get_flask_database_connection(app)
    dog_repository = DogRepository(connection)
    names = dog_repository.get_name_popularity()
    return render_template("name_leaderboard.html", names=names, **g.session_data)

@app.route("/likesleaderboard")
def likes_leaderboard():
    connection = get_flask_database_connection(app)
    dog_repository = DogRepository(connection)
    likes = dog_repository.get_likes_popularity()
    return render_template("likes_leaderboard.html", likes=likes, **g.session_data)

@app.route("/searchbybreed", methods=["POST", "GET"])
def search_by_breed():
    if request.method == 'POST':
        breed = request.form.get('breed')  # Safely fetch the form data
        if not breed:
            return render_template("search_by_breed.html", error="Please enter a breed.")

        connection = get_flask_database_connection(app)
        dog_repository = DogRepository(connection)
        dogs = dog_repository.find_by_breed(breed)
        return render_template("search_by_breed_results.html", dogs=dogs, breed=breed, **g.session_data)

    return render_template("search_by_breed.html", **g.session_data)

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
    return render_template("search_by_breed_results.html", dogs=dogs, breed=decoded_breed, **g.session_data)

@app.route("/viewalldogs")  # Use <path:> to allow slashes in URL parameters
def view_all_dogs():
    connection = get_flask_database_connection(app)
    dog_repository = DogRepository(connection)
    dogs = dog_repository.all()
    return render_template("view_all_dogs.html", dogs=dogs, **g.session_data)

@app.route("/searchbyname", methods=["POST", "GET"])
def search_by_name():
    if request.method == 'POST':
        name = request.form.get('name')  # Safely fetch the form data
        if not name:
            return render_template("search_by_name.html", error="Please enter a name.")

        connection = get_flask_database_connection(app)
        dog_repository = DogRepository(connection)
        dogs = dog_repository.find_by_name(name)
        return render_template("search_by_name_results.html", dogs=dogs, name=name, **g.session_data)

    return render_template("search_by_name.html", **g.session_data)

@app.route("/searchbyname/<dog_name>")
def search_by_dog_name(dog_name):
    connection = get_flask_database_connection(app)
    dog_repository = DogRepository(connection)
    dogs = dog_repository.find_by_name(dog_name)
    return render_template("search_by_name_results.html", dogs=dogs, name=dog_name, **g.session_data)

@app.route("/searchbydogid/<id>")
def search_by_dog_id(id):
    connection = get_flask_database_connection(app)
    dog_repository = DogRepository(connection)
    dogs = dog_repository.find(id)
    return render_template("search_by_name_results.html", dogs=dogs, id=id, **g.session_data)

@app.route("/breeds")
def display_all_breeds():
    connection = get_flask_database_connection(app)
    breed_repository = BreedRepository(connection)
    breeds = breed_repository.get_breed_alphabetically()
    return render_template("alphabetical_breeds.html", breeds=breeds, **g.session_data)
        
@app.route("/neverseen")
def display_never_seen_breeds():
    connection = get_flask_database_connection(app)
    breed_repository = BreedRepository(connection)  
    breeds = breed_repository.all_zeros()
    return render_template("never_seen_breeds.html", breeds=breeds, **g.session_data)

@app.route("/rarebreeds")
def display_rarely_seen_breeds():
    connection = get_flask_database_connection(app)
    dog_repository = DogRepository(connection)  
    breeds = dog_repository.get_rare_breeds()
    return render_template("rare_breeds.html", breeds=breeds, **g.session_data)

@app.route("/rarepurebreeds")
def display_rarely_seen_purebreeds():
    connection = get_flask_database_connection(app)
    dog_repository = DogRepository(connection)  
    breeds = dog_repository.get_rare_purebreeds()
    return render_template("rare_purebreeds.html", breeds=breeds, **g.session_data)

@app.route("/raremutts")
def display_rarely_seen_mutts():
    connection = get_flask_database_connection(app)
    dog_repository = DogRepository(connection) 
    breeds = dog_repository.get_loveable_mutts()
    return render_template("rare_mutts.html", breeds=breeds, **g.session_data)

@app.route("/randomdog", methods=["GET", "POST"])
def display_random_dog():
    connection = get_flask_database_connection(app)
    dog_repository = DogRepository(connection)

    if request.method == "POST":
        if "user" not in session:
            return {"success": False, "message": "Please log in to add favourites."}, 401
    
        auth0_user_dict = session["user"]  # Assume Auth0's "sub" is the user_id
        auth0_id = auth0_user_dict['userinfo']['sub']
        dog_id = request.json.get("dog_id")  # Use JSON to parse the request
    
        if not dog_id:
            return {"success": False, "message": "Dog ID is required"}, 400
    
        favourite_repository = FavouriteDogRepository(connection)
        favourite_repository.add_favourite_dog(auth0_id, dog_id)
        return {"success": True, "message": "Dog added to favourites!"}, 200

    # Handle GET requests
    dogs = dog_repository.random_dog()
    user_id = session["user"] if "user" in session else None
    return render_template("random_dog.html", dogs=dogs, user_id=user_id, **g.session_data)

@app.route("/favourites", methods=["GET", "POST"])
def get_favourites():
    connection = get_flask_database_connection(app)
    dog_repository = DogRepository(connection)
    favourite_dog_repository = FavouriteDogRepository(connection)

    if request.method == "GET":
        if "user" not in session:
            return {"success": False, "message": "User not logged in"}, 401

        auth0_user_dict = session["user"]  # Assume Auth0's "sub" is the user_id
        auth0_id = auth0_user_dict['userinfo']['sub']
        dog_ids = favourite_dog_repository.all(auth0_id)
        all_favourite_dog_ids = []
        for dog_id in dog_ids:
            dog = dog_id['dog_id']
            all_favourite_dog_ids.append(dog)
        all_dogs = []
        for id in all_favourite_dog_ids:
            dog = dog_repository.find_by_id(id)
            all_dogs.append(dog)
        return render_template("favourites.html", dogs=all_dogs, **g.session_data)

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)