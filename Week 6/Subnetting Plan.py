import ipaddress

def create_subnet_plan(network, departments):
    base_network = ipaddress.ip_network(network)
    subnets = list(base_network.subnets(new_prefix=27))  # Start with /27 for flexibility

    plan = {}
    for department, hosts in departments.items():
        for subnet in subnets:
            if subnet.num_addresses - 2 >= hosts:  # Check usable hosts
                plan[department] = subnet
                subnets.remove(subnet)
                break

    return plan

# Define requirements
network = '172.16.0.0/16'
departments = {
    "Engineering": 30,
    "Marketing": 15,
    "Finance": 10,
    "HR": 5
}

# Generate plan
plan = create_subnet_plan(network, departments)
for dept, subnet in plan.items():
    print(f"{dept}: {subnet} (Usable Hosts: {subnet.num_addresses - 2})")