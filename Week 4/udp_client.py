import socket
import threading
import sys

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 65433)

# Function to receive messages from server
def receive_messages():
    while True:
        try:
            data, _ = client_socket.recvfrom(2048)
            print(data.decode())
        except:
            break

# Start a thread for receiving messages
receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

# Get username from user
username = input("Enter your username: ")
# Send join message
client_socket.sendto(f"{username} joined the chat".encode(), server_address)

print("Type 'exit' to quit the chat")
# Main loop for sending messages
while True:
    message = input("")
    if message.lower() == 'exit':
        client_socket.sendto(f"{username} left the chat".encode(), server_address)
        break
    
    client_socket.sendto(f"{username}: {message}".encode(), server_address)

client_socket.close()