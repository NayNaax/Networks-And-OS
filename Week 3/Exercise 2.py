import subprocess

def tracert(domain):
    try:
        result = subprocess.run(["tracert", domain], capture_output=True, text=True)
        print(result.stdout)
    except FileNotFoundError:
        print("tracert command not found. Make sure it's available.")
    except Exception as e:  # Catching general exceptions for now
        print(f"An error occurred: {e}")

# Example usage
domains = ["google.com", "8.8.8.8", "example.com"]  # You can add more
for domain in domains:
    print(f"Traceroute for {domain}:")
    tracert(domain)