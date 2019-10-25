import os
import urllib
from nameko.dependency_providers import Config
from nameko.web.handlers import http
from urllib.request import urlopen
import sys
import psutil
import yaml

class HttpService:
    name = "connect_to_client"
    config = Config()
    
    # Hello User! 
    @http('GET', '/')
    def get_method0(self, request):
        print("\n")
        ip = self.config.get('IP')
        sys.stdout.flush()
        msg='''Hello User!!!!\n'''
        return msg 

    @http('GET', '/<string:cmd>/<string:file>')
    def get_method(self, request, cmd, file):
        ip = self.config.get('IP')
        #ip = '10.1.1.17'
        cip = "http://" +ip +"/" + cmd + "/" + file 
        print("IP:  " + cip, ip)
        print("\n")
        with urllib.request.urlopen(cip) as response:
            html = response.read()
        html = html.decode("utf8")
        response.close()
        return html



