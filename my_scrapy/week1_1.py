import requests
import lxml.etree    # 导入 xpath 包
from bs4 import BeautifulSoup as bs
from time import sleep
import random
import pandas as pd
# 安装并使用 requests、bs4 库，爬取猫眼电影的前 10 个电影名称、电影类型和上映时间，并以 UTF-8 字符集保存到 csv 格式的文件中。

main_domain = "https://maoyan.com"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/75.0.3770.100'
header = {'user-agent': user_agent}
myurl = 'https://maoyan.com/films?showType=3&offset=0'
response = requests.get(myurl, headers=header)
bs_info = bs(response.text, 'html.parser')
movie_list = []


def get_details(url, name):
    details_header = {'user-agent': user_agent}
    details_response = requests.get(url, headers=header)
    details_info = bs(details_response.text, 'html.parser')
    i = 0
    j = 0

    for tags in details_info.find_all('li', attrs={'class': 'ellipsis'}):
        if i == 0:   # 控制第一次发现<li class='ellipsis'>
            for atag in tags.find_all('a'):
                if j == 0:
                    print(name)
                    movie_list.append(name)
                    j = j + 1   # 防止反复获取电影名。
                print(atag.text)
                movie_list.append(atag.text)
                sleep(random.randint(3, 10))  # 防止被反扒
        if i == 2:   # 控制第三次发现<li class='ellipsis'>
            print(tags.text)
            movie_list.append(tags.text)
            sleep(random.randint(3, 10))  # 防止被反扒
        i = i + 1






ii = 0
for tags in bs_info.find_all('div', attrs={'class': 'channel-detail movie-item-title'}):
    if ii < 10:
        for atag in tags.find_all('a'):
            get_details(main_domain + atag.get('href'), atag.text)   # 调用获取详细信息函数
            sleep(random.randint(3, 10))    # 防止被反扒
        ii = ii + 1

movie1 = pd.DataFrame(data=movie_list)
movie1.to_csv('./movie1.csv', encoding='utf8', index=False, header=False)



