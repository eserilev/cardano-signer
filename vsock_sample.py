#!/usr/local/bin/env python3

# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import argparse
import socket
import sys
from cardano import Cardano

class VsockListener:
    """Server"""
    def __init__(self, conn_backlog=128):
        self.conn_backlog = conn_backlog
        self.cardano_obj = Cardano()

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
                    if data:
                        try:
                            signed_tx = self.cardano_obj.sign_transaction(tx_body_cbor=data)
                        except:
                            print('failed signature')
                    if signed_tx:
                        print('signed transaction')
                        self.send_data(data=signed_tx.to_cbor().encode())
                except socket.error:
                    break
                if not data:
                    break
            print()

    def send_data(self, data):
        """Send data to a remote endpoint"""
        (to_client, (remote_cid, remote_port)) = self.sock.accept()
        to_client.sendall(data)
        to_client.close()
            


def server_handler(args):
    server = VsockListener()
    server.bind(args.port)
    server.recv_data()


def main():
    parser = argparse.ArgumentParser(prog='vsock-sample')
    parser.add_argument("--version", action="version",
                        help="Prints version information.",
                        version='%(prog)s 0.1.0')
    subparsers = parser.add_subparsers(title="options")

    server_parser = subparsers.add_parser("server", description="Server",
                                          help="Listen on a given port.")
    server_parser.add_argument("port", type=int, help="The local port to listen on.")
    server_parser.set_defaults(func=server_handler)

    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()