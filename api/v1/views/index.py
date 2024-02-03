#!/usr/bin/python3
# api/v1/views/index.py
"""Creates views routes"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """Returns a JSON status 'OK'"""
    return jsonify({"status": "OK"})
