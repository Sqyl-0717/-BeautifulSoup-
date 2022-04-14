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
main()