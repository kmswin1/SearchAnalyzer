#-*- coding: utf-8 -*-
import sys
import json
import os
import urllib2
import traceback

#NLU_API = "http://10.40.97.88:6737/nlp//nlu/"
NLU_API = "http://223.39.121.167:7738/nlp/kr/nlu/"
NLU_PRD_API = "http://10.40.92.158:47738/nlp/kr/nlu/"
#NLU_PRD_API = "http://172.27.98.144:47738/nlp/kr/nlu/"
def _decode_list(data):
	rv = []
	for item in data:
		if isinstance(item, unicode):
			item = item.encode('utf-8')
		elif isinstance(item, list):
			item = _decode_list(item)
		elif isinstance(item, dict):
			item = _decode_dict(item)
		rv.append(item)
	return rv

def _decode_dict(data):
	rv = {}
	for key, value in data.iteritems():
		if isinstance(key, unicode):
			key = key.encode('utf-8')
		if isinstance(value, unicode):
			value = value.encode('utf-8')
		elif isinstance(value, list):
			value = _decode_list(value)
		elif isinstance(value, dict):
			value = _decode_dict(value)
		rv[key] = value
	return rv

def nlu_result(query, _type="music", user_id="", nlu_type="stg", device_type="spk"):
	nluQuery = {"meta": {"engine_result": "false", "client_system": "kv_farm", "service_type": _type, "device_type": device_type, "output_format": "simple_nlu"}, "nlu_input": [{"text": query}]}
	if user_id:
		user_id = user_id[:20]
		nluQuery["client"] = {"additional":{}}
		nluQuery["client"]["additional"]["userId"] = user_id
	try:
		api = NLU_API
		if nlu_type == "prd":
			api = NLU_PRD_API
		print api
		request = urllib2.Request(api, json.dumps(nluQuery), {'Content-Type': 'application/json'})
		f = urllib2.urlopen(request, timeout=1)
		nluResult = json.loads(f.read(), "utf-8")
		f.close()
		return nluResult
	except:
		print traceback.format_exc()
		return {}



#a= nlu_result("하현수씨에게 전화해줘", _type="aladdin", user_id="ALDESQA7MR18EDB429FA", nlu_type="prd", device_type="tmap_app")
#print json.dumps(a, ensure_ascii=False, indent=2)
