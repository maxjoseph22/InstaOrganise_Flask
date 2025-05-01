from flask import Flask

app = Flask(__name__)

@app.route("/")
def homepage_welcome():
    return "<p>Welcome to The Dogist! What would you like to do?</p>"

@app.route("/leaderboard")
def leaderboard():
    return "<p>Welcome to the dogist leaderboard!</p>"

@app.route("/dog")
def dog():
    return "<p>Welcome to the dog page!</p>"

@app.route("/dog/<dog_id>")
def individual_dog(dog_id):
    return "Welcome to the specific dog page for dog " + str(dog_id)

if __name__ == '__main__':
    app.run()