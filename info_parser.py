import requests
from bs4 import BeautifulSoup
import time
import pymongo
#url_cjfq = 'http://www.cnki.net/kcms/detail/detail.aspx?dbcode=CJFQ&dbName=CJFQ2008&FileName=KJXX200835679&v=&uid=WEEvREcwSlJHSldRa1FhcTdWZDluYUxSdldSdk5NUDN2UFpyeHEvT1hYbz0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!'
#url_cmfd = 'http://www.cnki.net/kcms/detail/detail.aspx?dbcode=CMFD&dbName=CMFD2011&FileName=2010155745.nh&v=&uid=WEEvREcwSlJHSldRa1FhcTdWZDluYUxSdmdQOXN5Ykw0RG9FVFFVUlI5dz0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!'
hds = {
    'Host': 'www.cnki.net',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    #'Referer': 'http://search.cnki.net/search.aspx?q=%e8%ae%a1%e7%ae%97%e6%9c%ba&rank=relevant&cluster=Type&val=I138',
    #'Cookie':'Ecp_ClientId=3170726174002909526; cnkiUserKey=20e3d87b-ece2-fd54-daa6-0f7dc65a91c7; UM_distinctid=15ea2a5b616\
         #2fa-0ce4323335e2eb-4c322c7f-1fa400-15ea2a5b6173ea; _pk_id=8f1a4d8e-f4ca-467a-8141-45dddc4191a8.1505967484.8.1506070635.1506070635.; _pk_ref=%5B%22%22%2C%22%22%2C1506070635%2C%22http%3A%2F%2Fsearch.cnki.net%2Fsearch.aspx%3Fq%3D%E8%AE%A1%E7%AE%97%E6%9C%BA%26rank%3Drelevant%26cluster%3DType%26val%3DI138%22%5D; SID=91002; LID=WEEvREcwSlJHSldRa1FhcEE0NXdpUDRmNEhkSlRNU0FieHc4aU93TlRJYz0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4ggI8Fm4gTkoUKaID8j8gFw!!; ASP.NET_SessionId=m54vkuu2s3ttjv553uieo545; SID_kcms=202104; UserSeesKcms=%u8BA1%u7B97%u673A%u8F85%u52A9%u6D4B%u91CF%u53CA%u5E94%u7528%u7814%u7A76%21cmfd%21cmfd2011%212010155745.nh%7C%u8BA1%u7B97%u673A%u8F85%u52A9%u6559%u5B66%u7CFB%u7EDF%u7684%u5F00%u53D1%u4E0E%u5E94%u7528%21cmfd%21cmfd2009%212009085133.nh%7C%u6D45%u8BBA%u8BA1%u7B97%u673A%u6280%u672F%u5728%u533B%u5B66%u4E2D%u7684%u5E94%u7528%21cjfq%21cjfq2008%21kjxx200835679%7C',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0'
       }
client = pymongo.MongoClient('localhost', 27017)
Cnki_db = client['Cnki_db']
info = Cnki_db['info']


def get_info_cjfq(paper_url, url):
    hds['Referer'] = url
    #print('正在爬取'+paper_url)
    try:
        wb_data = requests.get(paper_url, headers=hds)
    except:
        print("EXCEPYION("+time.strftime("%Y-%m-%d %H-%M-%S")+"):请求页面异常，休息120s")
        time.sleep(120)
        wb_data = requests.get(paper_url, headers=hds)
    #print(wb_data.text)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    title = soup.select('#chTitle')
    author = soup.select('div.author > p > a')
    summary = soup.select('#ChDivSummary')
    keywords = soup.select('div.keywords > span > a')
    keyword = []
    for k in keywords:
        keyword.append(k.get_text())
    data = {
        'title': title[0].get_text(),
        'author': author[0].get_text(),
        'summary': summary[0].get_text(),
        'keywords': keyword
    }
    info.insert_one(data)


def get_info_cmfd(paper_url, url):
    hds['Referer'] = url
    #print('正在爬取' + paper_url)
    try:
        wb_data = requests.get(paper_url, headers=hds)
    except:
        print("EXCEPYION("+time.strftime("%Y-%m-%d %H-%M-%S")+"):请求页面异常，休息120s")
        time.sleep(120)
        wb_data = requests.get(paper_url, headers=hds)
        print('爬取内容问题解决！')
    #print(wb_data.text)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    title = soup.select('#chTitle')
    author = soup.select('div.summary > p > a ')
    summary = soup.select('#ChDivSummary')
    keywords = soup.select('div.keywords > span > a')
    keyword = []
    for k in keywords:
        keyword.append(k.get_text())
    data = {
        'title': title[0].get_text(),
        'author': author[0].get_text(),
        'summary': summary[0].get_text(),
        'keywords': keyword
    }
    info.insert_one(data)
#get_info_cmfd(url_cmfd)
