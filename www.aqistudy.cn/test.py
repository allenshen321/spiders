

import requests
import execjs
import json
import time

t1 = time.time()
node = execjs.get()

# 参数
# method = 'GETcityweather'
method = 'GETMONTHDATA'
city = '上海'

file = 'getEncryptData.js'
ctx = node.compile(open(file).read())

js = 'getEncryptedData("{0}", "{1}")'.format(method, city)
param = ctx.eval(js)
# print(param)

# Get encrypted response text
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'
}
api = 'https://www.aqistudy.cn/historydata/api/historyapi.php'
response = requests.post(api, data={'hd': param})

# print(response.text)
# print(response.status_code)

# 解密数据
# Decode data
js2 = 'decodeData("{0}")'.format(response.text)
decrypted_data = ctx.eval(js2)
# print(decrypted_data)
jsonobj = json.loads(decrypted_data)
items = jsonobj['result']['data']['items']
# print(items)
for each in items:
    print(each)

print(time.time() - t1)
