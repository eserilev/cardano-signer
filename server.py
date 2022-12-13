import socket

class VsockListener:
    """Server"""
    def __init__(self, conn_backlog=128):
        self.conn_backlog = conn_backlog

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
                pass
                # try:
                #     data = from_client.recv(1024).decode()
                #     if data:
                #         print(data)
                # except socket.error:
                #     print('yo')
                #     continue
                # if not data:
                #     continue
               
            print()
            # self.send_data(data='test'.encode())

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
    # server_handler()
    while True:
        print('yo')

if __name__ == "__main__":
    main()

