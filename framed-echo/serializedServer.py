import socket
import sys
import os

# Set up the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 8000))
server_socket.listen(1)

# Wait for a connection
print('Waiting for connection...')
client_socket, client_address = server_socket.accept()

# Receive the file size
file_size_bytes = client_socket.recv(4)
file_size = int.from_bytes(file_size_bytes, byteorder='big')
print(f'Receiving a file of size {file_size} bytes...')

# Receive the file contents
file_contents = bytearray()
while len(file_contents) < file_size:
    data = client_socket.recv(file_size - len(file_contents))
    if not data:
        break
    file_contents.extend(data)

# Deserialize the file contents
file_contents = file_contents.decode()

# Write the file to disk
with open('received_file.txt', 'w') as f:
    f.write(file_contents)

# Clean up
print('File received and written to disk.')
client_socket.close()
server_socket.close()
