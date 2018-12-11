'''
此程序用于爬取腾讯动漫的漫画
腾讯动漫采用异步加载的方法动态加载动漫
本程序使用seleuium + Chrome自动化爬取
也可以使用phantomjs 等无界面的方式爬取，本文为了演示使用Chrome
作者:鲁戈
联系方式：15203659186@163.com
本文仅供学习交流所用
'''

from selenium import webdriver
import requests
import os,sys
import time

class Tencent(object):
  def __init__(self,url='https://ac.qq.com/ComicView/index/id/505430/cid/101'):
    #当前文件路径
    self.path = os.path.dirname(os.path.realpath(sys.argv[0]))
    #设置消息头
    self.headers = {"User-Agent":"Mozilla/5.0"}
    #传入要爬取的url
    #测试页面，腾讯动漫海贼王第一话
    self.url = url
    
    #保存图片地址
    self.img_list = []
    #创建浏览器对象,注意exe文件路径问题
    self.driver = webdriver.Chrome() 

  def open_url(self):
    self.driver.get(self.url)
    #先切换至对页模式，因为腾讯动漫采用异步加载模式且使用driver.execute_script()方法无法操作界面，所以为了方便，可切换到对页模式
    self.driver.find_element_by_id('crossPage').click()
    self.img_xpath()

  def img_xpath(self):
    #匹配所有的漫画元素,即使没有加载成功，也有元素结构,匹配结果用于计算页面页数
    img_src = self.driver.find_elements_by_xpath('//*[@id="comicContainCross"]/li/div[1]/div/img')

    
    if self.url == 'https://ac.qq.com/ComicView/index/id/505430/cid/1':
      for _ in range(len(img_src)-1):
      #点击下一页，完成异步加载,加载时间一定要给合适的一些,不然异步可能无法加载
        time.sleep(1.5)
        next = self.driver.find_element_by_id('crossLeft')
        next.click()
      self.get_img_url()
    else:
      for _ in range(len(img_src)):
        #点击下一页，完成异步加载,加载时间一定要给合适的一些,不然异步可能无法加载
        time.sleep(1.5)
        next = self.driver.find_element_by_id('crossLeft')
        next.click()
      self.get_img_url()
    

    
  def get_img_url(self):
    #重新获取页面元素，此时，异步加载已经结束，匹配每一个img
    img_src = self.driver.find_elements_by_xpath('//*[@id="comicContainCross"]/li/div/div/img')
    for img_url in img_src:
      self.img_list.append(img_url.get_attribute('src'))
    
    #打印测试
    # for url in self.img_list:
    #   print(url)
    if self.img_list:
      self.save_img()


  def save_img(self):
    #图片文件名字拼接
    img_num = 10001
    #文件夹名字拼接
    # dir = 1001
    # while True:
    #   mkdir = self.path + '\\' + str(dir)
    #   #判断文件夹是否存在，避免文件夹名称冲突
    #   if os.path.exists(mkdir):
    #     dir += 1
    #   else:
    #     os.mkdir(mkdir)
    #     break
    
    #文件夹名字拼接2，使用url命名
    dir = 1000
    dir = dir + int(self.url.split('/')[-1])
    mkdir = self.path + '\\' + str(dir)
    os.mkdir(mkdir)
    for url in self.img_list[::-1]:
      #由于网络问题，肯能会有某些没有加载的元素
      if url:
        res = requests.get(url,headers=self.headers)
        html = res.content
        u_list = url.split('.')
        filename = mkdir +'\\'+ str(img_num) + '.' + u_list[-1][:-2]
        # print(filename)
        img_num += 1
        with open(filename,'wb') as f:
          f.write(html)


  def work_on(self):
    #开始工作
    self.open_url()
    self.driver.quit()
    

if __name__ == '__main__':
  spider = Tencent()
  spider.work_on()