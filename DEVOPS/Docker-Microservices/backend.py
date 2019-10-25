import os
import urllib
from nameko.web.handlers import http
from urllib.request import urlopen
import sys



# class HttpService:
#     name = "download_file"

#     # Print commands
#     @http('GET', '/')
#     def get_method(self, request):
#         cmds = '''
#                     COMMANDS: 
#                     getFileContents          
#                     '''
#         sys.stdout.flush()
#         return cmds

   
# @http('GET', '/getFileContents')
# def get_file(self, request):
#     with open('/vagrant/src/files/a.txt', 'r') as f:
#         result = f.read().replace('\n', '')
#     return result

    