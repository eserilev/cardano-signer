
import socket


class VsockStream:
    """Client"""
    def __init__(self, conn_tmo=5):
        self.conn_tmo = conn_tmo

    def connect(self, endpoint):
        """Connect to the remote endpoint"""
        print(endpoint)
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
                continue
            print()
            print(f'signed_tx: {data}')
            break
        print()

    def disconnect(self):
        """Close the client socket"""
        self.sock.close()

def client_handler():
    client = VsockStream()
    endpoint = (21, 5005)
    client.connect(endpoint)
    unsigned_tx = 'a3008482582061ec2e00950b327e5a7e1e310d5817ee39bd3f400395b7af9e89ea658a6846c500825820acea00e1d3d95825a3ccdf7b121b7d5bb036424a31605a6977a6fe954425b00100825820bf85dbcee379daf56adb2d81480e02d0843565ab7d507f7e3cb106bbc27323c900825820d4175f22618cfbb7be3abf83f5ae22be3df22aeaf26b410c58dd50d558c8f89d00018282581d60d35dbbd8d078512d82cc8009ca09c448c73cf001c7ac4ad5897db4441a002dc6c082583900eba8d934c4090debac490538e8b30f433c19c008ffcaa1fda99c0de8717bb20a176c10c51603cb841bf0c29a9ed067bb52df083cdfdad3e6821a00276eeba1581c9ce492a69b50a7f0aa3657b5a9c3b6f8b230902503817fdd03f4d51ca151476f65726c6956657269666965645354471a003d0900021a0002a725'
    print(f'submitting unsigned tx: {unsigned_tx}')
    print()
    client.send_data(unsigned_tx.encode())
    client.recv_data()
    client.disconnect()


def main():
    client_handler()

if __name__ == "__main__":
    main()