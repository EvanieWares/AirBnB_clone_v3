#!/usr/bin/python3
# api/v1/views/places.py
"""Handles all default RESTFul API actions for Places"""
from flask import jsonify, abort, request
from models.city import City
from models.place import Place
from models.user import User
from models import storage
from api.v1.views import app_views
from os import getenv
STORAGE_TYPE = getenv('HBNB_TYPE_STORAGE', "fs")


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


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """
    Retrieves all Place objects depending of the JSON in the body of the
    request
    """
    all_places = list(place for place in storage.all('Place').values())
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    states = req_json.get('states')
    if states and len(states) > 0:
        all_cities = storage.all('City')
        state_cities = set([city.id for city in all_cities.values()
                            if city.state_id in states])
    else:
        state_cities = set()
    cities = req_json.get('cities')
    if cities and len(cities) > 0:
        cities = set([
            c_id for c_id in cities if storage.get('City', c_id)])
        state_cities = state_cities.union(cities)
    amenities = req_json.get('amenities')
    if len(state_cities) > 0:
        all_places = [place for place in all_places if place.city_id in state_cities]
    elif amenities is None or len(amenities) == 0:
        result = [place.to_json() for place in all_places]
        return jsonify(result)
    places_amenities = []
    if amenities and len(amenities) > 0:
        amenities = set([
            amenity_id for amenity_id in amenities
            if storage.get('Amenity', amenity_id)])
        for place in all_places:
            p_amenities = None
            if STORAGE_TYPE == 'db' and place.amenities:
                p_amenities = [amenity.id for amenity in place.amenities]
            elif len(place.amenities) > 0:
                p_amenities = place.amenities
            if p_amenities and all([a in p_amenities for a in amenities]):
                places_amenities.append(place)
    else:
        places_amenities = all_places
    result = [place.to_json() for place in places_amenities]
    return jsonify(result)
