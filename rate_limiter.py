from time import time

failed_login_attempts = {}

def check_failed_attempts(ip_address):
    current_time = time()
    attempts = failed_login_attempts.get(ip_address, [])

    attempts = [attempt for attempt in attempts if current_time - attempt < 3600]
    failed_login_attempts[ip_address] = attempts

    if len(attempts) > 5:
        return False
    return True

def record_failed_attempt(ip_address):
    current_time = time()
    failed_login_attempts.setdefault(ip_address, []).append(current_time)
