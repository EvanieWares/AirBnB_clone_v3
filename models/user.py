#!/usr/bin/python3
""" holds class User"""
import hashlib
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user", cascade='delete')
        reviews = relationship("Review", backref="user", cascade='delete')
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        if kwargs:
            password = kwargs.pop('password', None)
            if password is not None:
                User.__set_password(password)
        super().__init__(*args, **kwargs)
    
    def __set_password(self, pwd):
        """Encrypts password using MD5"""
        hash = hashlib.md5()
        hash.update(pwd.encode('utf-8'))
        secure_password = hash.hexdigest()
        setattr(self, "password", secure_password)
