# All code is compliant with PEP8 style guidelines

'''I will be using Flask to facilitate the API calls'''

from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from auth import AuthError, requires_auth, get_payload, check_ownership
from models import User, Pet, Bid, setup_db

app = Flask(__name__)
setup_db(app)
CORS(app)


@app.route('/pet/<pid>/listBids', methods=['GET'])
@requires_auth()
def get_pet_bids(pid):
    '''Returns list of bids placed on a pet, accessible by pet owner only'''
    payload = get_payload()
    check_ownership(pid, payload)
    pet = Pet.query.get(pid)
    bids = [bid.format() for bid in pet.bids]
    return jsonify({
        'bids': bids
    })


@app.route('/pet/<pid>/bid', methods=['POST'])
@requires_auth(permission='place:bid')
def place_bid(pid):
    '''Places a bid ordered by a user'''
    try:
        pid = int(pid)
        data = request.json
        payload = get_payload()
        uemail = payload['https://localhost/email']
        # This part checks for duplicate bids
        cBids = Bid.query.filter_by(uemail=uemail).all()
        for bid in cBids:
            if bid.pid == pid:
                abort(409)
        # If malformed will raise an exception, returning a 400 (Bad Request)
        amount = int(data['amount'])
        newBid = Bid(uemail=uemail, amount=amount, pid=pid)
        newBid.insert()
        return jsonify({
            'bid': newBid.format()
        })
    except ValueError:
        abort(400)


@app.errorhandler(400)
def bad_request(error):
    '''Handles status code 400, bad request'''
    return jsonify({
                    "success": False,
                    "error": 400,
                    "message": "bad request"
                    }), 400


@app.errorhandler(401)
def unauthorized(error):
    '''Handles status code 401, unauthorized'''
    return jsonify({
                    "success": False,
                    "error": 401,
                    "message": "unauthorized"
                    }), 401


@app.errorhandler(403)
def forbidden(error):
    '''Handles status code 403, forbidden'''
    return jsonify({
                    "success": False,
                    "error": 403,
                    "message": "forbidden"
                    }), 403


@app.errorhandler(404)
def not_found(error):
    '''Handles status code 404, not found'''
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "not found"
                    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    '''Handles status code 405, method not allowed'''
    return jsonify({
                    "success": False,
                    "error": 405,
                    "message": "method not allowed"
                    }), 405


@app.errorhandler(409)
def duplicate(error):
    '''Handles status code 409, conflict (duplicate)'''
    return jsonify({
                    "success": False,
                    "error": 409,
                    "message": "duplicate bid"
                    }), 409


@app.errorhandler(AuthError)
def autherror(error):
    '''Handles exception 'AuthError', returns the specified status code'''
    return jsonify({
                    "success": False,
                    "error": error.status_code,
                    "message": error.error
                    }), error.status_code


# Configures and runs app if file is run directly
if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True)
