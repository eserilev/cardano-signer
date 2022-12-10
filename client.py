
import socket


class VsockStream:
    """Client"""
    def __init__(self, conn_tmo=5):
        self.conn_tmo = conn_tmo

    def connect(self, endpoint):
        """Connect to the remote endpoint"""
        self.sock = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
        self.sock.settimeout(self.conn_tmo)
        self.sock.connect(endpoint)

    def send_data(self, data):
        """Send data to a remote endpoint"""
        self.sock.sendall(data)

    def recv_data(self):
        """Receive data from a remote endpoint"""
        while True:
            data = self.sock.recv(1024).decode()
            if not data:
                break
            print(data, end='', flush=True)
        print()

    def disconnect(self):
        """Close the client socket"""
        self.sock.close()

def client_handler(args):
    client = VsockStream()
    endpoint = ("i-093d90abd3f89c8ec-enc184fca2de3734aa", 5005)
    client.connect(endpoint)
    unsigned_tx = ''
    client.send_data(unsigned_tx.encode())
    client.disconnect()


def main():
    print("YO")
    client_handler()
