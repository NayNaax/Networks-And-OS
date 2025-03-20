import socket
from encryption import encrypt, decrypt

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the localhost address and port 65433
server_socket.bind(('localhost', 65433))

print("UDP Secure Chat Server is running...")

# Users database {username: password}
users = {
    "admin": "password123",
    "alice": "secure456",
    "bob": "qwerty789"
}

# Dictionary of authenticated clients
authenticated_clients = {}
# Dictionary to track IP addresses
ip_addresses = {}

while True:
    # Receive data and client address
    data, client_address = server_socket.recvfrom(2048)
    encrypted_message = data.decode()
    
    # Decrypt the message
    message = decrypt(encrypted_message)
    
    # Check if client is authenticated
    if client_address not in authenticated_clients:
        # Try to authenticate
        if message.startswith("AUTH:"):
            parts = message[5:].split(":")
            if len(parts) == 2:
                username, password = parts
                if username in users and users[username] == password:
                    authenticated_clients[client_address] = username
                    
                    # Add to IP addresses dictionary
                    ip = client_address[0]
                    port = client_address[1]
                    if ip not in ip_addresses:
                        ip_addresses[ip] = []
                    ip_addresses[ip].append((port, username))
                    
                    # Encrypt the response
                    response = encrypt("Authentication successful!")
                    server_socket.sendto(response.encode(), client_address)
                    print(f"User {username} authenticated from {ip}:{port}")
                else:
                    response = encrypt("Authentication failed!")
                    server_socket.sendto(response.encode(), client_address)
            else:
                response = encrypt("Invalid authentication format!")
                server_socket.sendto(response.encode(), client_address)
        else:
            response = encrypt("Authentication required! Use AUTH:username:password")
            server_socket.sendto(response.encode(), client_address)
    else:
        # Process message from authenticated client
        username = authenticated_clients[client_address]
        print(f"Encrypted message from {username}: {encrypted_message}")
        print(f"Decrypted message: {message}")
        
        # Forward message to all authenticated clients
        formatted_message = encrypt(f"{username}: {message}")
        for client in authenticated_clients:
            if client != client_address:  # Don't send back to sender
                server_socket.sendto(formatted_message.encode(), client)