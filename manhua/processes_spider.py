'''
此程序用于爬取腾讯动漫的漫画
本文在于之前的基础上，采用多进程/多线程，也可以两个并用的方式，效率爬取
经过测试,即使采用多线程，由于异步加载的原因，效率也和网络速度挂钩
总体来说，使用selenium + Chrome效率还是很低，但是对异步加载有方便的优势
作者:鲁戈
联系方式：15203659186@163.com
本文仅供学习交流所用
'''

from spider import *
from multiprocessing import Pool


def worker(url):
  spider = Tencent(url)
  spider.work_on()

if __name__ == '__main__':
  pool = Pool(processes=4)
  url_head = 'https://ac.qq.com/ComicView/index/id/505430/cid/'
  url_list = [url_head+str(i) for i in range(1,946)]
  for url in url_list:
    r = pool.apply_async(func=worker,args=(url,))

  pool.close()
  pool.join()