#-*- coding: euc-kr -*-
import requests
from bs4 import BeautifulSoup
import json
import os
import sys
from jsonpath_rw import jsonpath, parse

reload(sys)
sys.setdefaultencoding('euc-kr')

BASE_DIR = "/home/eunheekim/service/models/resultfiles"
def run(keyword, f_host, f_basicQuery, f_repeatQuery, s_host, s_basicQuery, s_repeatQuery, resultname, jsonPath):
    result = ""
    if jsonPath != "":
        jsonpath_expr = parse(jsonPath)
    with open(os.path.join(keyword), 'r') as f:
        f_query = f_host + f_basicQuery
        f_tempQ = f_query
        s_query = s_host + s_basicQuery
        s_tempQ = s_query
        f_req = requests.get(f_query)
        s_req = requests.get(s_query)
        f_repeatQuery = f_repeatQuery.split("&")
        f_basicQuery = f_basicQuery.split("&")
        s_repeatQuery = s_repeatQuery.split("&")
        s_basicQuery = s_basicQuery.split("&")
	f_ret = f_req.text
	f_ret = json.loads(f_ret)
	s_ret = s_req.text
	s_ret = json.loads(s_ret)
	result += ("first docid : " + f_ret["response"]["docs"][0]["pkey"] + " second docid : " + s_ret["response"]["docs"][0]["pkey"] + "\n")
        if f_req.status_code == 200 and s_req.status_code == 200:
            result += (f_tempQ + " : OK \n" + s_tempQ + " : OK \n")
            result += ("첫번째 검색결과 갯수 : ")
            result += str(f_ret["response"]["rows"])
	    result += "\n"
            result += (" 두번째 검색 결과 갯수 : ")
            result += str(s_ret["response"]["rows"])
            result += "\n\n"
        elif f_req.status_code ==200 and s_req.status_code != 200:
            result += (f_tempQ + " : OK \n" + s_tempQ + " : Not OK \n")
            result += ("첫번째 검색결과 갯수 : ")
            result += str(f_ret["response"]["rows"])
	    result += "\n"
            result += (" 두번째 검색 결과 갯수 : ")
            result += str(s_ret["response"]["rows"])
            result += "\n\n"
        elif f_req.status_code != 200 and s_req.status_code == 200:
            result += (f_tempQ + " : Not OK \n" + s_tempQ + " : OK \n")
            result += ("첫번째 검색결과 갯수 : ")
            result += str(f_ret["response"]["rows"])
	    result += "\n"
            result += (" 두번째 검색 결과 갯수 : ")
            result += str(s_ret["response"]["rows"])
            result += "\n\n"
        else:
            result += (f_tempQ + " : Not OK \n" + s_tempQ + " : Not OK \n")
            result += ("첫번째 검색결과 갯수 : ")
            result += str(f_ret["response"]["rows"])
	    result += "\n"
            result += (" 두번째 검색 결과 갯수 : ")
            result += str(s_ret["response"]["rows"])
            result += "\n\n"
        while (True):
            line = f.readline()
            if not line: break
            for f_basicQ in f_basicQuery:
                for f_repeatQ in f_repeatQuery:
                    f_temp = f_basicQ.split("=")
                    f_temp = f_temp[0]
                    if f_repeatQ == f_temp:
                        f_tempQ = f_query.replace(f_basicQ, (f_repeatQ + "=" + line))
            f_req = requests.get(f_tempQ)
            f_ret = f_req.text
            f_ret = json.loads(f_ret)
            for s_basicQ in s_basicQuery:
                for s_repeatQ in s_repeatQuery:
                    s_temp = s_basicQ.split("=")
                    s_temp = s_temp[0]
                    if s_repeatQ == s_temp:
                        s_tempQ = s_query.replace(s_basicQ, (s_repeatQ + "=" + line))
            s_req = requests.get(s_tempQ)
            s_ret = s_req.text
            s_ret = json.loads(s_ret)
            result += ("first docid : " + f_ret["response"]["docs"][0]["pkey"] + " second docid : " + s_ret["response"]["docs"][0]["pkey"] + "\n")
	    if f_req.status_code == 200 and s_req.status_code == 200:
                result += (f_tempQ + " : OK \n" + s_tempQ + " : OK \n")
                result += ("첫번째 검색결과 갯수 : ")
                result += str(f_ret["response"]["rows"])
		result += "\n"
                result += (" 두번째 검색 결과 갯수 : ")
                result += str(s_ret["response"]["rows"])
                result += "\n\n"
            elif f_req.status_code == 200 and s_req.status_code != 200:
                result += (f_tempQ + " : OK \n" + s_tempQ + " : Not OK \n")
                result += ("첫번째 검색결과 갯수 : ")
                result += str(f_ret["response"]["rows"])
		result += "\n"
                result += (" 두번째 검색 결과 갯수 : ")
                result += str(s_ret["response"]["rows"])
                result += "\n\n"
            elif f_req.status_code != 200 and s_req.status_code == 200:
                result += (f_tempQ + " : Not OK \n" + s_tempQ + " : OK \n")
                result += ("첫번째 검색결과 갯수 : ")
                result += str(f_ret["response"]["rows"])
		result += "\n"
                result += (" 두번째 검색 결과 갯수 : ")
                result += str(s_ret["response"]["rows"])
                result += "\n\n"
            else:
                result += (f_tempQ + " : Not OK \n" + s_tempQ + " : Not OK \n")
                result += ("첫번째 검색결과 갯수 : ")
                result += str(f_ret["response"]["rows"])
		result += "\n"
                result += (" 두번째 검색 결과 갯수 : ")
                result += str(s_ret["response"]["rows"])
                result += "\n\n"
    print result

    with open(os.path.join(BASE_DIR, resultname), 'w+') as result_file:
        result_file.write(result)
