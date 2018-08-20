#-*- coding: utf-8 -*-
import sys
import json
import os
import tornado.ioloop
import tornado.web
import tornado.template as template
import urllib2
import urllib
import traceback


import poi_search
import bypass
import query

KLP_SEARCH_API = "http://172.27.97.204:9300/wiki/_analyze?analyzer=search_analyzer&pretty&text=%s"
KLP_INDEX_API = "http://172.27.97.204:9300/wiki/_analyze?analyzer=klp_analyzer&pretty&text=%s"

PWD = os.path.dirname(os.path.realpath(__file__))

class AnalyzerHandler(tornado.web.RequestHandler):
    def get(self):
        result = {"text": "", "result": {}, "klp_index": {}, "klp_search": {}}
        args = self.request.arguments
        print args
        text = ""
        if "text" in args:
            text = args["text"][0]
        result["text"] = text
        try:
            f = urllib2.urlopen(KLP_INDEX_API%urllib.quote(text))
            analyzerResult = json.loads(f.read(), "utf-8")
            f.close()
        except:
            analyzerResult = {"exception": "Query is None!!"}

        result["klp_index"] = json.dumps(library._decode_dict(analyzerResult), indent=2, ensure_ascii=False)

        try:
            f = urllib2.urlopen(KLP_SEARCH_API%urllib.quote(text))
            analyzerResult = json.loads(f.read(), "utf-8")
            f.close()
        except:
            analyzerResult = {"exception": "Query is None!!"}

        result["klp_search"] = json.dumps(library._decode_dict(analyzerResult), indent=2, ensure_ascii=False)


        loader = template.Loader("%s/static/template"%PWD)
        self.write(loader.load("analyzer.html").generate(o=result))

class NLUHandler(tornado.web.RequestHandler):
    def get(self):
        result = {"text": "", "result": {}, "nlu_type": "stg"}
        args = self.request.arguments
        print args
        text = ""
        if "text" in args:
            text = args["text"][0].strip()
        result["text"] = text
        nlu_type = "stg"
        if "nlu_type" in args:
            nlu_type = args["nlu_type"][0].strip()
            result["nlu_type"] = nlu_type

        if text:
            nluResult = library.nlu_result(text, _type="aladdin", nlu_type=nlu_type)
        else:
            nluResult = {"exception": "Query is None!!"}
        result["result"] = json.dumps(library._decode_dict(nluResult), indent=2, ensure_ascii=False)

        loader = template.Loader("%s/static/template"%PWD)
        self.write(loader.load("nlu.html").generate(o=result))

settings = dict(
    template_path = os.path.join(os.path.dirname(__file__), "template"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),
)

class SMSHandler(tornado.web.RequestHandler):
    def get(self):
        result = {}
        result["error"] = ""
        result["from"] = ""
        result["to"] = ""
        result["msg"] = ""
        result["agency"] = ""
        result["status"] = 500

        args = self.request.arguments

        _from = "5882"
        _to = ""
        _msg = ""
        _agency = "SKT"
        print args

        if "from" in args:
            _from = args["from"][0]
        if "to" in args:
            _to = args["to"][0]
        if "msg" in args:
            _msg = args["msg"][0].decode("utf-8")
        if "agency" in args:
            _agency = args["agency"][0].upper()

        result["from"] = _from
        result["to"] = _to
        result["msg"] = _msg
        result["agency"] = _agency

        loader = template.Loader("%s/static/template"%PWD)
        self.write(loader.load("sms.html").generate(o=result))

class BaseHandler(tornado.web.RequestHandler):
    def get(self):
        result = {}
        loader = template.Loader("%s/static/template"%PWD)
        self.write(loader.load("main.html").generate(o=result))

class ProxyHandler(tornado.web.RequestHandler):
    def get(self):
        args = self.request.arguments
        if "url" not in args:
            self.write("url parameter require")
            return

        url = args["url"][0]
        f = urllib.urlopen(url)
        data = f.read()
        f.close()
        self.write(data)
        self.set_header('Content-Type', 'application/json')

class ProxyViewHandler(tornado.web.RequestHandler):
    def get(self):
        result = {"result": "Empty Result", "url": ""}
        args = self.request.arguments
        url = ""
        if "url" not in args:
            url = ""
        else:
            url = args["url"][0]
            try:
                f = urllib.urlopen(url)
                data = f.read()
                f.close()
                try:
                    result["result"] = json.dumps(library._decode_dict(json.loads(data)), indent=2, ensure_ascii=False)
                except:
                    result["result"] = data
            except:
                result["result"] = traceback.format_exc()
                pass

        result["url"] = url

        loader = template.Loader("%s/static/template"%PWD)
        self.write(loader.load("proxy.html").generate(o=result))


application = tornado.web.Application([
    (r"/", BaseHandler),
    (r"/poi_search", poi_search.SearchHandler),
    (r"/bypass", bypass.SearchHandler),
    (r"/analyzer", AnalyzerHandler),
    (r"/nlu", NLUHandler),
    (r"/sms", SMSHandler),
    (r"/proxy", ProxyHandler),
    (r"/proxy_view", ProxyViewHandler),
    (r"/query_analyzer", query.query_analyzerHandler),
    (r"/addHost",query.addHostHandler),
    (r"/addKeyword",query.addKeywordHandler),
    (r"/compareResult",query.compareResultHandler),
    (r"/getResult",query.getResultHandler),
    (r"/admin",query.adminHandler),
    (r"/fileUpload",query.fileUploadHandler),
], **settings)

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
