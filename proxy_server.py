import socket

def start_proxy():
    # Proxy server ke liye socket setup
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8080))  # Port 8080 pe bind ho raha hai
    server_socket.listen(5)
    print("Proxy server running on port 8080...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} established.")
        
        # Handle the request and respond accordingly
        client_socket.close()

if __name__ == "__main__":
    start_proxy()
