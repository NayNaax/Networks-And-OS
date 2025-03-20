import socket
import ipaddress

def analyse_website_ip(website):
    IPAddr = socket.gethostbyname(website)
    print(f"Website: {website}")
    print(f"IP Address: {IPAddr}")

    # Analyze the IP address
    ip = ipaddress.ip_address(IPAddr)
    print(f"Is private: {ip.is_private}")
    print(f"Is global: {ip.is_global}")

# Example usage
analyse_website_ip('www.university.edu')