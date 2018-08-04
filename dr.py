import requests
from bs4 import BeautifulSoup
from PIL import Image

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Referer':'https://accounts.douban.com/login?alias=&redir=https%3A%2F%2Fwww.douban.com%2F&source=index_nav&error=1001'

}

session = requests.Session()
session.headers.update(headers)

username = input('请输入你的用户名：')
password = input('请输入你的密码：')

url = 'https://accounts.douban.com/login'

def login(username,password,source='index_nav',redir='https://www.douban.com/',login='登录'):     #模拟登入函数
    caprcha_id,caprcha_link = get_captcha(url)          #把get_captcha函数返回的值
    if caprcha_id:          #如果有caprcha_id,就执行解析caprcha_link网页信息，并把图片保存下来打开
        img_html = session.get(caprcha_link)
        with open('caprcha.jpg','wb') as f:
            f.write(img_html.content)
        try:
            im = Image.open('caprcha.jpg')
            im.show()
            im.close()
        except:
            print('打开错误')
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
    html = session.post(url,data=data,headers=headers)
    print(session.cookies.items())


def get_captcha(url):       #解析登入界面，获取caprcha_id和caprcha_link
    html = requests.get(url)
    soup = BeautifulSoup(html.text,'lxml')
    caprcha_link = soup.select('#captcha_image')[0]['src']
    #lzform > div.item.item-captcha > div > div > input[type="hidden"]:nth-child(3)
    caprcha_id = soup.select('div.captcha_block > input')[1]['value']
    return caprcha_id,caprcha_link

login(username,password)
login_url = 'https://www.douban.com/group/'
xiaozu_html = session.get(login_url)
soup = BeautifulSoup(xiaozu_html.text,'lxml')
#content > div > div.article > div.topics > table > tbody > tr:nth-child(1) > td.td-subject > a
titles = soup.select('tr.pl > td.td-subject > a.title')
for title in titles:
    print(title['href'],title.string)