# proxy_server.py
import requests
from stem import Signal
from stem.control import Controller
from src.utils import log_event

def get_tor_session():
    session = requests.Session()
    session.proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    return session

def fetch_data_through_tor(url):
    try:
        session = get_tor_session()
        response = session.get(url, timeout=10)
        log_event(f"[TOR] Requested: {url}")
        return response.text
    except Exception as e:
        log_event(f"[TOR ERROR] {e}")
        return None

def fetch_data_direct(url):
    try:
        response = requests.get(url, timeout=10)
        log_event(f"[DIRECT] Requested: {url}")
        return response.text
    except Exception as e:
        log_event(f"[DIRECT ERROR] {e}")
        return None

def renew_tor_ip():
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password='your_tor_password')  # Replace with actual password
            controller.signal(Signal.NEWNYM)
            log_event("🔁 Tor IP renewed.")
    except Exception as e:
        log_event(f"[ERROR] Tor IP renew failed: {e}")

def proxy_request(url, use_tor=True):
    if use_tor:
        return fetch_data_through_tor(url)
    else:
        return fetch_data_direct(url)
