# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 18:59:35 2020

@author: Marcelo
"""
from . import secrets
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql
from api_folder.encrypt import decrypt
import os

DB_USER = decrypt(str.encode(os.getenv('DB_USER')), secrets.key).decode()
PASSWORD = decrypt(str.encode(os.getenv('PASSWORD')), secrets.key).decode()
IP = os.getenv('IP_name')
SCHEMA = os.getenv('SCHEMA')

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://"+DB_USER+":"+PASSWORD+"@"+IP+"/"+SCHEMA

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()