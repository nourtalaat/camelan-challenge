# All code is compliant with PEP8 style guidelines

'''I will be using the Auth0 service for authentication and authorization'''

import json
import os
from flask import request
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from models import Pet
from dotenv import load_dotenv

''' I do realize that saving both DB and auth env variables in the same file
and loading it in 2 different places is not a good practice, but I didn't
want to go overboard for a technical challenge'''

load_dotenv()

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
ALGORITHMS = ['RS256']
API_AUDIENCE = os.getenv('API_AUDIENCE')


class AuthError(Exception):
    '''Definition of the AuthError Exception'''

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    '''Fetches and validates the "Authorization" header in the request'''
    auth = request.headers.get('Authorization')
    if not auth:
        raise AuthError("No authorization header", 401)
    authParts = auth.split()
    if len(authParts) == 2 and authParts[0] == "Bearer":
        return authParts[1]
    raise AuthError("Malformed authorization header", 400)


def check_permissions(permission, payload):
    '''Validates JWT permissions'''
    if 'permissions' not in payload:
        raise AuthError("Token has no 'permissions' key", 400)
    if permission:
        if permission not in payload['permissions']:
            raise AuthError("Token does not include the required permission",
                            403)
    return True


def verify_decode_jwt(token):
    '''Decodes and verifies the JWT'''
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            desc = 'Token expired.'
            raise AuthError({
                'code': 'token_expired',
                'description': desc
            }, 401)

        except jwt.JWTClaimsError:
            desc = 'Incorrect claims. Please, check the audience and issuer.'
            raise AuthError({
                'code': 'invalid_claims',
                'description': desc
            }, 401)
        except Exception:
            desc = 'Unable to parse authentication token.'
            raise AuthError({
                'code': 'invalid_header',
                'description': desc
            }, 400)
    desc = 'Unable to find the appropriate key.'
    raise AuthError({
        'code': 'invalid_header',
                'description': desc
    }, 400)


def requires_auth(permission=''):
    '''Performs all authentication and authorization steps,
    available as a wrapper'''
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(*args, **kwargs)
        return wrapper
    return requires_auth_decorator


def get_payload():
    token = get_token_auth_header()
    return verify_decode_jwt(token)


def check_ownership(pid, payload):
    '''Checks if user is the pet's owner'''
    try:
        pet = Pet.query.get(pid)
        oemail = pet.uemail
    except Exception:
        raise AuthError("Pet ID invalid", 400)
    # This weird dict key is required by Auth0's policy to prevent collisions
    # with reserved keys
    uemail = payload['https://localhost/email']
    if oemail != uemail:
        raise AuthError("User is not the pet's owner", 403)
    return True
