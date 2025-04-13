# utils.py

import logging
import os

# Set up logging
def setup_logging(log_file='app.log'):
    """
    Set up logging to log events to a file and to the console.
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    logging.info("Logging setup complete.")

# Read configuration from a file (e.g., for Tor or proxy settings)
def read_config(config_file='config.json'):
    """
    Reads the configuration file and returns the configuration as a dictionary.
    """
    import json
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            config = json.load(file)
            logging.info(f"Configuration loaded from {config_file}")
            return config
    else:
        logging.error(f"Configuration file {config_file} not found!")
        return None

# Handle errors by logging them
def handle_error(error_message):
    """
    Logs the error message and can be used to raise or return the error.
    """
    logging.error(f"Error occurred: {error_message}")
    raise Exception(error_message)  # You can choose to raise the error or just log it.

# Example function to validate a URL (you could use this in your proxy server)
def is_valid_url(url):
    """
    Check if a URL is valid.
    """
    import re
    pattern = r'^(https?://)?([a-zA-Z0-9_-]+\.)+[a-zA-Z]{2,6}(/[\w-]*)*$'
    if re.match(pattern, url):
        return True
    return False

# Example function to parse command-line arguments
def parse_arguments():
    """
    Parse command-line arguments for the app.
    """
    import argparse
    parser = argparse.ArgumentParser(description='SafeWeb Proxy Server')
    parser.add_argument('--config', help='Path to the configuration file', default='config.json')
    parser.add_argument('--log', help='Log file name', default='app.log')
    return parser.parse_args()
