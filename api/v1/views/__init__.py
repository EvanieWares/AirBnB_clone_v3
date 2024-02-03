#!/usr/bin/python3
# api/vi/views/__init__.py
"""Creates app_views blueprint"""
from flask import Blueprint
from api.v1.views.index import *

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
