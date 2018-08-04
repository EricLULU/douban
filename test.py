import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import random
import string 
import pymongo 
import win32com.client
import winsound

# 定义全局变量
count_book = 0          # 记录一共有多少书
blank_page_count = 0  #记录空余页面次数


#定义数据库的连接，完成数据库的初始化连接
client = pymongo.MongoClient("mongodb://localhost:27017/")   #客户端初始化
db = client.douban               #定义数据库
collection = db.book_fourth         #定义数据库中的表
Referer_url_list = []            #只存两个链接  

#定义全局列表，用于存储每个标签下的链接
#tag_list = []



def downloader(url, num_retries=1):
    """
        html 页面下载
    """
    #proxies = proxies_get()  #获取代理
    #cookies = cookies_get()  #获取随机的cookies
    #User_Agent = user_agent_create()  #获取一个随机的代理
    headers, proxies= headers_and_proxy(url)

    #尝试下载html页面
    try:
        #requests = requests.Session()
        #print("开始下载:", url)
        response = requests.get(url, proxies=proxies, headers=headers)  #设置代理和请求头
        time.sleep(random.random()*10)
    except:
        if num_retries >0:
            print("重新下载", url)
            downloader(url, num_retries-1)  #开始重新下载
        else:
            print("下载失败")
            return None    #返回None
    else:
        if response.status_code == 200 and len(response.text) > 2000:
        #下载成功后，返回html
        #tag_parser(response.content)
            #print(response.text)
            return response.text
        else:
            print(response.status_code)
            print(len(response.text))
            print(response.text)
            if num_retries > 0:
                downloader(url, num_retries-1)  #开始重新下载




def proxies_get(num_retries=3):
    proxies_url = "http://localhost:5555/random"
    try:
        print("正在获取代理")
        r = requests.get(proxies_url)
        print(r.text)
    except:
        if num_retries > 0:
            print("正在获取代理")
            proxies_get(num_retries-1)
        else:
            print("代理获取失败")
    else:
        proxy = r.text
        proxies = {'http://': 'http' + proxy,
                   'https://': 'https' + proxy}
        return proxies, proxy




def user_agent_create():
    """
    产生代理
    func： 返回随机的代理
    """
    user_agent_list = user_agent_list = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
    # iPhone 6：
    "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",
    ]
    User_Agent = random.choice(user_agent_list)
    return User_Agent    




