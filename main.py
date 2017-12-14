from Extract_list import get_url_list
from info_parser import get_info_cmfd, get_info_cjfq
from multiprocessing import Pool
import time
main_url = {'http://search.cnki.net/Search.aspx?q=%e8%ae%a1%e7%ae%97%e6%9c%ba&rank=relevant&cluster=Type&val=I138&p={}'.format(str(i)) for i in range(0, 322098, 15)}
paper_list = []#已经爬取论文列表


def cnki_spider(db_paper):
    for url in db_paper:
        paper_list.append(url)
        time.sleep(5)
        url_list = get_url_list(url)
        for paper_url in url_list:
            if paper_url.find('CMFD') != -1:
                # print(paper_url)
                get_info_cmfd(paper_url, url)
            elif paper_url.find('CJFD') != -1:
                # print(paper_url)
                get_info_cjfq(paper_url, url)
            elif paper_url.find('CDFD') != -1:
                # print(paper_url)
                get_info_cmfd(paper_url, url)
            elif paper_url.find('CPFD') != -1:
                # print(paper_url)
                get_info_cmfd(paper_url, url)
            else:
                pass

if __name__ == '__main__':
    db_paper_list = []
    #pool = Pool()
    for db_url in main_url:
        db_paper_list.append(db_url)#总共需要爬取的页面数
    try:
        cnki_spider(db_paper_list)
    except None:
        cnki_spider(db_paper_list)
        db_paper_list = set(db_paper_list) - set(paper_list)
        cnki_spider(db_paper_list)

