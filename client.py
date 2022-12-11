
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

def client_handler():
    client = VsockStream()
    endpoint = (19, 5005)
    client.connect(endpoint)
    unsigned_tx = '84a3008282582032f8d11b6f5c888f5c5e9284085a8029295910b9bb6fba20e3ccaf080b40255c00825820dd37eadaea173565de5d3ea6091b85e525296a6ba4d7559bf59f8b08ed2db67b00018282581d607f155365338cb05bf72fc60a0dd5b6627eefb8713f297153bbc9e47c1a001e848082581d609872b47e668b9991c67afd00608685f1b9fd850563fb851ece13794a1b0000000253f87c7b021a00028d05a10080f5f6'
    client.send_data(unsigned_tx.encode())
    client.disconnect()


def main():
    print("YO")
    client_handler()

if __name__ == "__main__":
    main()