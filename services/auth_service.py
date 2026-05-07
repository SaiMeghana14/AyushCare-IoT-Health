import bcrypt
import json
import os

USERS_FILE = "users.json"


def hash_password(password):

    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


def verify_password(password, hashed):

    return bcrypt.checkpw(
        password.encode(),
        hashed.encode()
    )


def load_users():

    if os.path.exists(USERS_FILE):

        with open(USERS_FILE, "r") as f:
            return json.load(f)

    return {}


def save_users(users):

    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)
