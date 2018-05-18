
import requests
import json
import pymongo
import time
import random


def dmspider(num):
    url = 'https://search.damai.cn/searchajax.html'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0'
    }

    page_num = num
    data = {
        'ctl': '',
        'cty': '',
        'currPage': page_num,
        'order': '',
        'sctl': '',
        'singleChar': '',
        'tn': ''
    }

    response = requests.post(url, data=data, headers=headers)
    # 随机间隔2-3秒
    time.sleep(random.randint(2, 4))
    # 解析信息
    # parse_info(response)
    return response


def parse_info(response):
    jsonobj = json.loads(response.text)
    if jsonobj['pageData']['currentPage'] == jsonobj['pageData']['nextPage']:
        return
    else:
        datas = jsonobj['pageData']['resultData']
        for each_data in datas:
            # print(each_data.keys())
            item = {}
            item['actors'] = each_data['actors']
            item['categoryname'] = each_data['categoryname']
            item['business'] = each_data['business']
            item['cityname'] = each_data['cityname']
            item['description'] = each_data['description']
            item['nameNoHtml'] = each_data['nameNoHtml']
            try:
                item['price_str'] = each_data['price_str']
            except:
                item['price_str'] = '无'
            item['showstatus'] = each_data['showstatus']
            item['showtime'] = each_data['showtime']
            item['subcategoryname'] = each_data['subcategoryname']
            item['subhead'] = each_data['subhead']
            item['venue'] = each_data['venue']
            item['venuecity'] = each_data['venuecity']
            item['id'] = each_data['id']
            yield item


def save_data(items):
    mongo_host = '127.0.0.1'
    mongo_port = 27017
    mongo_database = 'damaiwang'

    mongo_cli = pymongo.MongoClient(host=mongo_host, port=mongo_port)
    mongo_db = mongo_cli[mongo_database]
    for each in items:
        mongo_db.data.insert(each)


def main():
    items = {}
    num = 0
    while items is not False:
        response = dmspider(num)
        items = parse_info(response)
        print('正在保存第%s页信息' % str(num+1))
        save_data(items)
        num += 1


if __name__ == '__main__':
    main()
