import subprocess
import os

def run_tracert(domain, output_file):
    """
    Runs tracert (Windows) or traceroute (macOS/Linux) and saves the output to a file.

    Args:
        domain: The domain name or IP address to trace.
        output_file: The name of the file to save the output to.
    """
    try:
        if os.name == 'nt':  # Windows
            command = ["tracert", domain]
        else:  # macOS or Linux
            command = ["traceroute", domain]

        result = subprocess.run(command, capture_output=True, text=True)

        with open(output_file, "w") as f:
            f.write(result.stdout)
        print(f"Trace route output for {domain} saved to {output_file}")

    except FileNotFoundError:
        print(f"{command[0]} command not found. Make sure it's available for your operating system.")
    except Exception as e:
        print(f"An error occurred: {e}")

# --- Example Usage ---
target_domain = "google.com"  # Change this to the domain you want to trace

# You'll need to run this script multiple times, 
# each time after you've changed your network location

# First location (e.g., home)
run_tracert(target_domain, "tracert_home.txt")

# After changing to a second location (e.g., coffee shop)
run_tracert(target_domain, "tracert_coffeeshop.txt")

# And so on...