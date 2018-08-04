"""
各个模块说明：
"""
1. downloader 模块
用来下载各个链接对应的 html 页面
并将爬取到的 html 结果返回，然后由 cache 存入Mongo中
2. html_parser 模块
从Mongo 中取html 来进行分析
然后从html中提取信息，再将提取到的信息存储到 mongo 中

3. mongocahe模块
存储html 信息
存储提取到的信息

4. test 模块
以 豆瓣读书 为例， 开始进行爬取
使用代理池


代理：
127.0.0.1:8888