# coding=utf-8

from selenium import webdriver
driver = webdriver.PhantomJS(executable_path=r"E:\Program Files\JetBrains\phantomjs-2.1.1-windows\bin\phantomjs.exe")
driver.get("http://www.toutiao.com")

print type(driver.page_source)
fo = open("aaaa1.html", "wb")
fo.write(driver.page_source.encode('utf8'))
fo.close()
driver.quit()

