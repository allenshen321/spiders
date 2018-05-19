# coding:utf-8
import requests
import json
import random
import queue


def get_ip_port_queue():
    r = requests.get('http://127.0.0.1:8000/?count=10')
    ip_ports = json.loads(r.text)
    print(ip_ports)
    ip_port_queue = queue.Queue(10)
    for each in ip_ports:
        ip_port_queue.put(each[0] + ':' + str(each[1]))
        # ip_port = each[0] + ':' + str(each[1])
        # print(ip_port.split(':')[0])
    return ip_port_queue


if __name__ == '__main__':
    # get_proxy()
    get_ip_port_queue()