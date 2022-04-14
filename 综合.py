# -*- coding: utf-8 -*-
#coding=utf-8
import os
import jieba
from collections import Counter
from wordcloud import WordCloud
import numpy as np
from PIL import Image
import string
import requests
import json
from bs4 import BeautifulSoup
import re
import os
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36 FS"}

def get_html(url):
	r = requests.get(url=url, headers=headers)
	r.encoding = r.apparent_encoding
	print("状态：", r.raise_for_status)
	return r.text

def get_json(url):
	r = requests.get(url=url, headers=headers)
	r.encoding = r.apparent_encoding
	print("状态：", r.raise_for_status)
	return r.json()

def get_url_list(json_text):
	url_dict = dict()
	for each in json_text['searchVO']['catMap']['gongwen']['listVO']:
		url_dict[each['url']] = each['title'].replace('<em>','').replace('</em>','')
	for each in json_text['searchVO']['catMap']['otherfile']['listVO']:
		url_dict[each['url']] = each['title'].replace('<em>','').replace('</em>','')
	return url_dict

def get_all_link(key):
	key = str(key.encode()).replace(r'\x', '%').upper()[2:-1]
	url_dict = dict()
	for i in range(10):
		url=f'http://sousuo.gov.cn/data?t=zhengce&q={key}&timetype=timeqb&mintime=&maxtime=&sort=&sortType=1&searchfield=&pcodeJiguan=&childtype=&subchildtype=&tsbq=&pubtimeyear=&puborg=&pcodeYear=&pcodeNum=&filetype=&p={i}&n=5&inpro=&sug_t=zhengce'
		json_text = get_json(url)
		dic = get_url_list(json_text)
		if not dic:
			break
		url_dict.update(dic)
	print(url_dict)
	return url_dict


def save_file(url, title, key):
	text = get_html(url)
	soup = BeautifulSoup(text, 'html.parser')
	try:
		fp = open(f'D:/pycharm/pythonProject/file/{key}/{title}.txt', 'w', encoding='utf-8')
		for each in soup.find_all('p'):
			if each.string:
				fp.writelines(each.string)
		fp.close()
	except:
		print("跳过")
	# for each in soup.find_all('p'):
	#     if each.string:
	#         fp.writelines(each.string)
	#fp.close()

	print("写入成功")




