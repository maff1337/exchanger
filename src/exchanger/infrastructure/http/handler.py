import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

from exchanger.exceptions import UnsupportedMediaType
from exchanger.infrastructure.controllers.types import HttpRequest, HttpResponse
from exchanger.infrastructure.http.routing.router import Router


def create_handler(router: Router) -> type[BaseHTTPRequestHandler]:
    class HttpHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            self._handle_request()
        
        def do_POST(self) -> None:
            self._handle_request()
        
        def do_PATCH(self) -> None:
            self._handle_request()
        
        def _handle_request(self) -> None:
            try:
                request = self._create_request()
                
                response = router.handle(request)
                
                self._send_response(response)
            except UnsupportedMediaType as e:
                response = HttpResponse(
                    status_code=415,
                    headers={'Content-Type': 'application/json'},
                    body={'message': str(e)}
                )
                
                self._send_response(response)
        
        def _create_request(self) -> HttpRequest:
            parsed_url = urlparse(self.path)
            
            return HttpRequest(
                method=self.command,
                path=parsed_url.path,
                headers=dict(self.headers),
                query=self._parse_query(parsed_url.query),
                body=self._parse_body()
            )

        def _parse_query(self, query_string: str) -> dict[str, str] | None:
            if not query_string:
                return None
            
            query = parse_qs(query_string)
            
            return {k: v[0] for k, v in query.items()}
        
        def _parse_body(self) -> dict | None:
            content_length = self.headers.get('Content-Length')
            
            if content_length is None:
                return None
            
            raw = self.rfile.read(int(content_length))
            
            if not raw:
                return None
            
            content_type = self.headers.get('Content-Type', '')
            media_type = content_type.split(';', 1)[0].strip().lower()
            
            print(media_type)
            
            if media_type == 'application/json':
                return json.loads(raw.decode('utf-8'))
            
            if media_type == 'application/x-www-form-urlencoded':
                return {
                    key: value[0]
                    for key, value in parse_qs(
                        raw.decode('utf-8')
                    ).items()
                }
            
            raise UnsupportedMediaType(f'Unsupported media type: {media_type}')
        
        def _send_response(self, response: HttpResponse) -> None:
            self.send_response(response.status_code)
            
            for name, value in response.headers.items():
                self.send_header(name, value)
                
            self.end_headers()
            
            if response.body is None:
                return
            
            body = json.dumps(response.body, ensure_ascii=False).encode('utf-8')
            
            self.wfile.write(body)

    return  HttpHandler