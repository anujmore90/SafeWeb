import requests
from stem import Signal
from stem.control import Controller
import logging
from hashlib import sha256

# Set up logging to capture events
logging.basicConfig(filename="app.log", level=logging.INFO)

# Function to get a Tor session (for routing requests through Tor)
def get_tor_session():
    session = requests.Session()
    session.proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    return session

# Function to make requests through the Tor network
def fetch_data_through_tor(url):
    try:
        session = get_tor_session()
        response = session.get(url)
        log_event(f"Request made through Tor: {url}")
        return response.text
    except requests.exceptions.RequestException as e:
        log_event(f"Request failed through Tor: {e}")
        raise

# Function to renew the Tor IP address (used when we want to change the IP)
def renew_tor_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
        log_event("Tor IP address renewed.")

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

# Example function to demonstrate proxy server functionality
def proxy_request(url, use_tor=True):
    if use_tor:
        log_event(f"Fetching data through Tor for URL: {url}")
        return fetch_data_through_tor(url)
    else:
        try:
            log_event(f"Fetching data without Tor for URL: {url}")
            response = requests.get(url)
            return response.text
        except requests.exceptions.RequestException as e:
            log_event(f"Request failed without Tor: {e}")
            raise

# Testing the proxy server
if __name__ == "__main__":
    # Example of Tor request
    try:
        tor_url = "http://httpbin.org/ip"
        tor_response = proxy_request(tor_url, use_tor=True)
        print("Tor Response: ", tor_response)
    except Exception as e:
        print(f"Error occurred while fetching data through Tor: {e}")
    
    # Example of normal request (without Tor)
    try:
        normal_url = "http://httpbin.org/ip"
        normal_response = proxy_request(normal_url, use_tor=False)
        print("Normal Response: ", normal_response)
    except Exception as e:
        print(f"Error occurred while fetching data normally: {e}")

    # Example of user authentication
    username = "user1"
    password = "password123"
    stored_token = generate_token(username, password)

    # Try authenticating the user
    if authenticate(username, password, stored_token):
        print("User authenticated successfully.")
    else:
        print("Authentication failed.")
