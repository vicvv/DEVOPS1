import os
import urllib
from nameko.web.handlers import http
from urllib.request import urlopen
import sys
import psutil


class HttpService:
    name = "psutils_client"

    # Print commands
    @http('GET', '/')
    def get_method1(self, request):
        print("\n")
        print ("Calling Method 1 with python version: ",sys.version_info[:])
        print("\n")
        cmds = '''
COMMANDS: 
cpu_times 
virtual_memory 
swap_memory 
net_if_addrs
          
'''
        sys.stdout.flush()
        return cmds

    @http('GET', '/cpu_times')
    def get_cpu_times(self, request):
        result = str(psutil.cpu_times()) + '''

''';
        return result

    @http('GET', '/virtual_memory')
    def get_virtual_memory(self, request):
        result = str(psutil.virtual_memory()) + '''

''';
        return result

    @http('GET', '/swap_memory')
    def get_swap_memory(self, request):
        result = str(psutil.swap_memory()) + '''

''';
        return result
        
    @http('GET', '/net_if_addrs')
    def get_net_if_addrs(self, request):
        result = str(psutil.net_if_addrs()) + '''

''';
        return result
