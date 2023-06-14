import socket
import handle_data
_active = False
# Print ip to console on load
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("1.1.1.1", 0))
print('This IP: {}'.format(s.getsockname()[0]))
s.close()
def start(port):
    global _active
    _active = True
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port))
    sock.settimeout(0.5)
    while _active:
        try:byte_data, addr = sock.recvfrom(1347)
        except socket.timeout:continue
        handle_data.start(byte_data)
def stop():
    global _active
    _active = False
    handle_data.stop()