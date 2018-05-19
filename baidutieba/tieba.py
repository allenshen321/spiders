# encoding: utf-8

import requests
from lxml import etree


class TiebaSpider():
    def __init__(self):

        # self.keyword = raw_input('请输入访问的贴吧：')
        # self.start_num = int(raw_input('请输入起始页：'))
        # self.end_num = int(raw_input('请输入终止页：'))
        self.keyword = input('请输入访问的贴吧:')
        self.start_num = int(input('请输入起始页:'))
        self.end_num = int(input('请输入终止页:'))

        # 保存每个帖子的urls
        self.urls_set = set()

        self.base_url = 'https://tieba.baidu.com'

        self.url = 'https://tieba.baidu.com/f'
        self.params = {
            'kw': self.keyword,
            'tab': 'good',
        }

        self.headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1 Trident/5.0;'}

    def get_urls(self):
        '''爬出所有的帖子的url网址'''
        urls = []
        for page_num in range(self.start_num, self.end_num+1):
            pn = 50 * (page_num - 1)
            self.params['pn'] = pn
            response = requests.get(self.url, params=self.params, headers=self.headers)
            html = etree.HTML(response.text)
            urls_list = html.xpath('//div[@class="threadlist_lz clearfix"]/div/a/@href')
            urls += urls_list
        self.urls_set = set(urls)

    def parse(self):
        """解析每个帖子"""
        for url in self.urls_set:
            page_num = 1
            full_url = self.base_url + url
            # 设置只看楼主 即关键字中see_lz = 1
            params = {'see_lz': 1, 'pn': page_num}

            # 用来保存每个帖子中的所有图片的url
            pic_urls = []

            # 爬取每个帖子的html
            response = requests.get(full_url, params=params, headers=self.headers)

            # xpath解析
            html = etree.HTML(response.text)
            # 帖子中，每页中的图片的url
            pic_url = html.xpath('//img[@class="BDE_Image"]/@src')
            pic_urls += pic_url

            is_next_page = html.xpath('//ul[@class="l_posts_num"]/li/a[last()]/text()')
            if is_next_page != []:
                while is_next_page[0] == '尾页':
                    page_num += 1
                    next_page_params = {'see_lz': 1, 'pn': page_num}
                    next_page_response = requests.get(full_url, params=next_page_params, headers=self.headers)
                    next_page_html = etree.HTML(next_page_response.text)
                    next_page_pic_url = next_page_html.xpath('//img[@class="BDE_Image"]/@src')
                    pic_urls += next_page_pic_url

                    is_next_page = next_page_html.xpath('//ul[@class="l_posts_num"]/li/a[last()]/text()')
            pic_urls = set(pic_urls)

            # 保存图片
            self.save_pic(pic_urls)

    def save_pic(self, pic_urls):
        pic_num = 0
        for url in pic_urls:
            filepath = 'tieba_pic/meitui-2/' + url[-14:-4] + '.jpg'
            pic = open(filepath, 'wb')
            response = requests.get(url, headers=self.headers)
            pic.write(response.content)
            pic.close()

            pic_num += 1
            print('以保存%d个图片' % pic_num)


if __name__ == '__main__':
    tieba = TiebaSpider()
    tieba.get_urls()
    tieba.parse()
