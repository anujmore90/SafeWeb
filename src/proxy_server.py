# proxy_server.py
import socket
import threading

def handle_client(client_socket):
    request = client_socket.recv(4096)
    print(f"[REQUEST] {request.decode(errors='ignore')}")
    client_socket.close()

def start_proxy(host='127.0.0.1', port=8888):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[LISTENING] Proxy server running on {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[NEW CONNECTION] {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_proxy()
