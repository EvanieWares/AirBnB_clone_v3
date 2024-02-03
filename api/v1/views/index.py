#!/usr/bin/python3
# api/v1/views/index.py
"""Creates views routes"""
from flask import jsonify
from models import *
from models import storage
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """Returns a JSON status 'OK'"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """Returns a JSON status 'OK'"""
    amenities = storage.count('Amenity')
    cities = storage.count('City')
    places = storage.count('Place')
    reviews = storage.count('Review')
    states = storage.count('State')
    users = storage.count('User')
    return jsonify({
        "amenities": amenities,
        "cities": cities,
        "places": places,
        "reviews": reviews,
        "states": states,
        "users": users
        })