def headers_and_proxy(url):
    """
    获取 cookies 和 proxy，同时返回这两个数据
    利用proxy 来获取代理，同时利用代理来获取cookies，将cookies返回，利用此cookies来爬取数据
    """
    proxies = proxies_get()[0]     #获取代理, requests 使用的代理
    #proxy = proxies_get()[1]       #获取代理，selenium 使用的代理
    User_Agent = user_agent_create()  #获取 user_agent
    headers = {'User_Agent':User_Agent} 
    r = requests.get(url, proxies=proxies, headers=headers)
    cookies_list = []   #用来存储cookie
    for key, value in r.cookies.items():
        cookie = '{}{}{}'.format(key,'=',value)   #合成cookie
        cookies_list.append(cookie)
    cookies = ','.join(cookies_list)     #cookies 设置

    """
    service_args = ['--proxy='+proxy,'--proxy-type=http']
    browser = webdriver.PhantomJS(service_args=service_args)    #获取浏览器,并设置代理
    browser.get(url)      #爬取url
    cookie_list = browser.get_cookies()    #获取cookies
    c_list = []  #cookies 的存储列表
    for cookie in cookie_list:
        c = cookie['name'] + '=' + cookie['value']
        c_list.append(c)
    cookies = ','.join(c_list)
    """
    #headers = {'User_Agent':User_Agent, 'cookies':cookies}   #headers设置
    headers = {
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding' : 'gzip, deflate, sdch, br',
            'Accept-Language' : 'zh-CN,zh;q=0.8',
            'Connection' : 'keep-alive',
            'Cookie' : cookies,                                                         #'ll="129059"; bid=LGKvV4eiPRo; __yadk_uid=mdRyurjdvN9YpaTediph1fGvXm5kFwDv; Hm_lvt_16a14f3002af32bf3a75dfe352478639=1530035976; ps=y; viewed="27186423_30155720_26830570_30230525"; ct=y; douban-fav-remind=1; _ga=GA1.2.136521292.1532742322; push_noty_num=0; push_doumail_num=0; ue="1937745693@qq.com"; ap=1; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1532879802%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_id.100001.3ac3=b18d25a7c828ec36.1532746268.9.1532879802.1532876147.; _pk_ses.100001.3ac3=*; gr_user_id=aed55e35-108a-4a89-804c-b544ce17eb7f; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=bf17d7dc-0031-4da1-8625-dd6400142110; gr_cs1_bf17d7dc-0031-4da1-8625-dd6400142110=user_id%3A0; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_bf17d7dc-0031-4da1-8625-dd6400142110=true; __utmt_douban=1; __utma=30149280.136521292.1532742322.1532875198.1532879802.11; __utmb=30149280.1.10.1532879802; __utmc=30149280; __utmz=30149280.1532875198.10.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.16455; __utmt=1; __utma=81379588.849084421.1532746268.1532875200.1532879802.9; __utmb=81379588.1.10.1532879802; __utmc=81379588; __utmz=81379588.1532875200.8.8.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _vwo_uuid_v2=D6DD576F3726815F082BD613DE8AA2E9E|fd53ca50e9b535c18b508c8560eba809',
            'Host' : 'book.douban.com',
            'User-Agent' : User_Agent,
            'Referer':'https://www.douban.com',
            }
    return headers, proxies           #f返回cookies 和 proxy，最好可以返回headers， 开始进行修改



def cookies_get():
    bid = ''.join(random.sample(string.ascii_letters + string.digits, 11))    #获取随机的11位数
    first_sq = 'll="129059;'
    second_sq = 'bid='+ bid + ';'
    third_sq = '__yadk_uid=mdRyurjdvN9YpaTediph1fGvXm5kFwDv; Hm_lvt_16a14f3002af32bf3a75dfe352478639=1530035976; ps=y; viewed="27186423_30155720_26830570_30230525"; ct=y; douban-fav-remind=1; _ga=GA1.2.136521292.1532742322; push_noty_num=0; push_doumail_num=0; ue="1937745693@qq.com"; ap=1; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1532879802%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_id.100001.3ac3=b18d25a7c828ec36.1532746268.9.1532879802.1532876147.; _pk_ses.100001.3ac3=*; gr_user_id=aed55e35-108a-4a89-804c-b544ce17eb7f; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=bf17d7dc-0031-4da1-8625-dd6400142110; gr_cs1_bf17d7dc-0031-4da1-8625-dd6400142110=user_id%3A0; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_bf17d7dc-0031-4da1-8625-dd6400142110=true; __utmt_douban=1; __utma=30149280.136521292.1532742322.1532875198.1532879802.11; __utmb=30149280.1.10.1532879802; __utmc=30149280; __utmz=30149280.1532875198.10.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.16455; __utmt=1; __utma=81379588.849084421.1532746268.1532875200.1532879802.9; __utmb=81379588.1.10.1532879802; __utmc=81379588; __utmz=81379588.1532875200.8.8.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _vwo_uuid_v2=D6DD576F3726815F082BD613DE8AA2E9E|fd53ca50e9b535c18b508c8560eba809'
    cookies = first_sq + second_sq + third_sq  #获取一个随机的cookies
    return cookies



