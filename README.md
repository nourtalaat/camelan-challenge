# Camelan

You'll find that there are 2 folders present here, one for each challenge, I'll start with challenge #1.
## Challenge #1
For this challenge I'll use the following:

* REST APIs: Flask/Python
* Authentication and authorization: Auth0 + Python integration
* Data warehouse and retrieval: Postgres DB + SQLAlchemy ORM

In the `challenge1` folder you'll find 7 files as follows:

1. .env: used to store environment variables
2. api.py: contains the APIs logic and functionality
3. auth.py: contains authentication/authorization logic and functinality
4. models.py: contains ORM declarations and functionality
5. test.db: **Postgres** DB backup containing data required to run the tests
6. test_cases-postman-collection.json: **Postman** collection of test cases
7. requirements.txt: **Python** dependencies used

### Endpoints
By default the server will run on `http://localhost:5000`, so that'll be the base URL.

The program serves 2 endpoints:

1. /pet/`id`/bid:
    * Description: allows authorized users to place bids on pet (provided the pet's ID)
    * Allowed methods: POST
    * Authorization: JWT Bearer token
    * Body type: JSON
    * Body structure:
        ```json
        {
            "amount": int
        }
    * Output structure:
        ```json
        {
            "bid": {
                        "id": int,
                        "user": str,
                        "pet_id": int,
                        "amount": int
                   }
        }
2. /pet/`id`/listBids:
    * Description: allows the pet owner to list the bids placed on their pet.
    * Allowed methods: GET
    * Authorization: JWT Bearer token
    * Body type: None
    * Output structure:
        ```json
        {
            "bids": [
                        {
                            "id": int,
                            "user": str,
                            "pet_id": int,
                            "amount": int
                        },
                        {
                            "id": int,
                            "user": str,
                            "pet_id": int,
                            "amount": int
                        },
                        ...
                    ]
        }

### Setup
In order to run the program and test it correctly, you'll need to perform the following steps:

1. Make sure you have Postgres, Python, and Postman installed on your current machine.
2. Install all Python requirements by running `pip install -r requirements.txt` in the folder's directory.
3. Creating an empty Postgres DB (the default name is 'camelan' and it's defined as an environment variable in the .env file) e.g. via psql: `psql -U postgres` and providing the password when prompted then running `CREATE DATABASE camelan;`.
4. Import the Postgres DB backup, e.g. via psql: `psql -U postgres camelan < test.db` and providing the password when prompted.
5. Import the Postman collection.

### Running the server
Simply run the api.py file via `python api.py` from the command line.

### Tests
The predefined tests cover a number of cases:

* /pet/`id`/bid:
    1. Not authenticated: the user is not authenticated (brearer token not provided or invalid).
        
        * Expected code: 401
    2. Not authorized: the user is not allowed to place a bid.
        
        * Expected code: 403
    3. Malformed post request: the user provided a malformed post request.
        
        * Expected code: 400
    4. Success: the user is authenticated and authorized and has provided a valid request.

        * Expected code: 200
    5. Duplicate bid: the user is authenticated and authorized but is attempting to bid on the same pet twice.

        * Expected code: 409

* /pet/`id`/listBids:
    1. Not authenticated: the user is not authenticated (brearer token not provided or invalid).
        
        * Expected code: 401
    2. Not pet owner: the user is authenticated but is not the pet's owner

        * Expected code: 403
    3. Success: the user is authenticated and is the pet's owner

        * Expected code: 200


### Running the tests
In postman:

1. Click 'Import' (top left section).
2. Select 'Upload Files' and choose the file named `test_cases-postman-collection.json`.
3. Click 'Import' and the collection will be imported.
4. Click 'Runner' (top left section).
5. Select the collection from the left section.
6. Click 'Start camelan-challenge'.
7. Wait for the tests to run then inspect the results.

Note #1: Please note that if you run the tests multiple times 2 of the tests will fail (that is due to the duplicate bids check), in order to be able to run the tests correctly again, kindly log into Postgres (e.g. via psql: `psql -U postgres camelan` and enter the password when prompted then run the following SQL query `delete from bids;` to remove previous bids).

Note #2: For ease of use I have already included the JWT (tokens) in the test cases, they will expire at 6:45 PM on the 18th of May 2021 EET (Cairo time); should you want to run the tests after that deadline, please use [the following URL](https://dev-xjvy32fs.eu.auth0.com/authorize?audience=camelan_challenge&response_type=token&client_id=PfVrgzsztlDdI8ejsFYQBcAXSuYHRqDJ&redirect_uri=http://localhost:5000/) to generate new tokens, for the purpose of ease of use you could also use the following credentials to generate the new tokens:

* notbidder@email.com:123456aA (User without the 'place:bid' permission).
* bidder@email.com:123456aA (User that has the 'place:bid' permission).
* petowner@email.com:123456aA (Owner of pet with id #1 -in the provided database backup-).

___

## Challenge #2
This challenge is solved in Python

In the `challenge2` folder you'll find 3 files as follows:
1. challenge2.py: the file containing the logic and functionality
2. challenge2_test.py: the file loads and performs a number of tests
3. challenge2_test_cases.json: the file contains the test cases in JSON

### Setup
You need to have Python installed on your current machine.

### Running the program
You can enter cases manually by running the challenge2.py file via `python challenge2.py` and entering the requested data.

### Tests
The predefined tests cover a number of cases:
1. Baseline case
2. No bidders
3. Duplicate bid amounts by different bidders
4. Number of items > number of bidders
5. No items are up for auction
6. One of the bidders is bidding a negative amount

The format and expected outputs for these test cases can be found in the `challenge2_test_cases.json` file.

### Running the tests
You can run the predefined test cases by running the challenge2_test.py file via `python challenge2_test.py`

Should you have any questions or run into any difficulties while running and testing the implementations, please reach out to me.