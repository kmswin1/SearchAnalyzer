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
import requests


ENGINE_ACCOUNT = "poi"
reload(sys)
sys.setdefaultencoding('utf-8')


PWD = os.path.dirname(os.path.realpath(__file__))
params =  {}
class SearchHandler(tornado.web.RequestHandler):
    def makeDocument(self, result, search_result):
        newDocument = []


        try:

            result["query"] = search_result.get("request").get("user_query")
            result["total_count"] = search_result.get("response").get("num_found")
            result["search_api"] = search_result.get("search_api")

            documents = search_result["response"]["docs"]
            for idx, doc in enumerate(documents):
                doc["idx"] = idx + 1
                doc["address"] = doc["lcd_name"] + ' ' + doc["mcd_name"] + ' ' + doc["road_name"] + ' ' + doc["bld_no1"]
                if doc.get("class_nm_data") != None:
                    cateName = doc.get("class_nm_data").split(" ")[0]
                    arr = cateName.split(":")
                    doc["disCate"] = " > ".join(arr[1:len(arr)-1])
                else:
                    doc["disCate"] = ""

                if doc.get("phone_data") != None:
                    doc["disPhone"] = doc.get("phone_data").split(" ")[0]
                else:
                    doc["disPhone"] = ""

                if doc.get("distance") != None:
                    if float(doc.get("distance")) < 1.0:
                        doc["disDistance"] = str(int(float(doc.get("distance")*1000)) ) + " m"
                    else:
                        doc["disDistance"] = str(round(float(doc.get("distance")), 1)) + " km"
                else:
                    doc["disDistance"] = ""



                newDocument.append(doc)
        except:
            print traceback.format_exc()
        return newDocument


    def fieldCheck(self, doc, field):
        val = doc.get(field)

        if val == None:
            return ""

        return val


    def makeDocumentAlly(self, result, search_result):
        newDocument = []

        try:

            result["query"] = search_result.get("nlu_result")[0].get("text")
            result["total_count"] = search_result.get("hits").get("total")
            result["search_api"] = search_result.get("search_api")

            documents = search_result["hits"]["hits"]
            for idx, doc in enumerate(documents):
                temp = doc.get("fields")
                doc = doc.get("_source")

                doc["idx"] = idx + 1

                doc["place_name"] = self.fieldCheck(doc, "place_name")

                doc["address"] = self.fieldCheck(doc, "lcd_name") + ' ' + self.fieldCheck(doc,"mcd_name") + ' ' + self.fieldCheck(doc, "road_name") + ' ' + self.fieldCheck(doc, "bld_no1")
                if doc.get("class_nm_data") != None:
                    cateName = doc.get("class_nm_data").split(" ")[0]
                    arr = cateName.split(":")
                    doc["disCate"] = " > ".join(arr[1:len(arr)-1])
                else:
                    doc["disCate"] = ""

                if doc.get("phone_data") != None:
                    doc["disPhone"] = doc.get("phone_data").split(" ")[0]
                else:
                    doc["disPhone"] = ""

                if doc.get("distance") != None:
                    if float(doc.get("distance")) < 1.0:
                        doc["disDistance"] = str(int(float(doc.get("distance")*1000)) ) + " m"
                    else:
                        doc["disDistance"] = str(round(float(doc.get("distance")), 1)) + " km"
                else:
                    doc["disDistance"] = ""

                if 'CNS' not in doc.get("nav_type"):
                    doc["nav_wgs84_lat"] = doc["pns_wgs84_lat"]
                    doc["nav_wgs84_lon"] = doc["pns_wgs84_lon"]
                    doc["nav_wgs84"] = doc["pns_wgs84"]

                doc["fields"] = temp
                newDocument.append(doc)
        except:
            print traceback.format_exc()
        return newDocument


    def makeDocumentDev(self, result, search_result):
        newDocument = []

        try:

            print search_result
            result["query"] = search_result.get("request").get("query")
            result["total_count"] = search_result.get("response").get("total_count")
            result["search_api"] = search_result.get("search_api")

            documents = search_result["response"]["docs"]
            for idx, doc in enumerate(documents):
                temp = doc.get("fields")
                doc = doc.get("_source")

                doc["idx"] = idx + 1

                doc["place_name"] = self.fieldCheck(doc, "place_name")

                doc["address"] = self.fieldCheck(doc, "lcd_name") + ' ' + self.fieldCheck(doc,"mcd_name") + ' ' + self.fieldCheck(doc, "road_name") + ' ' + self.fieldCheck(doc, "bld_no1")
                if doc.get("class_nm_data") != None:
                    cateName = doc.get("class_nm_data").split(" ")[0]
                    arr = cateName.split(":")
                    doc["disCate"] = " > ".join(arr[1:len(arr)-1])
                else:
                    doc["disCate"] = ""

                if doc.get("phone_data") != None:
                    doc["disPhone"] = doc.get("phone_data").split(" ")[0]
                else:
                    doc["disPhone"] = ""

                if doc.get("distance") != None:
                    if float(doc.get("distance")) < 1.0:
                        doc["disDistance"] = str(int(float(doc.get("distance")*1000)) ) + " m"
                    else:
                        doc["disDistance"] = str(round(float(doc.get("distance")), 1)) + " km"
                else:
                    doc["disDistance"] = ""

                if 'CNS' not in doc.get("nav_type"):
                    doc["nav_wgs84_lat"] = doc["pns_wgs84_lat"]
                    doc["nav_wgs84_lon"] = doc["pns_wgs84_lon"]
                    doc["nav_wgs84"] = doc["pns_wgs84"]

                doc["fields"] = temp
                newDocument.append(doc)
        except:
            print traceback.format_exc()
        return newDocument

    def search_es(self, api, query, SEARCH_TYPE):
        try:
            send_data = {}

            send_data["q"] = query

            if SEARCH_TYPE == "prd":
                send_data["coord.user.x"] = params["x"]
                send_data["coord.user.y"] = params["y"]
                send_data["coord.user.type"] = "bessel_tmap"
                send_data["coord.focus.x"] = params["x"]
                send_data["coord.focus.y"] = params["y"]
                send_data["coord.focus.type"] = "bessel_tmap"

                send_data["fl.group"] = "all"
                send_data["referrer_code"] = "TP780"
                send_data["additional_results"] = "area_name_list"
                send_data["rows"] = params["rows"]
            elif SEARCH_TYPE == "ally":
                send_data["coord.user.x"] = params["x"]
                send_data["coord.user.y"] = params["y"]
                send_data["coord.user.type"] = "bessel_tmap"
                send_data["coord.focus.x"] = params["x"]
                send_data["coord.focus.y"] = params["y"]
                send_data["coord.focus.type"] = "bessel_tmap"
                send_data["n"] = params["rows"]
                send_data["type"] = params["type"]
            else:
                send_data["user.x"] = params["x"]
                send_data["user.y"] = params["y"]
                send_data["user.type"] = "bessel_tmap"
                send_data["focus.x"] = params["x"]
                send_data["focus.y"] = params["y"]
                send_data["focus.type"] = "bessel_tmap"
                send_data["n"] = params["rows"]
                send_data["p"] = params["p"]
                send_data["debug"] = params["debug"]

            print api + "?" + urllib.urlencode(send_data)
            #req = urllib2.Request(api, urllib.urlencode(send_data), {'Content-Type': 'application/x-www-form-urlencoded'})
            f = urllib2.urlopen(api + "?" +  urllib.urlencode(send_data) , timeout=3)
            result = f.read()
            search_result = json.loads(result)

            search_result["search_api"] = api + "?" + urllib.urlencode(send_data)
            f.close()

            return search_result
        except:
            print traceback.format_exc()
            return {}



    def result_init(self):
        result = {}

        result["total_count"] = 0
        result["documents"] = []
        result["url"] = ""
        result["result_type"] = "search"
        result["search_api"] = ""
        result["action_type"] = ""
        result["frame_name"] = ""



        return result


    def params_init(self):
        global params

        params["q"] = ""
        params["p"] = "1"
        params["frame_1"] = "T_PRD"
        params["frame_2"] = "K"
        params["frame_3"] = "G"
        params["x"] = ""
        params["y"] = ""
        params["rows"] = ""
        params["search_type"] = ""
        params["debug"] = "true"
        params["type"] = ""

        return params


    def makeResultProd(self, result, query):
        try:
            SEARCH_API = ""
            SEARCH_TYPE = ""
            if result["action_type"] == 'T_PRD':
                SEARCH_API = "http://172.27.108.24:8080/tmap/1.0/search/poi.json"
                SEARCH_TYPE = "prd"
            elif result["action_type"] == 'T_ALLY':
                SEARCH_API = "http://d-tsch-os02:7777/poi/search"
                SEARCH_TYPE = "ally"
            else:
                SEARCH_API = "http://d-tsch-os03:8001/poi/search"
                SEARCH_TYPE = "dev"

            search_result = self.search_es(SEARCH_API, query, SEARCH_TYPE)

        except:
            print traceback.format_exc()

        try:
            new_document = []
            if result["action_type"] == 'T_PRD':
                new_document = self.makeDocument(result, search_result)
            elif result["action_type"] == 'T_ALLY':
                new_document = self.makeDocumentAlly(result, search_result)
            elif result["action_type"] == 'T_DEV':
                new_document = self.makeDocumentDev(result, search_result)
            result["documents"] = new_document
        except:
            print traceback.format_exc()
            pass


        return result





    def makeGoogleSearch(self, result, query):
        API = "https://dapi.kakao.com/v2/local/search/keyword.json?y=37.514322572335935&x=127.06283102249932&query=" + query

        result["documents"] = []
        result["url"] = API
        result["search_api"] = API
        return result


    def makeGoogleSearchFrame(self, result, query):
        result["url"] = "https://www.google.co.kr/maps/search/" + query
        result["search_api"] = "https://www.google.co.kr/maps/search/" + query
        result["result_type"] = "frame"

        return result


    def makeKakaoSearch(self, result, query):
        API = "https://dapi.kakao.com/v2/local/search/keyword.json"

        send_data = {"y":37.514322572335935, "x":127.06283102249932, "query":query}

        try:
            request = urllib2.Request(API, urllib.urlencode(send_data), headers={'Authorization': 'KakaoAK e5297385eb6cae85d959172a6d2f9d60', 'Content-Type': 'application/x-www-form-urlencoded'})
            response = urllib2.urlopen(request)
            search_result = response.read()

        except:
            print traceback.format_exc()
            return {}

        rObj = json.loads(search_result)

        result["url"] = API
        result["total_count"] = rObj.get("meta").get("total_count")

        newDocument = []
        documents = rObj["documents"]
        for idx, doc in enumerate(documents):
            doc["idx"] = idx + 1
            doc["name_org"] = doc["place_name"]
            doc["pkey"] = doc["id"]
            doc["cate_nm_t2"] = doc["category_name"]
            doc["address"] = doc["road_address_name"]
            doc["nav_wgs84_lon"] = doc["x"]
            doc["nav_wgs84_lat"] = doc["y"]

            newDocument.append(doc)

        result["documents"] = newDocument
        result["result_type"] = "search"

        return result


    def makeKakaoSearchFrame(self, result, query):
        result["url"] = "http://map.daum.net/?q=" + query
        result["search_api"] = "http://map.daum.net/?q=" + query
        result["result_type"] = "frame"

        return result


    def makeNaverSearch(self, result, query):
        API = "https://openapi.naver.com/v1/search/local.json"

        send_data = { "query": "1", "display" : "10", "start" : "1"}

        try:
            request = urllib2.Request(API, urllib.urlencode(send_data))
            request.add_header('X-Naver-Client-Id', '7QiBlwSQpCH4VgtESHJq')
            request.add_header('X-Naver-Client-Secret', 'vL3qHP_qrU')
            print request
            response = urllib2.urlopen(request)
            search_result = response.read()

        except:
            print traceback.format_exc()
            return {}

        print search_result
        return
        rObj = json.loads(search_result)

        result["url"] = API
        result["total_count"] = rObj.get("meta").get("total_count")

        newDocument = []
        documents = rObj["documents"]
        for idx, doc in enumerate(documents):
            doc["idx"] = idx + 1
            doc["name_org"] = doc["place_name"]
            doc["pkey"] = doc["id"]
            doc["cate_nm_t2"] = doc["category_name"]
            doc["address"] = doc["road_address_name"]
            doc["nav_wgs84_lon"] = doc["x"]
            doc["nav_wgs84_lat"] = doc["y"]

            newDocument.append(doc)

        result["documents"] = newDocument

        return result


    def makeNaverSearchFrame(self, result, query):
        result["url"] = "https://map.naver.com/?query=" + query
        result["search_api"] = "https://map.naver.com/?query=" + query
        result["result_type"] = "frame"

        return result

    def emptyFrame(self, result, query):

        return result

    def makeQA(self):
        send_data = {}
        qa = {}
        send_data["query"] = params["q"]
        API = "http://10.40.103.214:9001/hydra/local/analyzer.json?"+urllib.urlencode(send_data)

        try:
            request = urllib2.Request(API)
            response = urllib2.urlopen(request)
            search_result = response.read()
            qa = json.loads(search_result)
            qa["url"] = "http://10.40.103.214:9001/hydra/local/analyzer.json?query="+params["q"]
            return qa

        except:
            print traceback.format_exc()
            return {}

    def get(self, local_args={}, local=False):
        lonlat = {"lon":"", "lat":""}
        self.set_header('X-FRAME-OPTIONS', 'SAMEORIGIN')

        params = self.params_init()
        result_frame1 = self.result_init()
        result_frame2 = self.result_init()
        result_frame3 = self.result_init()

        if local:
            args = local_args
        else:
            args = self.request.arguments

        for key in args:
            params[key] = args[key][0].strip()

        query = params["q"]
        qa = self.makeQA()
        if params.get("center") != None and "," in params["center"]:
            arr = params["center"].split(",")
            params["x"] = arr[0]
            params["y"] = arr[1]
            lon = params["x"]
            lat = params["y"]
            payload = {'appKey': '9b2ecdb3-9215-45cb-bd2b-dff4f24892cf', 'lon': lon, 'lat': lat, 'fromCoord': 'BESSEL',
                       'toCoord': 'WGS84GEO'}
            ret = requests.get('https://api2.sktelecom.com/tmap/geo/coordconvert', params=payload)
            ret = ret.json()
            lonlat["lon"] = ret["coordinate"]["lon"]
            lonlat["lat"] = ret["coordinate"]["lat"]
            print
            lonlat

        if query:
            switcher = {
                "T_PRD": self.makeResultProd,
                "T_DEV": self.makeResultProd,
                "T_ALLY": self.makeResultProd,
                "G": self.makeGoogleSearchFrame,
                "K": self.makeKakaoSearchFrame,
                "N": self.makeNaverSearchFrame
            }
            frame_names = {
                "T_PRD": "T map 검색 상용",
                "T_DEV": "T map 검색 내재화",
                "T_ALLY": "Ally 전용",
                "G": "Google",
                "K": "Kakao",
                "N": "Naver"
            }

            try:
                result_frame1["action_type"] = params["frame_1"]
                result_frame1["frame_name"] = frame_names[params["frame_1"]]
                func1 = switcher.get(params["frame_1"], self.emptyFrame)
                result_frame1 = func1(result_frame1, query)

                result_frame2["action_type"] = params["frame_2"]
                result_frame2["frame_name"] = frame_names[params["frame_2"]]
                func2 = switcher.get(params["frame_2"], self.emptyFrame)
                result_frame2 = func2(result_frame2, query)

                result_frame3["action_type"] = params["frame_3"]
                result_frame3["frame_name"] = frame_names[params["frame_3"]]
                func3 = switcher.get(params["frame_3"], self.emptyFrame)
                result_frame3 = func3(result_frame3, query)
            except:
                print
                "result_frame is empty"

        loader = template.Loader("%s/static/template" % PWD)
        self.write(loader.load("poi_search.html").generate(r1=result_frame1, r2=result_frame2, r3=result_frame3, p=params, qa=qa, lonlat=lonlat))


