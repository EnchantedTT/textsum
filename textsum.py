#encoding:utf-8
#textsum.py
import logging
import requests
import utils
import json
from topic import Topic
import zmq, sys
MODEL_URL = "http://0.0.0.0:7784/translator/translate"

HEADERS = {'content-type': "application/json",}

##
# 预处理所有标题
# 全角标点变换半角，空格变逗号
# 包含数字的字符建立hash
# 返回预处理后结果
##
def prepocess(topics):
	pre_list = []
	for topic in topics:
		topic = topic.strip()
		tp = Topic(topic, comma=True, num=False)
		pre_list.append(tp)
	return pre_list

def stringToDict(topic):
	return {'src':topic}

##
# http 请求接口
# 模型预测
# 输入一组标题
# 返回一组模型预测结果和得分
##
def getModelResults(topics):
	src_list = map(lambda x:stringToDict(x), topics)
	input_data = json.dumps(src_list)
	try:
		response = requests.request("POST", MODEL_URL, data=input_data, headers=HEADERS)
		if response.status_code == 200:
			results = response.json()
			return results
	except:
		return None
	return None

SOCK = zmq.Context().socket(zmq.REQ)
SOCK.connect("tcp://127.0.0.1:5556")
def getModelResultsByTCP(topics):
	src_list = map(lambda x:stringToDict(x), topics)
	input_data = json.dumps(src_list)
	SOCK.send(input_data)
	SOCK.recv()
	return None

def getIndex(w, l):
	if w in l:
		return l.index(w)
	else:
		return -1

def isInSrc(r_words, tp_words):
	flag = True
	for word in r_words:
		if word not in tp_words:
			flag = False
			break
	return flag

def getIndexList(r_words, tp_words):
	index_list = []
	for word in r_words:
		index_list.append(getIndex(word, tp_words))
	#for index, item in enumerate(index_list):
	#	count = 1
	#	while item < 0:
	#		item = index_list[count]
	return index_list

def mapIndex(index, tp_words):
	if index < 0 or index > len(tp_words) - 1:
		return "<UNK>"
	else: return tp_words[index]

def getFinalWords(tp_words, r_words):
	final_words = r_words
	if isInSrc(r_words, tp_words):
		return "".join(r_words)
	index_list =  getIndexList(r_words, tp_words)
	final_words = map(lambda x:mapIndex(x, tp_words), index_list)
	return "".join(final_words)

##
# 后处理单个topic
# 返回单个topic所有结果
##
def postprocessOne(topic, result):
	tp_result = dict()
	tgt = result[u'tgt']
	score = result[u'pred_score']
	r_words = tgt.split(" ")
	final_words = getFinalWords(topic.words, r_words)
	tp_result['src'] = topic.origin
	tp_result['rep'] = topic.rep_string
	tp_result['score'] = score
	tp_result['tgt'] = tgt
	tp_result['result'] = final_words
	return tp_result

##
# 后处理
# 还原大小写，数字
# 处理得分不高的结果
##
def postprocess(topics, results):
	tp_results = []
	for (topic, result) in zip(topics, results):
		tp_result = postprocessOne(topic, result[0])
		tp_results.append(tp_result)
	return tp_results

##
# 批量获取摘要
# 1. 预处理
# 2. 模型输出结果和得分
# 3. 后处理
# 返回摘要集合
##
def getSummarizations(topics):
	results = []
	pre_topics = prepocess(topics)
	model_results = getModelResults(map(lambda x:x.rep_string, pre_topics))
	if model_results:
		results = postprocess(pre_topics, model_results)
	#print "\n".join([t.rep_string for t in pre_topics])
	return results