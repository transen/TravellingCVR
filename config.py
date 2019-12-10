# Secret keys, API-keys and everything else important and secret goes here

#: The secret key is needed to keep the client-side sessions secure on the flask-app
secret_app_key = b'\xcb<\xdbEV\x8b\x04\x9dE\xac\xca\x18\x8b\xaa~\xbc'

#: API-key for MapQuest API
api_mapkey = 'zI2StNX9E0KnuNbN6h9XU6SNoF6n7Q9B'

#: The HTTP-header sent to the CVR-API
cvr_api_header = 'test_forsoeg'

#: Username for the external MongoDB
mongo_user = 'cvrapi_user'

#: Password for the external MongoDB
mongo_passw = 'KpPus2ImqATaomW1'

#: The client-string to access the external MongoDB
mongoclientstring = 'mongodb+srv://cvrapi_user:KpPus2ImqATaomW1@cvrdataapi-7bhwg.gcp.mongodb.net/travellingcvr' \
                    '?retryWrites=true&w=majority'
