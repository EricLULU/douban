
import random
import time

def headers_return():
    list_hea = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch, br',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Cookie':'dbcl2="182339024:5WbcAMjeT7Y"; bid=uMtVus5yIiY; ck=fj1e; ps=y; __utmt=1; ap=1; __utmt_douban=1; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1533444397%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=4dea5b3f-eb2b-4110-a3fc-5ee3e015a5db; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_4dea5b3f-eb2b-4110-a3fc-5ee3e015a5db=true; gr_cs1_4dea5b3f-eb2b-4110-a3fc-5ee3e015a5db=user_id%3A1; gr_user_id=4f4654a4-f867-4c55-b080-9240957129d3; __utma=30149280.2145365967.1533444390.1533444390.1533444390.1; __utmb=30149280.4.10.1533444390; __utmc=30149280; __utmz=30149280.1533444390.1.1.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/register_success; __utmv=30149280.18233; __utma=81379588.1985137161.1533444396.1533444396.1533444396.1; __utmb=81379588.2.10.1533444396; __utmc=81379588; __utmz=81379588.1533444396.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_id.100001.3ac3=f0f0870f4b144b0d.1533444397.1.1533444404.1533444397.; _pk_ses.100001.3ac3=*; _vwo_uuid_v2=DFF939E4A982B8551793A8357DD36E500|534ac3a0d9d38f12e63bb4068a9090c6; push_noty_num=0; push_doumail_num=0',
    'Host':'book.douban.com',
    'Referer':'https://book.douban.com/',
    'Upgrade-Insecure-Requests':1,
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    }
    
    return list_hea     #超过600秒则随机返回一个代理user_agent
