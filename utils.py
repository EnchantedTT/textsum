#encoding:utf-8
#import logging
#import settings
import jieba
import sys
import os
import re

zhPattern = re.compile(u'[\u4e00-\u9fa5]+')

def fullToHalf(s):
	n = []
	for char in s:
		num = ord(char)
		if num == 0x3000:
			num = 32
		elif 0xFF01 <= num <= 0xFF5E:
			num -= 0xfee0
		num = unichr(num)
		n.append(num)
	return ''.join(n)

def spacesToComma(topic):
	return re.sub(r'\s+', ',', topic)

def numsToToken(word):
	return re.sub(br'\d', '0', word)

def replaceCaseAndNums(words):
	return [numsToToken(w).lower() for w in words]

def tokenizer(sentence):
	jieba_words = list(jieba.cut(sentence))
	words = []
	for w in jieba_words:
		if zhPattern.search(w):
			words.extend(list(w))
		else:
			words.append(w)
	return words