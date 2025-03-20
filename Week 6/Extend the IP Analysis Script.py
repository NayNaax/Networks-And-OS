import ipaddress

def analyse_ip(ip_str):
    # Create an IP interface object
    ip = ipaddress.ip_interface(ip_str)
    print(f"Address: {ip.ip}")
    print(f"Network: {ip.network}")
    print(f"Netmask: {ip.netmask}")
    print(f"Broadcast Address: {ip.network.broadcast_address}")
    print(f"First Usable Host: {list(ip.network.hosts())[0]}")
    print(f"Last Usable Host: {list(ip.network.hosts())[-1]}")
    print(f"Number of Usable Hosts: {ip.network.num_addresses - 2}")
    print(f"Is private: {ip.ip.is_private}")
    print(f"Is global: {ip.ip.is_global}")

    # Compare networks with different CIDR prefixes
    new_ip = ip.ip.with_prefixlen.replace(str(ip.network.prefixlen), "24")
    new_network = ipaddress.ip_network(new_ip, strict=False)
    print(f"\nComparing with /24 network: {new_network}")

    # List all hosts in the network
    if ip.network.num_addresses < 256:  # Only for small networks
        print("\nHosts in network:")
        for host in ip.network.hosts():
            print(host)

# Example usage
analyse_ip('192.168.1.1/28')