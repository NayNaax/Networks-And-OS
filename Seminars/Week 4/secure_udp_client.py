import socket
import threading
from encryption import encrypt, decrypt

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 65433)

# Function to receive messages from server
def receive_messages():
    while True:
        try:
            data, _ = client_socket.recvfrom(2048)
            # Decrypt the received message
            decrypted_message = decrypt(data.decode())
            print(decrypted_message)
        except Exception as e:
            print(f"Error: {e}")
            break

# Authenticate with server
username = input("Enter username: ")
password = input("Enter password: ")
auth_message = f"AUTH:{username}:{password}"
# Encrypt the authentication message
encrypted_auth = encrypt(auth_message)
client_socket.sendto(encrypted_auth.encode(), server_address)

# Start a thread for receiving messages
receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

print("Type 'exit' to quit the chat")
# Main loop for sending messages
while True:
    message = input("")
    if message.lower() == 'exit':
        break
    
    # Encrypt the message before sending
    encrypted_message = encrypt(message)
    client_socket.sendto(encrypted_message.encode(), server_address)

client_socket.close()