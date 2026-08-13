from http.server import BaseHTTPRequestHandler, HTTPServer


def run_server(address: tuple[str, int], handler: type[BaseHTTPRequestHandler]) -> None:
    server = HTTPServer(address, handler)

    print(f'Run server on {address[0]}:{address[1]}')
    server.serve_forever()