def main():
	key = input("请输入想要搜索的关键字：")
	if not os.path.exists(f'D:/pycharm/pythonProject/file/{key}/'):
		os.makedirs(f'D:/pycharm/pythonProject/file/{key}/')
	url_dict = get_all_link(key)
	for url in url_dict:
		save_file(url, url_dict[url], key)
	class Wordcloud():
		def __init__(self,
					 path,
					 back_coloring_path,
					 save_path,
					 width,
					 height,
					 max_words,
					 min_length,
					 stop_words,
					 background_color='white',
					 font_path="simhei.ttf",
					 cut_all=True,
					 ):
			self.path = path
			self.save_path = save_path
			self.back_coloring_path = np.array(Image.open(back_coloring_path))
			self.width = width
			self.height = height
			self.stop_words = open("E:\\词云\\词云测试1\\stopword.txt",encoding="utf8").read().split("n")
			self.cut_all = cut_all
			self.max_words = max_words
			self.font_path = font_path
			self.background_color = background_color
			self.min_length = min_length

		# 去除标点符号
		def replace_punctutation(self, word):
			# 定义中文标点符号
			punctutations = ['【', '】', '《', '》', '：', '，', '（', '）', '、', '！', '？', '“', '”', "。", ".", "/", "%", "；"]
			# 去除中文标点符号
			for i in punctutations:
				word.replace(i, "")
			# 去除英文标点符号
			for j in string.punctuation:
				word.replace(j, "")
			return word

		# 打开文件，读取文字内容
		def __open_split_file(self, path):
			# 合并所有txt文件内容
			#file_path = self.join_txt(path).replace(u'\xa0', u'')
			file_path = self.join_txt(path)
			file_words = self.open_file(file_path)
			#file_words = file_words.replace(u'\xa0', u'')
			#file_words.encode("gbk", 'ignore').decode("gbk", "ignore")  此方法应为重编码过程，但是一直报错且改不好，删去了，暂不清楚影响

			#self.file.write(file_words.replace(u'\xa0', u''))
			return self.__seg_words(file_words)  # 调用__seg_words方法

		# 打开文件
		def open_file(self, path):
			file_words = []
			with open(path, 'r', encoding='utf-8') as f:
				for i in f.readlines():  # 逐行读入到file_words中
					i = ''.join(i.split())
					file_words.append(i)
			return file_words

		# 进行分词
		def __seg_words(self, file_words):
			seg_lists = []
			for i in file_words:
				seg_list = jieba.cut(i, cut_all=self.cut_all)  # 进行分词，cut_all=True的话分词更精细一些
				seg_lists.extend(seg_list)
				# 遍历每一行
			results = []
			for result in seg_lists:
				result = self.replace_punctutation(result)  # 去除标点符号
				if self.stop_words:
					result = self.delet_words(result)  # 删除指定词
				results.append(result)
			if "" in results:
				results.remove('')  # 去除空值

			return results

		def delet_words(self, word):
			#self.stop_words.add("和")
			self.stop_words = open("E:/词云/词云测试1/stopword.txt", encoding="utf8").read().split("\n")
			for i in self.stop_words:  # 停用词语
				if i in word:
					word = ""
			return word

		# 统计词频
		def __count_words(self, results):
			counter = Counter()  # 初始化一个计数器
			for word in results:
				if len(word) >= self.min_length and word != '\n':
					counter[word] += 1
			return counter

		def word_cloud_and_count_words(self):
			"""
			生成词云图片
			统计词频
			"""
			print("有红字不要怕，正常")
			#stop_words = open("E:\\词云\\词云测试1\\stopwords.txt", encoding="utf8").read().split("n")
			words = self.__open_split_file(self.path)  # 调用open_split_file方法，进行分词
			# 统计词频
			counter = self.__count_words(words)  # 调用count_words方法
			text = ' '.join(words)
			wordcloud = WordCloud(  # 初始化词云对象
				background_color=self.background_color,
				width=self.width,
				height=self.height,
				margin=2,
				max_words=self.max_words,
				mask=self.back_coloring_path,
				font_path=self.font_path,
				random_state=100,
				#stopwords = stop_words
				)  # 设置随机生成多少种配色方案
			# 调用生成词云图方法
			word_cloud = wordcloud.generate(text)
			# 转换成图片
			image = word_cloud.to_image()
			# 保存图片
			image.save(self.save_path)
			return counter, image

		def join_txt(self, path):
			'''
			合并所有的txt文件并写入到一个文件中
			'''
			# 找出当前目录下所有的文件
			file_names = os.listdir(path)
			file = open(os.path.join(path,'results.txt'),'w',encoding='utf-8')
			for file_name in file_names:
				if ".txt" not in file_name:  # 如果后缀不是.txt,直接结束当前迭代，进入下一次迭代
					continue
				else:
					file_path = os.path.join(path, file_name)
					# 遍历单个文件，读取每行内容
					for line in open(file_path, encoding='utf-8'):
						file.writelines(line)
					file.write('\n')  # 每个txt文件的内容用回车键隔开
			file.close()
			# results文件的绝对路径
			path = os.path.join(path, 'results.txt')
			return path


	if __name__ == "__main__":
		# 参数
		args = {
			"path": "E:\\词云\\词云测试1\\1",  # 文本所在的文件夹相对路径
			"back_coloring_path": "E:\词云\词云测试1\\纯色填充.png",  # 背景图路径
			"save_path": "E:\\词云\\词云测试1\\词云图.png",  # 词云图文件保存路径
			"background_color": "white",  # 词云背景图颜色，默认是白色
			"font_path": "simhei.ttf",  # 字体，默认是黑体
			"cut_all": False,  # 是否全分，默认是True
			"width": 300,  # 词云图的宽度
			"height": 400,  # 词云图的高度
			"max_words": 100,  # 最多显示多少词
			"min_length": 2,  # 词语最短长度
			"stop_words": "和" # 停用词语，直接往里添加list
		}
		word_cloud = Wordcloud(**args)
		counter, image = word_cloud.word_cloud_and_count_words()
		print(counter)
		image.show()
main()