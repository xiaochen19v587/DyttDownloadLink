import random
import time
import requests
from fake_useragent import UserAgent
from lxml import etree
import  execjs


class Dytt_xpath(object):
    def __init__(self):
        self.url = 'https://www.dytt8.net/html/gndy/dyzz/list_23_{}.html'
        self.headers = {
            'User-Agent':UserAgent().random
        }
    
    # 获取内容并解析
    def get_analyze(self,url,xpath_str):
        html = requests.get(url=url,headers=self.headers).content.decode('gbk','ignore')
        parse_html = etree.HTML(html)
        lists = parse_html.xpath(xpath_str)
        return lists
    
    # 提取一级页面链接
    def parse_page1(self,url):
        link_xpath_str = '//div[@class="co_content8"]//table[@class="tbspan"]//b/a/@href'
        data_link_list = self.get_analyze(url,link_xpath_str)
        name_xpath_str = '//div[@class="co_content8"]//table[@class="tbspan"]//b/a/text()'
        data_name_list = self.get_analyze(url,name_xpath_str)
        for i in range(len(data_link_list)):
            data_link = 'https://www.dytt8.net'+data_link_list[i]
            moive_name=data_name_list[i]
            ftpLink = self.parse_page2(data_link)
            downLink = self.readJs(ftpLink)
            movieInfo = moive_name+' '+downLink
            with open('DyttDownLink.txt','a+')as f:
                f.writelines(movieInfo)
                f.writelines('\n')

    def readJs(self,ft_url):
        with open('Dytt_base64.js', 'r')as f:
            file = f.read()
        res = execjs.compile(file).call('ThunderEncode', ft_url)
        return res

    # 获取二级页面下载链接
    def parse_page2(self,data_link):
        xpath_str='''
            //div[@class="bd3r"]//div[@class="co_content8"]//table//a/@href
        '''
        downLinks = self.get_analyze(data_link,xpath_str)
        return downLinks[0]

    # 主函数
    def main(self):
        for page in range(1,10):
            url = self.url.format(page)
            self.parse_page1(url)
            print('第{}页完成.'.format(page))
            time.sleep(random.randint(1,3))

if __name__ == "__main__":
    start = time.time()
    spi = Dytt_xpath()
    spi.main()
    end = time.time()
    print('执行时间:%.2fs'%(end-start))
