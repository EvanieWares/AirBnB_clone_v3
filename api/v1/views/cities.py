#!/usr/bin/python3
# api/v1/views/cities.py
"""Handles all default RESTFul API actions for States"""
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views


@app_views.route(
        '/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """
    Retrieves a list of all City objects of a State

    Returns:
        A list of all City objects
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = state.cities
    return jsonify([city.to_dict() for city in cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a City object

    Args:
        city_id (str): The id of the City object to retrieve

    Returns:
        A City object, otherwise 404 error
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route(
        '/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a City object

    Args:
        city_id (str): The id of the City object to delete
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    del city
    return jsonify({}), 200


@app_views.route(
        '/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """
    Creates a City

    Returns:
        The new City with code 201, otherwise error code 404 or 400
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json()
    if 'name' not in data:
        abort(400, "Missing name")
    new_city = City(**data)
    new_city.state_id = state_id
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    Updates a City object

    Args:
        city_id (str): The id of the City object to update

    Returns:
        The City object with code 200, otherwise error code 404 or 400
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
