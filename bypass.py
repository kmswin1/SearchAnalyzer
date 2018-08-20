#-*- coding: utf-8 -*-
import sys
import json
import os
import urllib2
import urllib
import pprint
import traceback
import library
import tornado.ioloop
import tornado.web
import tornado.template as template
import time

import urllib2

ENGINE_ACCOUNT = "poi"



PWD = os.path.dirname(os.path.realpath(__file__))
params =  {}
class SearchHandler(tornado.web.RequestHandler):


    def get(self, local_args={}, local=False):

        self.set_header('X-FRAME-OPTIONS', 'SAMEORIGIN')

        API = "http://172.27.108.24:8080/tmap/1.0/search/poi.json"
        queryString = ""
        args = self.request.arguments

        for key in args:
            queryString += key + "=" + args[key][0].strip() + "&"

        API_URL = API + "?" + queryString

        result = urllib2.urlopen(API_URL).read()


        self.write(result)


