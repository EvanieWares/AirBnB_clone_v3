#!/usr/bin/python3
# api/v1/views/places_amenities.py
"""
Handles all default RESTFul API actions for Place objects and Amenity objects
"""
from flask import jsonify, abort, request
from models.place import Place
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from os import getenv
STORAGE_TYPE = getenv('HBNB_TYPE_STORAGE')


@app_views.route(
        '/places/<place_id>/amenities',
        methods=['GET'],
        strict_slashes=False
        )
def places_amenities(place_id):
    """
    Retrieves the list of all Amenity objects of a Place

    Args:
        place_id (str): The id of the place to retrieve amenities from

    Returns:
        List of all Amenity objects of a Place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if STORAGE_TYPE == 'db':
        amenities = place.amenities
    else:
        amenities = place.amenity_ids
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=['DELETE'],
        strict_slashes=False
        )
def delete_place_amenity(place_id, amenity_id):
    """
    Deletes a Amenity object to a Place

    Args:
        place_id (str): The id of the place to delete amenity from
        amenity_id (str): The id of the amenity to delete

    Returns:
        An empty dictionary with status code 200, otherwise error 404
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if STORAGE_TYPE == 'db':
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids
    if amenity not in place_amenities:
        abort(404)
    place_amenities.remove(amenity)
    place.save()
    return jsonify({}), 200


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=['POST'],
        strict_slashes=False
        )
def link_place_amenity(place_id, amenity_id):
    """
    Link a Amenity object to a Place

    Args:
        place_id (str): The id of the place to link with the amenity
        amenity_id (str): The id of the amenity to link with the place

    Returns:
        The Amenity with status code 201, otherwise error 200 or 404
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if STORAGE_TYPE == 'db':
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids
    if amenity in place_amenities:
        return jsonify(amenity.to_dict()), 200
    place_amenities.append(amenity)
    place.save()
    return jsonify(amenity.to_dict()), 201
