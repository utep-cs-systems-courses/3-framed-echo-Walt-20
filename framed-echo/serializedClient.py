import socket
import sys
import os

# Set up the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 8000))

# Read the file contents
file_name = sys.argv[1]
with open(file_name, 'r') as f:
    file_contents = f.read()

# Serialize the file contents
file_contents = file_contents.encode()
file_size = len(file_contents)

# Send the file size
file_size_bytes = file_size.to_bytes(4, byteorder='big')
client_socket.sendall(file_size_bytes)

# Send the file contents
client_socket.sendall(file_contents)

# Clean up
print(f'{file_name} sent.')
client_socket.close()
