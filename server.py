import socket
# from cardano import Cardano

class VsockListener:
    """Server"""
    def __init__(self, conn_backlog=128):
        self.conn_backlog = conn_backlog
        # self.cardano_obj = Cardano(env="local")

    def bind(self, port):
        """Bind and listen for connections on the specified port"""
        self.sock = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
        self.sock.bind((socket.VMADDR_CID_ANY, port))
        self.sock.listen(self.conn_backlog)

    def recv_data(self):
        """Receive data from a remote endpoint"""
        while True:
            (from_client, (remote_cid, remote_port)) = self.sock.accept()
            # Read 1024 bytes at a time
            while True:
                try:
                    data = from_client.recv(1024).decode()
                    print(data)
                    # transaction = self.cardano_obj.sign_transaction(tx_body_cbor=data)
                    self.send_data(data=None)
                except socket.error:
                    print('yo')
                    continue
                if not data:
                    continue
               
            print()
            from_client.close()

    def send_data(self, data):
        """Send data to a remote endpoint"""
        while True:
            (to_client, (remote_cid, remote_port)) = self.sock.accept()
            to_client.sendall(data)
            to_client.close()

def server_handler():
    server = VsockListener()
    server.bind(5005)
    server.recv_data()

def main():
    server_handler()

if __name__ == "__main__":
    main()

