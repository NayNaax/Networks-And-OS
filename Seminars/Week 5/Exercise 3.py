import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 65432))
server_socket.listen(1)

print("TCP Server is listening...")

client_socket, client_address = server_socket.accept()
print(f"Connected to {client_address}")

with open('received_data.txt', 'w') as f:  # Open file in write mode ('w')
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        f.write(data.decode())  # Write decoded data to the file
        print(f"Received: {data.decode()}")
        client_socket.sendall(b"ACK: " + data)

print("File received and saved!")
client_socket.close()