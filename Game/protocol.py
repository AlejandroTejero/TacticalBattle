import pickle
import struct


def recv_all(sock, length):
    buffer = b''
    while length != 0:
        buffer_aux = sock.recv(length)
        if not buffer_aux:
            return None
        buffer = buffer + buffer_aux
        length = length - len(buffer_aux)
    return buffer


def send_one_message(sock, message, is_text=True):
    if is_text:
        encoded_data = message.encode('utf-8')
    else:
        encoded_data = pickle.dumps(message)
    length = len(encoded_data)
    header = struct.pack("!I", length)
    sock.sendall(header)
    sock.sendall(encoded_data)


def recv_one_message(sock, is_text=True):
    header_buffer = recv_all(sock, 4)
    if header_buffer:
        header = struct.unpack("!I", header_buffer)
        length = header[0]
        encoded_data = recv_all(sock, length)
        if is_text:
            message = encoded_data.decode('utf-8')
        else:
            message = pickle.loads(encoded_data)
        return message
    else:
        raise ConnectionError("La conexión se cerró antes de recibir el mensaje completo")
