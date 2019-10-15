import requests
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from config import *

# Slår CVR-registret op efter firma-navn og returnerer dict over virksomheden
def cvrapinavn(navn, land='dk'):
    """Looks up the the CVR-register of a company name and returns a dictionary from the API


#asiduagsidugas






# Hi there
