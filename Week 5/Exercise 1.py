import socket
import datetime

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 65432))

message = input("Enter message: ")
client_socket.sendall(message.encode())

response = client_socket.recv(1024)
print(f"Server response: {response.decode()}")

client_socket.close()
datetime.datetime.now()