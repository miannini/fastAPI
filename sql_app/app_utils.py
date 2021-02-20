# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 22:58:28 2021

@author: Marcelo
"""
from datetime import timedelta, datetime
from . import secrets
from jose import jwt
##########################
# to get a string like this run:
# openssl rand -hex 32
secret_key = secrets.secret_key
algorithm = secrets.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 720

def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def decode_access_token(*, data: str):
    to_decode = data
    return jwt.decode(to_decode, secret_key, algorithms=algorithm)