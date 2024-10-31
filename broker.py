import socket
import threading

class BrokerServer:
    def __init__(self):
        self.worker_servers = [("localhost", 8081), ("localhost", 8082), ("localhost", 8083)]
        self.request_count = [0, 0, 0]  # Counter untuk setiap worker
        self.current_index = 0

    def handle_client(self, client_socket):
        request = client_socket.recv(1024).decode()
        app_id, app_type = request.split(":")

        # Metode alokasi: pilih antara "round_robin" atau "balanced"
        allocation_method = "round_robin"
        
        if allocation_method == "balanced":
            # Alokasi dengan pemerataan jumlah request
            target_index = self.request_count.index(min(self.request_count))
            self.request_count[target_index] += 1
        else:
            # Alokasi berurutan (round-robin)
            target_index = self.current_index
            self.current_index = (self.current_index + 1) % 3

        target_server = self.worker_servers[target_index]
        self.forward_request(target_server, request, client_socket)
        print(f"Broker: Forwarded request '{app_id}' to Worker {target_index + 1}.")

    def forward_request(self, server_address, request, client_socket):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as worker_socket:
            worker_socket.connect(server_address)
            worker_socket.send(request.encode())
            response = worker_socket.recv(1024)
            client_socket.send(response)
        client_socket.close()

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("localhost", 8080))
        server_socket.listen(5)
        print("Broker server running on port 8080...")

        while True:
            client_socket, addr = server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    broker = BrokerServer()
    broker.start()
