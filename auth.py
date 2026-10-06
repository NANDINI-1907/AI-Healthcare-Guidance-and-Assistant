import hashlib
import json
import os


USER_FILE = "users.json"


def hash_password(password):
    return hashlib.sha256(
        password.encode()
    ).hexdigest()


def load_users():

    if not os.path.exists(USER_FILE):
        return {}

    with open(USER_FILE, "r") as file:
        return json.load(file)


def save_users(users):

    with open(USER_FILE, "w") as file:
        json.dump(users, file, indent=4)


def register_user(name, email, password):

    users = load_users()

    email = email.lower().strip()

    if email in users:
        return False, "An account with this email already exists."

    users[email] = {
        "name": name,
        "password": hash_password(password)
    }

    save_users(users)

    return True, "Account created successfully."


def login_user(email, password):

    users = load_users()

    email = email.lower().strip()

    if email not in users:
        return False, None

    if users[email]["password"] != hash_password(password):
        return False, None

    return True, users[email]["name"]