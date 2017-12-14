import requests
from bs4 import BeautifulSoup
import time
#urls = 'http://search.cnki.net/search.aspx?q=%e8%ae%a1%e7%ae%97%e6%9c%ba&rank=relevant&cluster=Type&val=I138'
hds = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}


def get_url_list(url):
    print(url)
    try:
        wb_data = requests.get(url, headers=hds)
    except None:
        print("EXCEPYION("+time.strftime("%Y-%m-%d %H-%M-%S")+"):请求页面异常，休息120s")
        time.sleep(120)
        wb_data = requests.get(url, headers=hds)
        print('爬取列表问题解决！')
    soup = BeautifulSoup(wb_data.text, 'lxml')
    all_url_list = soup.select('div.wz_content > h3 > a')
    url_list = []
    for i in all_url_list:
        if "http://epub.cnki.net/" in i.get('href'):
            url_list.append(i.get('href'))
        else:
            pass
    #print('爬完一页啦！')
    print(url_list)
    return url_list

#get_url_list(urls)

