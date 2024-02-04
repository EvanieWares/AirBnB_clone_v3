#!/usr/bin/python3
# api/v1/views/places.py
"""Handles all default RESTFul API actions for Places"""
from flask import jsonify, abort, request
from models.city import City
from models.place import Place
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route(
        '/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """
    Retrieves a list of all Place objects of a City

    Returns:
        A list of all Place objects
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    return jsonify([place.to_dict() for place in places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a Place object

    Args:
        place_id (str): The id of the Place object to retrieve

    Returns:
        A Place object, otherwise 404 error
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
        '/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a Place object

    Args:
        place_id (str): The id of the Place object to delete
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    del place
    return jsonify({}), 200


@app_views.route(
        '/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """
    Creates a Place

    Returns:
        The new Place with code 201, otherwise error code 404 or 400
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, "Missing user_id")
    else:
        user_id = data.get('user_id')
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
    if 'name' not in data:
        abort(400, "Missing name")
    new_place = Place(**data)
    new_place.user_id = user_id
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place object

    Args:
        place_id (str): The id of the Place object to update

    Returns:
        The Place object with code 200, otherwise error code 404 or 400
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'city_id', 'user_id']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
