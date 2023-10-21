#!/usr/bin/python3
""" script that starts a Flask web application """

from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__, template_folder="templates")
file = "9-states.html"


@app.route("/states", strict_slashes=False)
def states():
    """ """
    states = storage.all(State)
    states = dict(sorted(states.items(), key=lambda item: item[1].name))
    return render_template(file, not_found=False, data=states, id=None)


@app.route("/states/<id>", strict_slashes=False)
def states_id(id):
    """ """
    state = storage.search(State, id=id)
    if state is None:
        return render_template(file, not_found=True, data=states)
    c = storage.all(City)
    cities = {}
    for key, city in c.items():
        if state.id == city.state_id:
            cities[key] = city
    cities = dict(sorted(cities.items(), key=lambda item: item[1].name))
    return render_template(file, name=state.name, not_found=False,
                           data=cities, id=1)


@app.teardown_appcontext
def teardown(error):
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
