import requests
from bs4 import BeautifulSoup
import re
import os
key = 1
i = 1
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36 FS"}
url = f'http://sousuo.gov.cn/data?t=zhengce&q={key}&timetype=timeqb&mintime=&maxtime=&sort=&sortType=1&searchfield=title&pcodeJiguan=&childtype=&subchildtype=&tsbq=&pubtimeyear=&puborg=&pcodeYear=&pcodeNum=&filetype=&p={i}&n=5&inpro='
# def get_key_url(key):
#     #url = 'http://sousuo.gov.cn/s.htm?t=zhengce&q='+str(key.encode()).replace(r'\x', '%').upper()[2:-1]+'&timetype=timeqb&mintime=&maxtime=&sort=&sortType=1&searchfield=&pcodeJiguan=&childtype=&subchildtype=&tsbq=&pubtimeyear=&puborg=&pcodeYear=&pcodeNum=&filetype=&p=0&n=5&inpro=&sug_t=zhengce'
#     url = f'http://sousuo.gov.cn/data?t=zhengce&q=%E7%89%B9%E8%89%B2%E5%86%9C%E4%BA%A7%E5%93%81&timetype=&mintime=&maxtime=&sort=score&sortType=1&searchfield=&pcodeJiguan=&childtype=&subchildtype=&tsbq=&pubtimeyear=&puborg=&pcodeYear=&pcodeNum=&filetype=&p=0&n=5&inpro='
#     return url


def get_html(url):
    r = requests.get(url=url, headers=headers)
    r.encoding = r.apparent_encoding
    print("状态：", r.raise_for_status)
    return r.text


def get_url_list(text, url_dict):
    soup = BeautifulSoup(text, 'html.parser')
    block = soup.find_all('div', attrs={'class': 'dys_middle_result_content'})
    collect = re.findall('<a href="(.*?)" onclick=".*?" target="_blank">(.*?)<span class="date">', str(block[0]))
    for i, j in collect:
        url_dict[i] = j.replace('<em>','').replace('</em>','')
    return url_dict

def get_json(url):
    r = requests.get(url=url, headers=headers)
    r.encoding = r.apparent_encoding
    print("状态：", r.raise_for_status)
    #print(get_json(url))
    #json_text = get_json(url)
    #print(json_text)
    #print(type(json_text))
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
        url=f'http://sousuo.gov.cn/data?t=zhengce&q={key}&timetype=timeqb&mintime=&maxtime=&sort=&sortType=1&searchfield=title&pcodeJiguan=&childtype=&subchildtype=&tsbq=&pubtimeyear=&puborg=&pcodeYear=&pcodeNum=&filetype=&p={i}&n=5&inpro='
        json_text = get_json(url)
        dic = get_url_list(json_text)
        if not dic:
            break
        url_dict.update(dic)
    return url_dict
    return url


def main():
    key = input("请输入要输入的关键字：")
    #url = get_key_url(key)
    text = get_html(url)
    #print(url)
    #print(text[:100])


    soup = BeautifulSoup(text, 'html.parser')
    soup.find_all('div', attrs={'class': 'dys_middle_result_content'})
    block = soup.find_all('div', attrs={'class': 'dys_middle_result_content'})
    #collect = re.findall('<a href="(.*?)" onclick=".*?" target="_blank">(.*?)<span class="date">', str(block[0]))
    url_dict = {}
    url_dict.update(get_url_list(url_dict))
    print(url_dict)
    key_list = url_dict.keys()
    print(list(key_list))
    #print("")

main()
