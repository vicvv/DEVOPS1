import json
import os
import sys
import glob
from nameko.web.handlers import http

class HttpService:
    name = "backend_service"
    @http('GET', '/get/<string:file>')
    def get_file(self, request, file):
        try:
            with open(os.path.expanduser('/app/files/') + file, 'r') as f:
                result = f.read().replace('\n', '')
            return result + "\n"
        except FileNotFoundError as e:
            return str(e) + "\n" + "File requested: "+ str(file) + "\n" +"Files available: " + str(glob.glob("/app/files/*.txt"))
