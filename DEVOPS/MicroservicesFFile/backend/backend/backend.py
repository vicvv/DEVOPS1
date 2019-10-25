import os
import urllib
from nameko.web.handlers import http
from urllib.request import urlopen
import sys



class HttpService:
    name = "backend_service"

    @http('GET', '/<string:fname>')
    def get_method0(self, request,fname):
        f = open(fname,"r")
        data = [line.rstrip('\n') for line in f]
        strData = data[0] + "\n"
        f.close()
        return strData 


