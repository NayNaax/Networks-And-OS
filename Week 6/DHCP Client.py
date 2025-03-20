import socket
import json

client_config = {
    "mac": "AA:BB:CC:DD:EE:FF",
    "ip": None
}

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 5000))

    # Step 1: Send DISCOVER
    discover = {"type": "DISCOVER", "mac": client_config["mac"]}
    client.send(json.dumps(discover).encode())

    # Step 2: Receive OFFER
    offer = json.loads(client.recv(1024).decode())
    if offer["type"] == "OFFER":
        print(f"Received OFFER: {offer['ip']}")

        # Step 3: Send REQUEST
        request = {"type": "REQUEST", "mac": client_config["mac"], "ip": offer["ip"]}
        client.send(json.dumps(request).encode())

        try:
            request_data = json.loads(request)
        except json.JSONDecodeError:
            print("Received invalid JSON")
            client.close()
            return

        # Step 4: Receive ACK
        ack = json.loads(client.recv(1024).decode())
        if ack["type"] == "ACK":
            client_config["ip"] = ack["ip"]
            print(f"Received ACK: {ack['ip']}")

    client.close()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")