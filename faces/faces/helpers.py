import os
import requests
from flask import redirect, request
from pymongo import MongoClient

mongo_uri = os.environ.get('MONGODB_URI', 'mongodb://localhost/') + os.environ.get('MONGODB_DB', 'celso')

client = MongoClient(mongo_uri)

def get_connection():
    return client

def close_connection(client):
    client = None
