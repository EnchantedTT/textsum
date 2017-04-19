#encoding:utf-8
import utils
#import logging

class Topic():
	def __init__(self, topic, comma=False, num=False):
		self.origin = topic

		# 全角变半角
		half_topic = utils.fullToHalf(topic)

		# 空格变逗号
		self.rep_topic = half_topic
		if comma:
			self.rep_topic = utils.spacesToComma(half_topic)

		# 分字
		self.words = utils.tokenizer(self.rep_topic)

		# 变换大小写和数字
		self.rep_words = [w.lower() for w in self.words]
		if num:
			self.rep_words = utils.replaceCaseAndNums(self.words)

		self.len = len(self.rep_words)
		self.rep_string = " ".join(self.rep_words).strip()

	def results():
		pass

