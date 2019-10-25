import os
import urllib
from nameko.dependency_providers import Config
from nameko.web.handlers import http
from urllib.request import urlopen
import sys
import psutil



class HttpService:
    name = "grab_client"


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
        msg='''
Hello User!

'''
        return msg 


    # Trailing slash required to avoid 301 redirect which fails. Not resolved.
    @http('GET', '/grab/<string:cmd>/')
    def get_method1(self, request, cmd):
        ip = self.config.get('IP')
        print("\n")
        print("IP:  " + ip)
        print("\n")
        cip = "http://"+ip + "/" + cmd
        print("\n")
        print("IP:  " + cip)
        print("\n")
        with urllib.request.urlopen(cip) as response:
            html = response.read()
        html = html.decode("utf8")
        response.close()
        return html

