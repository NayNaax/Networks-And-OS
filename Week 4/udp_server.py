import socket

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the localhost address and port 65433
server_socket.bind(('localhost', 65433))

print("UDP Chat Server is running...")

# Dictionary to keep track of clients
clients = {}

# Continuously listen for incoming packets
while True:
    # Receive data and client address
    data, client_address = server_socket.recvfrom(2048)
    
    # Store client in our clients dictionary
    if client_address not in clients:
        clients[client_address] = client_address[0]
    
    # Print the received data
    message = data.decode()
    print(f"Received from {client_address}: {message}")
    
    # Forward the message to all other clients
    for client in clients:
        if client != client_address:  # Don't send back to the sender
            server_socket.sendto(data, client)