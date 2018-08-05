"""
模块功能说明：
（1）用于对网页解析，包括两个部分：
    1）tag页面的解析
        args： html，
        return url
    2）图书页面信息的解析
        args: html
        return info_book={} #字典
"""
from bs4 import  BeautifulSoup
"""
传入参数： html
"""
class parser_html(object):
    def __init__(self, html):
        self.html = html

    def tag_html_parse(self):
        try:
            soup = BeautifulSoup(self.html, 'lxml')
            wrapper = soup.find(id='wrapper')
            """
            try:
                h1 = wrapper.find('h1').string
                #print(h1)
            except:
                print("H1出错")
            """

            tag_list = wrapper.find(class_="").find_all(class_="")
            for tag in tag_list:
                #这里会出错，需要使用try 。。。 except。。 结构来避免错误
                """
                try:
                    h2 = tag.find('h2').string
                    #print(h2)
                except:
                    pass
                """

                for td in tag.find_all('td'):
                    item = {'name': td.find('a').string,          #标签名称
                            'link': td.find('a').attrs['href'],   #标签链接
                            'num_p': td.find('b').string.replace('(','').replace(')',''),  #评价人数 
                            }
                    #print(item)
                    #yield item    #返回的链接应该是可以直接用的
                    url = self.normalzie_url(item['link'])
                    yield url  #这是每个标签页的首页链接   
        except:
            #这里只会因为代理无法使用的问题产生问题，不会因为其他的问题产生问题, 记录这里可以继续增加东西
            pass 
    def normalzie_url(self,link):
        """
        对 url 进行完整化
        """
        #这里产生的 url 是每个标签首页的url 
        seed_url = "https://book.douban.com/"
        url = seed_url + link
        return url

    def book_info(self):
        global count_book
        global blank_page_count  
        
        try:
            soup = BeautifulSoup(html, 'lxml')
            wrapper = soup.find(id='wrapper')
            s_list = wrapper.find(class_='subject-list').find_all(class_='subject-item')
            for li in s_list:
                info = li.find(class_='info')
                try:
                    title = info.find('h2').find('a').string.strip()
                except:
                    title = None
                try:
                    pub = info.find(class_='pub').string.strip()
                except:
                    pub = info.find(class_='pub').string
                try:
                    rat_num = info.find(class_="star").find(class_="rating_nums").string
                except:
                    rat_num = None
                try:
                    pl = info.find(class_='star').find(class_='pl').string.strip()
                except:
                    pl = info.find(class_='star').find(class_='pl').string
                try:
                    cont = info.find('p').string
                except:
                    cont = None
                item_book = {
                    'title': title,
                    'link': info.find('h2').find('a').attrs['href'],
                    'pub' : pub,
                    'rat_num' : rat_num,
                    'pl' :pl,
                    'cont': cont,
                    }
                count_book += 1
                print("已经爬到第",count_book,'本书')
                print(item_book)  #将图书的信息打印出来
                #info_save(item_book)  #保存信息
                return item_book       #返回图书信息
                
        except:
            """
                如果结果没有找到合适的信息，则开始进行新的解析，同时返回 “没有找到符合条件的图书”
            """
            try:
                soup = BeautifulSoup(html, 'lxml')
                subject_list = soup.find(id='subject-list')
                p = subject_list.find(class_='p12').string    #找到合适的信息
                return p  #返回合适的信息
            except:
                #执行到这里的时候，只能说明这是一个 None 的html            
                print("解析出错")