# Define delimiters for start and end
START_DELIMITER = bytes([0x02])
END_DELIMITER = bytes([0x03])

# define max packet size
MAX_PACKET_SIZE = 1024

# framing the message
def frame_message(message_str):
    # covert the message to a byte array
    message = message_str.encode('utf*8')

    # calculate number of packets needed
    num_packets = (len(message) + MAX_PACKET_SIZE - 1) // MAX_PACKET_SIZE

    # list to hold packets
    packets = []

    # segment the message into packets
    for i in range(num_packets):
        # calculate the size of the current packet
        packet_size = min(MAX_PACKET_SIZE, len(message) - i * MAX_PACKET_SIZE)

        # create byte array from current packet
        packet = bytearray(packet_size + 3)

        # add the start delimiter
        packet[0:1] = START_DELIMITER

        # add sequence number so as to identify the order of the packets
        # in the original message
        packet[1:2] = bytes([i])

        # add data
        packet[2:packet_size+2] = message[i * MAX_PACKET_SIZE:(i+1) * MAX_PACKET_SIZE]

        # add the end delimiter
        packet[2:packet_size+2:packet_size+3] = END_DELIMITER

        # Add packet to list
        packets.append(packet)

    # concatenate packets into a single byte array
    framed_message = bytearray().join(packets)

    return framed_message
        
