from flask import Flask

app = Flask(__name__)

@app.route("/")
def homepage_welcome():
    return "<p>Welcome to The Dogist! What would you like to do?</p>"

@app.route("/leaderboard")
def leaderboard():
    return "<p>Welcome to the dogist leaderboard!</p>"