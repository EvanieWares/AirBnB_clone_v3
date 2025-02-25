#!/usr/bin/python3
# api/v1/views/amenities.py
"""Handles all default RESTFul API actions for Amenities"""
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """
    Retrieves a list of all the Amenity objects

    Returns:
        A list of all Amenity objects
    """
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route(
        '/amenities/<amenity_id>',
        methods=['GET'],
        strict_slashes=False
        )
def get_amenity(amenity_id):
    """
    Retrieves a Amenity object

    Args:
        amenity_id (str): The id of the Amenity object to retrieve

    Returns:
        An Amenity object, otherwise 404 error
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route(
        '/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes a Amenity object

    Args:
        amenity_id (str): The id of the Amenity object to delete
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    Creates a Amenity

    Returns:
        The new Amenity with code 201, otherwise error code 400
    """
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json()
    if 'name' not in data:
        abort(400, "Missing name")
    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route(
        '/amenities/<amenity_id>',
        methods=['PUT'],
        strict_slashes=False
        )
def update_amenity(amenity_id):
    """
    Updates a Amenity object

    Args:
        amenity_id (str): The id of the Amenity object to update

    Returns:
        The Amenity object with code 200, otherwise error code 404 or 400
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
