import socket
import sys

def main():
    if len(sys.argv) < 3:
        print("Usage: python client.py <server_ip> <server_port>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_ip, server_port))
    print(f"Connected to server at {server_ip}:{server_port}")

    try:
        while True:
            data = s.recv(1024)
            if not data:
                print("Server closed the connection...")
                break

            message = data.decode("ascii", errors="ignore")
            print(message, end="")

            if "Goodbye..." in message:
                break

            user_input = input("> ").strip()
            print(f"[Client Log] Sending '{user_input}' to server.")
            s.sendall(user_input.encode("ascii"))

    except KeyboardInterrupt:
        print("\nClient exiting due to user interrupt.")
    finally:
        s.close()

if __name__ == "__main__":
    main()
