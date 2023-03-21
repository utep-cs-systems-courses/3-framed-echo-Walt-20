import socket, sys, re
sys.path.append("../lib")  # for params
import params

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-?', '--usage'), 'usage', False),
)

progname = 'fixedLengthClient'
paramMap = params.parseParams(switchesVarDefaults)

server, usage = paramMap['server'], paramMap['usage']

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(':', server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

# Create a socket and connect to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((serverHost, serverPort))

# Send messages with fixed-length framing
outMessages = [
    b'Hello',
    b'World!',
    b'How are you?',
]

for message in outMessages:
    # Prefix the message with its length using a fixed-length prefix
    prefix = len(message).to_bytes(4, byteorder='big')
    framedMessage = prefix + message

    # Send the framed message to the server
    s.sendall(framedMessage)

# Signal the end of the output stream by sending a zero-length message
s.sendall(b'\x00\x00\x00\x00')

# Receive messages with fixed-length framing
while True:
    # Receive the message length prefix
    prefix = s.recv(4)

    # If we received an empty message length prefix, the server is done sending messages
    if not prefix:
        break

    # Extract the message length from the prefix
    messageLength = int.from_bytes(prefix, byteorder='big')

    # Receive the message content
    message = s.recv(messageLength)

# Close the socket
s.close()
