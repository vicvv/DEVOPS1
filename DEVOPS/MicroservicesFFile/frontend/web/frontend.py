import os
import urllib
from nameko.dependency_providers import Config
from nameko.web.handlers import http
from urllib.request import urlopen
import sys




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

 
    @http('GET', '/<string:fname>')
    def get_method1(self, request,fname):
        print("\n")
        ip = self.config.get('IP')
        cip = "http://" +ip + "/" + fname
        with urllib.request.urlopen(cip) as response:
            html = response.read()
        html = html.decode("utf8") + "\n"
        response.close()
        return html 


    
