import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

## -------------------------------------
## Utils
## -------------------------------------

AUTH0_DOMAIN = 'dev-j30osbgf.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'dev'
JWKS_URL = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'

# Gets JSON data from URL
# Source: https://www.datasciencelearner.com/how-to-get-json-data-from-url-in-python/ 
def get_json_data(url):
    operUrl = urlopen(url)
    if(operUrl.getcode() != 200):
        return False

    data = operUrl.read()
    jsonData = json.loads(data)
    return jsonData

## -------------------------------------
## Authorization 
## -------------------------------------

# Handles authentication errors to raise exceptions.
# Returns: dictionary with error message and description.
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

# Gets auth header.
# Returns: split_auth_header (string)
def get_token_auth_header():
    auth_header = request.headers.get('Authorization', None)

    if not auth_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header not found.'
        }, 401)

    split_auth_header = auth_header.split(' ')

    if len(split_auth_header) == 0:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Invalid token header.'
        }, 401)

    if split_auth_header[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Invalid token type.'
        }, 401)

    if not split_auth_header[1]:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Empty Bearer token value.'
        }, 401)

    return split_auth_header[1]

# Checks permission against the payload coming from Auth0.
# For more: verify_decode_jwt()
# Accepts: permission (string) and payload (dictionary).
def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_payload',
            'description': 'Invalid payload.'
        }, 422)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'forbidden',
            'description': 'Request is forbidden.'
        }, 403)
    
    return True

# Fetches JSON web key set from Auth0
# Accepts: token (string)
# Returns: rsa_key (dictionary)
# Link: https://auth0.com/docs/tokens/concepts/jwks 
def get_rsa_key(token):
    jwks_data = get_json_data(JWKS_URL)

    if not jwks_data:
        raise AuthError({
            'code': 'invalid_auth_api',
            'description': 'Invalid authorization API.'
        }, 422)

    jwt_headers = jwt.get_unverified_headers(token)
    if 'kid' not in jwt_headers:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Missing "kid" header.'
        }, 422)

    rsa_key = None
    for key in jwks_data['keys']:
        if key['kid'] != jwt_headers['kid']:
            continue
        rsa_key = {
            'kty': key['kty'],
            'kid': key['kid'],
            'use': key['use'],
            'n': key['n'],
            'e': key['e']
        }

    if not rsa_key:
        raise AuthError({
            'code': 'invalid_key',
            'description': 'Unable to find the appropriate key.'
        }, 401)

    return rsa_key

# Verification and decoding of JWT.
# Receives: token (string)
# Returns: payload (dictionary)
def verify_decode_jwt(token):
    rsa_key = get_rsa_key(token)

    try:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms = ALGORITHMS,
            audience = API_AUDIENCE,
            issuer = f'https://{AUTH0_DOMAIN}/'
        )
        return payload

    except jwt.ExpiredSignatureError:
        raise AuthError({
            'code': 'expired_token',
            'description': 'Token has expired.'
        }, 401)

    except Exception:
        raise AuthError({
            'code': 'invalid_token',
             'description': 'Token is invalid.'
        }, 422)

    except jwt.JWTClaimsError:
        raise AuthError({
            'code': 'invalid_decode',
            'description': 'Invalid decode configuration.'
        }, 422)

# Decorator to check permissions and authentication on endpoints.
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(*args, **kwargs)

        return wrapper
    return requires_auth_decorator