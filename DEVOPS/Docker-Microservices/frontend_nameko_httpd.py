import os
import urllib
from nameko.dependency_providers import Config
from nameko.web.handlers import http
from urllib.request import urlopen
import sys
import psutil

class HttpService:
    name = "connect_to_client"
    config = Config()

    # Hello User! 
    @http('GET', '/')
    def get_method0(self, request):
        print("\n")
        ip = self.config.get('IP')
        print("\n")
        print("IP:  " + str(ip))
        print ("Calling Method 1 with python version: ",sys.version_info[:])
        print("\n")
        sys.stdout.flush()

        # Format output for client
        msg='''Hello User!!!!\n'''
        return msg 


    # Trailing slash required to avoid 301 redirect which fails. Not resolved.
    # @http('GET', '/grab/<string:cmd>/')
    # def get_method(self, request, cmd):
    #     #ip = config.get('IP')
        
    #     ip = '10.1.1.17'
    #     cip = "http://"+ip +":8000" +"/" + cmd
    #     print("IP:  " + cip, ip)
    #     print("\n")
    #     with urllib.request.urlopen(cip) as response:
    #         html = response.read()
    #     html = html.decode("utf8")
    #     response.close()
    #     return html

    @http('GET', '/<string:cmd>/<string:file>')
    def get_method(self, request, cmd, file):
        #ip = config.get('IP')
        
        ip = '10.1.1.17'
        cip = "http://"+ip +":8000" +"/" + cmd + "/" + file
        print("IP:  " + cip, ip)
        print("\n")
        with urllib.request.urlopen(cip) as response:
            html = response.read()
        html = html.decode("utf8")
        response.close()
        return html



