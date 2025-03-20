import socket
import datetime
import time

# Function to send message using TCP
def send_via_tcp(message):
    # Start timing
    start_time = time.time()
    
    # Create TCP socket
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect(('localhost', 65432))
    
    # Send message
    tcp_socket.sendall(message.encode())
    
    # Receive response
    response = tcp_socket.recv(1024)
    
    # End timing
    end_time = time.time()
    
    # Close socket
    tcp_socket.close()
    
    return response.decode(), (end_time - start_time)

# Function to send message using UDP
def send_via_udp(message):
    # Start timing
    start_time = time.time()
    
    # Create UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Send message
    udp_socket.sendto(message.encode(), ('localhost', 65433))
    
    # Receive response
    response, server = udp_socket.recvfrom(1024)
    
    # End timing
    end_time = time.time()
    
    # Close socket
    udp_socket.close()
    
    return response.decode(), (end_time - start_time)

# Get message from user
message = input("Enter message: ")

# Send via TCP
print("\n--- TCP Communication ---")
try:
    tcp_response, tcp_time = send_via_tcp(message)
    print(f"TCP Server response: {tcp_response}")
    print(f"TCP Time: {tcp_time:.6f} seconds")
except Exception as e:
    print(f"TCP Error: {e}")

# Send via UDP
print("\n--- UDP Communication ---")
try:
    udp_response, udp_time = send_via_udp(message)
    print(f"UDP Server response: {udp_response}")
    print(f"UDP Time: {udp_time:.6f} seconds")
except Exception as e:
    print(f"UDP Error: {e}")

# Compare times
if 'tcp_time' in locals() and 'udp_time' in locals():
    print("\n--- Comparison ---")
    time_diff = tcp_time - udp_time
    faster = "UDP" if time_diff > 0 else "TCP"
    print(f"Time difference: {abs(time_diff):.6f} seconds")
    print(f"{faster} was faster")

print(f"\nCurrent time: {datetime.datetime.now()}")