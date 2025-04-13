import requests
import stem
from stem.control import Controller

def get_current_ip():
    try:
        response = requests.get("http://httpbin.org/ip", timeout=5)
        return response.json()['origin']
    except Exception as e:
        return f"Error: {e}"

def set_tor_proxy():
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    return proxies

def request_new_tor_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password='your_tor_password')  # Replace with your password
        controller.signal(stem.Signal.NEWNYM)

if __name__ == "__main__":
    print("🔍 Original IP:", get_current_ip())

    proxies = set_tor_proxy()

    # Use Tor network
    try:
        response = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=10)
        print("🕵️ IP via Tor:", response.json()['origin'])
    except Exception as e:
        print("❌ Failed using Tor:", e)
