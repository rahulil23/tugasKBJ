import socket

def send_request(app_id, app_type):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(("localhost", 8080))
        message = f"{app_id}:{app_type}"  # Format: Application ID : Application Type
        client_socket.send(message.encode())
        
        response = client_socket.recv(1024).decode()
        print(f"Client received: {response}")

# Contoh pengiriman request oleh client
send_request("App1", "Long")
send_request("App2", "Short")
send_request("App3", "Long")
send_request("App4", "Short")
