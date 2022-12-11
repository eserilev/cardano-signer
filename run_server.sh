docker build -t vsock-server -f Dockerfile.server .
nitro-cli build-enclave --docker-uri vsock-server --output-file vsock_server.eif
sudo nitro-cli run-enclave --eif-path vsock_server.eif --cpu-count 2 --memory 2054 --debug-mode