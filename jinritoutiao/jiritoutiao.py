# encoding: utf-8

from .new_getASCP import getASCP
import requests
import json
import jsonpath
import re
# from HTMLParser import HTMLParser
from html.parser import HTMLParser
import time


def get_url(min_behot_time=0):
    url = 'https://www.toutiao.com/api/pc/feed/?'
    AS,CP = getASCP()
    print('as='+AS)
    print('cp='+CP)
    cookies = {
        'tt_webid' : '6486077894102943246',
        'Domain' : '.toutiao.com',
        'Max - Age' : '7804800',
        'Path' : '/'
    }
    params = {
        'category': 'news_society',
        'utm_source': 'toutiao',
        'widen': '1',
        'max_behot_time': min_behot_time,
        'max_behot_time_tmp': min_behot_time,
        'tadrequire': 'true',
        'as': AS,
        'cp': CP
    }
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0"
    }

    response = requests.get(url, params=params, headers=headers, cookies=cookies)
    print('requests的url:'+response.url.encode('utf-8'))
    html = json.loads(response.text)
    # 提取新闻链接并调用parse_html()函数解析响应内容
    link_list = jsonpath.jsonpath(html, '$..data')[0]
    # 遍历url，解析响应中的内容
    for each in link_list:
        link = each['source_url']
        if link.startswith('/group/'):
            parse_html(link)
            print('完成解析网页：' + str(link))
    # 提取下一页的时间戳
    next_hot_time = jsonpath.jsonpath(html, 'next.max_behot_time')[0]
    print(next_hot_time)
    #time.sleep(3)
    get_url(next_hot_time)

def parse_html(url):
    """解析每个新闻链接，提取内容"""
    url = 'https://www.toutiao.com' + url
    print (url)
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0"
    }
    response = requests.get(url, headers=headers)
    # 提取文章的标题
    patterm = re.compile(r"title: '(.*?)',")
    title_list = patterm.findall(response.content)
    title = ''
    for each in title_list:
        title += each
    #print title
    # 提取文章的内容
    patterm_content = re.compile(r"content: '(.*?)',")
    content_list = patterm_content.findall(response.content)
    # 将文本列表转成字符串格式
    content = ''
    for each in content_list:
        content += each.strip()
    # 创建一个HTMLparse对象，处理content中的转义字符

    html_parser = HTMLParser()
    html = html_parser.unescape(content)
    #print html
    # 解析html中的文本
    new_pattern = re.compile(r'<p>(.*?)</p>')
    new_text = new_pattern.findall(html)
    article = ''
    for each in new_text:
        article += each.strip()
    #print article
    # 保存数据 title,article
    save_data(title, article)

def save_data(title, content):
    if '/' in list(title):
        title.replace('/','_')
    file_path = 'data/news_society/' + title.decode() + '.txt'
    print(file_path)
    try:
        with open(file_path, 'w') as f:
            f.write(title.decode() + '\n' + content.decode())
    except Exception as e:
        print(e)

if __name__ == '__main__':
    get_url()
