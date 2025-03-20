import socket
import ipaddress

def analyse_device_ip():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    print("Your Computer Name is:", hostname)
    print("Your Computer IP Address is:", IPAddr)

    # Analyze the IP address
    ip = ipaddress.ip_address(IPAddr)
    print(f"Is private: {ip.is_private}")
    print(f"Is global: {ip.is_global}")

analyse_device_ip()