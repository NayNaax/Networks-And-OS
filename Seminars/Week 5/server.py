import socket
import threading

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 65432))
server_socket.listen(1) # Allow 1 pending connection

print("TCP Server is listening...")

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(('localhost', 65433))

def handle_udp():
    print("UDP Server is listening...")
    while True:
        data, client_address = udp_socket.recvfrom(1024)
        print(f"UDP Received from {client_address}: {data.decode()}")
        udp_socket.sendto(b"ACK: " + data, client_address)

# Start UDP handler in a separate thread
udp_thread = threading.Thread(target=handle_udp)
udp_thread.daemon = True
udp_thread.start()

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connected to {client_address}")

    # First receive regular message
    data = client_socket.recv(1024)
    print(f"Received: {data.decode()}")

    # Echo back the data
    client_socket.sendall(b"ACK: " + data)
    
    # Now handle file receiving
    with open('received_file.txt', 'wb') as f:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            f.write(data)
    print("File received!")
    
    client_socket.close()