def tag_parser(html):
    """
        tag_html 页面解析， 用于返回每个 tag 首页的链接，
        ex: 这里只使用了一个url， 不会存在 url 溢出的问题
    """
    #因为 html 有可能为 None,导致解析失败，故而需要使用 try。。。。 except 结构
    try:
        soup = BeautifulSoup(html, 'lxml')
        wrapper = soup.find(id='wrapper')
        try:
            h1 = wrapper.find('h1').string
            print(h1)
        except:
            print("H1出错")

        tag_list = wrapper.find(class_="").find_all(class_="")
        for tag in tag_list:
            #这里会出错，需要使用try 。。。 except。。 结构来避免错误
            try:
                h2 = tag.find('h2').string
                print(h2)
            except:
                pass

            for td in tag.find_all('td'):
                item = {'name': td.find('a').string,          #标签名称
                        'link': td.find('a').attrs['href'],   #标签链接
                        'num_p': td.find('b').string.replace('(','').replace(')',''),  #评价人数 
                        }
                #print(item)
                #yield item    #返回的链接应该是可以直接用的
                url = normalzie_url(item['link'])
                yield url  #这是每个标签页的首页链接   
    except:
        #这里只会因为代理无法使用的问题产生问题，不会因为其他的问题产生问题
        pass 
        




def normalzie_url(link):
    """
    对 url 进行完整化
    """
    #这里产生的 url 是每个标签首页的url 
    seed_url = "https://book.douban.com/"
    url = seed_url + link
    return url 




def info_save(item):
    global collection        #声明集合
    """
        html_parser 信息解析后的存储或者打印
    """
    try:
        if collection.insert(item):
            print("保存成功")
    except:
        print("保存失败")




def url_produce(url):
    """
        url 产生， 用于产生每个标签页下的图书页面 url 的迭代 
    """
    params = "?start="
    for i in range(51):
        url_tag = "{}{}{}".format(url, params, i*20)
        yield url_tag    #产生迭代值





def info_book_get(html):
    """
        解析函数： 用来提取图书信息
        图书可以提取的信息包括： 
        书名， 出版信息，评分，参与评分人数， 内容简介 
        que：  每个标签下的图书的页码是不同的，有的会多，有的会少，因此，有的页面会解析不到数据，从而产生错误，因此，可以将结果返回为False， 加以判断
        return info_book, 或者是 False, 其中false 用于判断，而 info 则是用于存储
    """

    # 声明全局变量
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
            print(item_book)  #将图书的信息打印出来
            info_save(item_book)  #保存信息
            print("已经爬到第",count_book,'本书')
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
            pass

        """
        if blank_page_count > random.randint(0,3):    #是否大于一个任意的随机整数
            blank_page_count = 0                      #重新初始化
            return False                              #此时已经解析失败
        else:
            blank_page_count += 1               
        """




def main():
    """
        主函数， 也就是调度函数

    """
    global Referer_url_list   #声明全局列表
    count = 0   #链接计数
    url = "https://book.douban.com/tag/"
    html = downloader(url)
    link_tag = tag_parser(html)
    Referer_url_list.append(url)

    #开始下载每个标签页下面的图书信息
    for url in link_tag:
        for url_tag in url_produce(url):
            print(url_tag)
            Referer_url_list.append(url_tag) 
            count += 1
            html_book_list = downloader(url_tag)
            condition = info_book_get(html_book_list) #判断条件
            
            if condition == "没有找到符合条件的图书":
                #如果已经翻到最后一页， 那么可以终止此次爬取
                break



            """
            if not info_book_get(html_book_list):
                break
            else:
                pass
                #存储函数
            """
            #print(url_tag)   #这里已经可以找到每一个标签页的链接，接下来只需要编写解析的函数即可
            #print("url总数：", count)
        #downloader(url)

    #print_tag_url(url_tag)

def make_alarm():
    speak = win32com.client.Dispatch('SAPI.SPVOICE')
    #winsound.Beep(2015, 3000)
    flag = 0
    while True:
        speak.Speak('eric,程序运行完毕!')
        if flag < 3:
            flag += 1
        else:
            break

if __name__ == '__main__':
    count_book = 0

    start_time = time.time()  #定义起始时间
    print(count_book)

    main()
    print("书的总数是：", count_book)

    end_time = time.time() #记录结束时间
    print("总的耗时:", end_time - start_time)
    make_alarm()   #调用警报声