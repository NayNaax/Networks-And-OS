import socket
import json

server_config = {
    "ip_pool": ["192.168.1.100", "192.168.1.101", "192.168.1.102"],
    "leases": {}
}

def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    request_data = json.loads(request)

    if request_data["type"] == "DISCOVER":
        if server_config["ip_pool"]:
            offered_ip = server_config["ip_pool"].pop(0)
            response = {"type": "OFFER", "ip": offered_ip}
            client_socket.send(json.dumps(response).encode())
        else:
            client_socket.send(json.dumps({"type": "NACK"}).encode())

    elif request_data["type"] == "REQUEST":
        server_config["leases"][request_data["mac"]] = request_data["ip"]
        response = {"type": "ACK", "ip": request_data["ip"]}
        client_socket.send(json.dumps(response).encode())

    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5000))  # Server
    server.listen(5)
    print("DHCP Server is running...")

    while True:
        client_socket, addr = server.accept()
        handle_client(client_socket)

if __name__ == "__main__":
    main()