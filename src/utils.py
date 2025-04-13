import logging
from hashlib import sha256

# Set up logging to capture events
logging.basicConfig(filename="app.log", level=logging.INFO)

# Log events to the log file
def log_event(event):
    logging.info(event)

# Function to generate a hashed token for user authentication
def generate_token(username, password):
    return sha256(f"{username}{password}".encode('utf-8')).hexdigest()

# Function to authenticate a user based on username, password, and stored token
def authenticate(username, password, stored_token):
    token = generate_token(username, password)
    if token == stored_token:
        log_event(f"User {username} authenticated successfully.")
        return True
    else:
        log_event(f"Authentication failed for user {username}.")
        return False
