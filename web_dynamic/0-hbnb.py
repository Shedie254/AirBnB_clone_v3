#!/usr/bin/python3
""" Starts a Flask web app """
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from os import environ
from flask import Flask, render_template
import uuid

app = Flask(__name__)

@app.teardown_appcontext
def close_db(error):
    """ Closes the current SQLAlchemy Session """
    storage.close()

@app.route('/0-hbnb/', strict_slashes=False)
def hbnb():
    """ Displays HBNB data """
    # Retrieve states sorted by name
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)

    # Group states with their cities sorted by name
    st_ct = []
    for state in states:
        st_ct.append([state, sorted(state.cities, key=lambda k: k.name)])

    # Retrieve amenities and places sorted by name
    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda k: k.name)

    places = storage.all(Place).values()
    places = sorted(places, key=lambda k: k.name)

    # Generate a unique cache ID
    cache_id = uuid.uuid4()

    return render_template('0-hbnb.html',
                           states=st_ct,
                           amenities=amenities,
                           places=places,
                           cache_id=cache_id)

if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5001)

