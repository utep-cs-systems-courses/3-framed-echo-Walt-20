import socket
import os
import sys

# Set up the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 50001))
server_socket.listen(5)

# Listen for incoming connections and handle them in child processes
while True:
    client_socket, client_address = server_socket.accept()
    pid = os.fork()
    
    if pid == 0:  # Child process
        print(f"Child process {os.getpid()} handling connection from {client_address}")
        
        # Receive the file size
        file_size_bytes = client_socket.recv(4)
        file_size = int.from_bytes(file_size_bytes, byteorder='big')
        
        # Receive the file contents
        file_contents = b''
        bytes_received = 0
        while bytes_received < file_size:
            chunk = client_socket.recv(file_size - bytes_received)
            if not chunk:
                break
            file_contents += chunk
            bytes_received += len(chunk)

        # Deserialize the file contents
        file_contents = file_contents.decode()

        # Save the file contents to disk
        with open(f'file_{os.getpid()}.txt', 'w') as f:
            f.write(file_contents)

        # Clean up
        print(f"Child process {os.getpid()} received and saved file")
        client_socket.close()
        sys.exit(0)
    
    else:  # Parent process
        client_socket.close()
