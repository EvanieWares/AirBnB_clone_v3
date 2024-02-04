#!/usr/bin/python3
# api/v1/views/users.py
"""Handles all default RESTFul API actions for Users"""
from flask import jsonify, abort, request
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieves a list of all the User objects

    Returns:
        A list of all User objects
    """
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route(
        '/users/<user_id>',
        methods=['GET'],
        strict_slashes=False
        )
def get_user(user_id):
    """
    Retrieves a User object

    Args:
        user_id (str): The id of the User object to retrieve

    Returns:
        An User object, otherwise 404 error
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route(
        '/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a User object

    Args:
        user_id (str): The id of the User object to delete
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Creates a User

    Returns:
        The new User with code 201, otherwise error code 400
    """
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json()
    if 'email' not in data:
        abort(400, "Missing email")
    if 'password' not in data:
        abort(400, "Missing password")
    new_amenity = User(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route(
        '/users/<user_id>',
        methods=['PUT'],
        strict_slashes=False
        )
def update_user(user_id):
    """
    Updates a User object

    Args:
        user_id (str): The id of the User object to update

    Returns:
        The User object with code 200, otherwise error code 404 or 400
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
