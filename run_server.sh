docker build -t vsock-server -f Dockerfile.server .
nitro-cli build-enclave --docker-uri vsock-server --output-file vsock_server.eif