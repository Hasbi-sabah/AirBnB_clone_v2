#!/usr/bin/python3
""" script that starts a Flask web application """

from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.user import User


app = Flask(__name__, template_folder="templates")
file = "100-hbnb.html"

@app.route("/hbnb", strict_slashes=False)
def hbnb_filters():
    """ """
    states = storage.all(State)
    states = dict(sorted(states.items(), key=lambda item: item[1].name))
    cities = storage.all(City)
    cities = dict(sorted(cities.items(), key=lambda item: item[1].name))
    amenities = storage.all(Amenity)
    amenities = dict(sorted(amenities.items(), key=lambda item: item[1].name))
    places = storage.all(Place)
    places = dict(sorted(places.items(), key=lambda item: item[1].name))
    users = storage.all(User)

    return render_template(file, states=states, cities=cities, amenities=amenities, places=places, users=users)


@app.teardown_appcontext
def teardown(error):
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
