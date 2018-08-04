import requests
from PIL import image
from bs4 import beautifulSoup

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Referer':'https://accounts.douban.com/login?alias=&redir=https%3A%2F%2Fwww.douban.com%2F&source=index_nav&error=1001'

}

session = r.Session()
#添加headers
session.headers.update(headers)
user_name = input("输入账号：")
password = input("输入密码：")

def login(user_name, password, source='index_nav', redir='https://www.douban.com/', login='登入'):
    caprcha_id,caprcha_link = get_captcha(url)          #把get_captcha函数返回的值,获取验证码的id和链接
    if caprcha_id:
        img_html = session.get(caprcha_link)
    with open ('caprcha.jpg','w') as f:
        f.write(img_html.content)
    try:
        im = image.open(caprcha.jpg)
        im.show()
        im.close()
    except:
        print("打开图片出错")
    else:
        caprcha = input('请输入验证码：')      #把看到的验证码图片输入进去
    data = {                    #需要传去的数据
            'source':source,
            'redir':redir,
            'form_email':username,
            'form_password':password,
            'login':login,
            }    
    if caprcha_id:          #如果需要验证码就把下面的两个数据加入到data里面
        data['captcha-id'] = caprcha_id
        data['captcha-solution'] = caprcha
    html = html = session.post(url,data=data,headers=headers)   #获取登入后的页面
    print(session.cookies.items())   #打印此时的cookies



def get_captcha(url):       #解析登入界面，获取caprcha_id和caprcha_link
    html = requests.get(url)
    soup = BeautifulSoup(html.text,'lxml')
    caprcha_link = soup.select('#captcha_image')[0]['src']
    #lzform > div.item.item-captcha > div > div > input[type="hidden"]:nth-child(3)
    caprcha_id = soup.select('div.captcha_block > input')[1]['value']
    return caprcha_id,caprcha_link    #返回链接和id信息

login(username,password)
login_url = 'https://www.douban.com/group/'
xiaozu_html = session.get(login_url)
soup = BeautifulSoup(xiaozu_html.text,'lxml')
#content > div > div.article > div.topics > table > tbody > tr:nth-child(1) > td.td-subject > a
titles = soup.select('tr.pl > td.td-subject > a.title')
for title in titles:
    print(title['href'],title.string)

