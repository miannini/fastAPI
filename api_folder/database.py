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

DB_USER = secrets.DB_USER
PASSWORD = secrets.PASSWORD
IP = secrets.IP
SCHEMA = secrets.SCHEMA

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://"+DB_USER+":"+PASSWORD+"@"+IP+SCHEMA

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()