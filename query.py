#-*- coding: utf-8 -*-
import sys
import json
import os
import urllib2
import urllib
import pprint
import traceback
import library
import tornado
import tornado.ioloop
import tornado.web
import tornado.template as template
import time
import pymysql
import euckr_result
import utf8_result
import utf8_compare
import euckr_compare

reload(sys)
sys.setdefaultencoding('utf-8')
ENGINE_ACCOUNT = "query_analyzer"

PWD = os.path.dirname(os.path.realpath(__file__))


class query_analyzerHandler(tornado.web.RequestHandler):
    def get(self):
        result = {}
        loader = template.Loader("%s/static/template"%PWD)
        self.write(loader.load("query_analyzer.html").generate(o=result))

class addHostHandler(tornado.web.RequestHandler):
    def get(self):
        conn = pymysql.connect(host='10.40.103.211', port=9380, user='eunheekim', password='Tmapsearch1!@',
                               db='QueryAnalyzer', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        getHostSql = "select * from Hosts"
        curs.execute(getHostSql)
        hosts = curs.fetchall()
        result = {}
        loader = template.Loader("%s/static/template"%PWD)
        self.write(loader.load("addHost.html").generate(o=result, hosts=hosts))
        print "getting host data success"
        conn.close()

    def post(self):
        conn = pymysql.connect(host='10.40.103.211', port=9380, user='eunheekim', password='Tmapsearch1!@',
                               db='QueryAnalyzer', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        jsonObj = json.loads(self.request.body)
        print 'post host data received'

        sql = "insert into Hosts(hostname, hostinfo, encoding, doctype) values(%s, %s, %s, %s)"
        curs.execute(sql,(jsonObj["hostname"],jsonObj["hostinfo"],jsonObj["encoding"],jsonObj["doctype"]))
        conn.commit()
        print "inserting host data success"
        conn.close()

    def delete(self):
        conn = pymysql.connect(host='10.40.103.211', port=9380, user='eunheekim', password='Tmapsearch1!@',
                               db='QueryAnalyzer', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        jsonObj = json.loads(self.request.body)
        sql = "delete from Hosts where id = %s"
        curs.execute(sql,(jsonObj["id"]))
        conn.commit()
        print "deleting host data success"
        conn.close()

class addKeywordHandler(tornado.web.RequestHandler):
    def get(self):
        conn = pymysql.connect(host='10.40.103.211', port=9380, user='eunheekim', password='Tmapsearch1!@',
                               db='QueryAnalyzer', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        getKeywordSql = "select * from Keywords"
        curs.execute(getKeywordSql)
        keywords = curs.fetchall()
        result = {}
        loader = template.Loader("%s/static/template"%PWD)
        self.write(loader.load("addKeyword.html").generate(o=result, keywords=keywords))
        print "getting keyword data success"
        conn.close()

    def post(self):
        conn = pymysql.connect(host='10.40.103.211', port=9380, user='eunheekim', password='Tmapsearch1!@',
                               db='QueryAnalyzer', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        jsonObj = json.loads(self.request.body)
        print 'post keyword data received'

        sql = "insert into Keywords(keywordbody, keywordinfo, keywordname) values(%s, %s, %s)"
        keybody = "/home/eunheekim/service/models/keywordfiles/" + jsonObj["keywordname"]
        curs.execute(sql,(keybody, jsonObj["keywordinfo"],jsonObj["keywordname"]))
        conn.commit()
        print "inserting keyword data success"
        conn.close()

    def delete(self):
        conn = pymysql.connect(host='10.40.103.211', port=9380, user='eunheekim', password='Tmapsearch1!@',
                               db='QueryAnalyzer', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        jsonObj = json.loads(self.request.body)
        sql = "delete from Keywords where id = %s"
        curs.execute(sql,(jsonObj["id"]))
        conn.commit()
        print "deleting keyword data success"
        conn.close()

class getResultHandler(tornado.web.RequestHandler):
    def get(self):
        conn = pymysql.connect(host='10.40.103.211', port=9380, user='eunheekim', password='Tmapsearch1!@',
                               db='QueryAnalyzer', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        getHostSql = "select * from Hosts"
        curs.execute(getHostSql)
        hosts = curs.fetchall()
        getKeywordSql = "select * from Keywords"
        curs.execute(getKeywordSql)
        keywords = curs.fetchall()
        getResultSql = "select * from Results"
        curs.execute(getResultSql)
        results = curs.fetchall()
        result = {}
        loader = template.Loader("%s/static/template"%PWD)
        self.write(loader.load("getResult.html").generate(o=result, hosts=hosts, keywords=keywords, results=results))
        print "getting result data success"
        conn.close()

    def post(self):
        conn = pymysql.connect(host='10.40.103.211', port=9380, user='eunheekim', password='Tmapsearch1!@',
                               db='QueryAnalyzer', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        jsonObj = json.loads(self.request.body)
        print 'post result data received'
        bq = jsonObj["basicquery"]
        rq = jsonObj["repeatquery"]
        resultname = jsonObj["resultname"]
        resultbody = "/home/eunheekim/service/models/resultfiles/" + jsonObj["resultname"]
        getHostSql = "select hostname from Hosts where id = %s"
        curs.execute(getHostSql,(jsonObj["hostid"]))
        host = curs.fetchone()
        getKeywordSql = "select keywordbody from Keywords where id = %s"
        curs.execute(getKeywordSql,(jsonObj["keywordid"]))
        keyword = curs.fetchone()
        if jsonObj["encoding"] == "utf-8":
            utf8_result.run(host["hostname"],keyword["keywordbody"],resultname,bq,rq,jsonObj["jsonpath"])
        else:
            euckr_result.run(host["hostname"],keyword["keywordbody"],resultname,bq,rq,jsonObj["jsonpath"])


        sql = "insert into Results(resultname, resultbody, encoding, jsonpath, resulttype) values(%s, %s, %s, %s, %s)"
        curs.execute(sql,(resultname,resultbody,jsonObj["encoding"],jsonObj["jsonpath"],"추출"))
        conn.commit()
        print "inserting result data success"
        conn.close()

class compareResultHandler(tornado.web.RequestHandler):
    def get(self):
        conn = pymysql.connect(host='10.40.103.211', port=9380, user='eunheekim', password='Tmapsearch1!@',
                               db='QueryAnalyzer', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        getHostSql = "select * from Hosts"
        curs.execute(getHostSql)
        hosts = curs.fetchall()
        getKeywordSql = "select * from Keywords"
        curs.execute(getKeywordSql)
        keywords = curs.fetchall()
        getResultSql = "select * from Results"
        curs.execute(getResultSql)
        results = curs.fetchall()
        result = {}
        loader = template.Loader("%s/static/template"%PWD)
        self.write(loader.load("compareResult.html").generate(o=result, hosts=hosts, keywords=keywords, results=results))
        print "getting compare data success"
        conn.close()

    def post(self):
        conn = pymysql.connect(host='10.40.103.211', port=9380, user='eunheekim', password='Tmapsearch1!@',
                               db='QueryAnalyzer', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        jsonObj = json.loads(self.request.body)
        print 'post compare data received'
        fbq = jsonObj["firstbasicquery"]
        frq = jsonObj["firstrepeatquery"]
        sbq = jsonObj["secondbasicquery"]
        srq = jsonObj["secondrepeatquery"]
        resultname = jsonObj["resultname"]
        resultbody = "/home/eunheekim/service/models/resultfiles/" + jsonObj["resultname"]
        getHostSql = "select hostname from Hosts where id = %s"
        curs.execute(getHostSql,(jsonObj["firsthostid"]))
        fhost = curs.fetchone()
        curs.execute(getHostSql,(jsonObj["secondhostid"]))
        shost = curs.fetchone()
        getKeywordSql = "select keywordbody from Keywords where id = %s"
        curs.execute(getKeywordSql,(jsonObj["keywordid"]))
        keyword = curs.fetchone()
        if jsonObj["encoding"] == "utf-8":
            utf8_compare.run(keyword["keywordbody"],fhost["hostname"],fbq,frq,shost["hostname"],sbq,srq,resultname,jsonObj["jsonpath"])
        else:
            euckr_compare.run(keyword["keywordbody"],fhost["hostname"],fbq,frq,shost["hostname"],sbq,srq,resultname,jsonObj["jsonpath"])

        sql = "insert into Results(resultname, resultbody, encoding, resulttype) values(%s, %s, %s, %s)"
        curs.execute(sql,(jsonObj["resultname"], resultbody, jsonObj["encoding"], "비교"))
        conn.commit()
        print "inserting compare data success"
        conn.close()

class adminHandler(tornado.web.RequestHandler):
    def get(self):
        conn = pymysql.connect(host='10.40.103.211', port=9380, user='eunheekim', password='Tmapsearch1!@',
                               db='QueryAnalyzer', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        getResultSql = "select * from Results"
        curs.execute(getResultSql)
        results = curs.fetchall()
        result = {}
        loader = template.Loader("%s/static/template"%PWD)
        self.write(loader.load("admin.html").generate(o=result, results=results))
        print "getting admin data success"
        conn.close()

    def delete(self):
        conn = pymysql.connect(host='10.40.103.211', port=9380, user='eunheekim', password='Tmapsearch1!@',
                               db='QueryAnalyzer', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        jsonObj = json.loads(self.request.body)
        sql = "select resultbody from Results where id = %s"
        curs.execute(sql,(jsonObj["id"]))
        path = curs.fetchone()
        path = path["resultbody"]
        os.remove(path)
        sql = "delete from Results where id = %s"
        curs.execute(sql,(jsonObj["id"]))
        conn.commit()
        print "deleting admin data success"
        conn.close()

    def put(self):
        jsonObj = json.loads(self.request.body)
        path = jsonObj["resultbody"]
        print "post resultbody data received"
        with open(path, 'r') as f:
            ret = ""
            while (True):
                line = f.readline()
                if not line: break
                ret += (line+"<br>")
        self.write(ret)




class fileUploadHandler(tornado.web.RequestHandler):
    def get(self):
        result = {}
        loader = template.Loader("%s/static/template"%PWD)
        self.write(loader.load("fileUpload.html").generate(o=result))
        print "getting file data success"

    def post(self):
        conn = pymysql.connect(host='10.40.103.211', port=9380, user='eunheekim', password='Tmapsearch1!@',
                               db='QueryAnalyzer', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        fileinfo = self.request.files
        bodyinfo = self.request.body
        print "fileinfo is", fileinfo
        print "bodyinfo is", bodyinfo
        print 'post file data received'

        print 'file is saved'
        self.get()
        conn.close()
