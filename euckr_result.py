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
def run(host, keyword, resultname, basicQuery, repeatQuery, jsonPath):
    result = ""
    if jsonPath != "":
        jsonpath_expr = parse(jsonPath)
    with open(os.path.join(keyword), 'r') as f:
        query = host + basicQuery
        tempQ = query
        req = requests.get(query)
        ret = req.text
        ret = json.loads(ret)
        if req.status_code == 200:
            result += (tempQ + " : OK\n")
            result += ("검색결과 갯수 : ")
            result += str(ret["response"]["rows"])
            result += "\n"
        else:
            result += (tempQ + " : Not OK\n")
        repeatQuery = repeatQuery.split("&")
        basicQuery = basicQuery.split("&")
        while(True):
            line = f.readline()
            if not line: break
            for basicQ in basicQuery:
                for repeatQ in repeatQuery:
                    temp = basicQ.split("=")
                    temp = temp[0]
                    if repeatQ == temp:
                        tempQ = query.replace(basicQ,(repeatQ + "=" + line))
            req = requests.get(tempQ)
            ret = req.text
            ret = json.loads(ret)
            if req.status_code == 200:
                result += (tempQ+" : OK\n")
                result += ("검색결과 갯수 : ")
                result += str(ret["response"]["rows"])
                result += "\n"
            else:
		        result += (tempQ+" : Not OK\n")
    print result

    with open(os.path.join(BASE_DIR, resultname), 'w+') as result_file:
        result_file.write(result)

