import json
from nameko.web.handlers import http

class HttpService:
    name = "backend_service"

    @http('GET', '/get/<string:file>')
    def get_file(self, request, file):
        with open('/vagrant/src/files/' + file, 'r') as f:
            result = f.read().replace('\n', '')
        return result
