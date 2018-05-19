# 爬取网址
url = https://tieba.baidu.com/f?

# 爬取的keyword
kw = {'kw': '美腿', 'ie': 'utf-8', 'tab': 'good', 'pn': 50}

# 每页的帖子url， xpath


# 只看楼主的url　链接是在关键字中加入see_lz=1

# 判断每个页面下的最后链接是否是 ’尾页‘
//div[@class="l_thread_info"]/ul[@class="l_posts_num"]/li[@class="l_pager pager_theme_4 pb_list_pager"]/a[last()]/text()

#　每个帖子的中页面的关键字
pn = 2

# 每页帖子中图片的链接
//img[@class="BDE_Image"]/@src


