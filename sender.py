import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = "Water intake started - status: OK"

print(f"Sending message: {MESSAGE}")

# Creating socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))

print("Sent.")