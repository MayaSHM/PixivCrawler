import requests
from lxml import etree
import re
import datetime
import os
import json


def getYesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    return yesterday


def create_dir(dir_):
    if not os.path.exists(dir_):
        os.mkdir(dir_)


def main():
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
            '537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    }  # UA伪装
    # 获取排名信息
    rank_url = 'https://www.pixiv.net/ranking.php'
    params = {
        'p': '1',
        'format': 'json',
        'mode': "daily",
        'date': re.sub("\D", "", str(getYesterday())),
    }
    rank_resp = requests.get(rank_url, params=params, headers=headers)
    rank_json = rank_resp.json()

    # 爬取图片
    create_dir(dir_=f'./pixiv/{getYesterday()}')
    id_list = []
    for contents in rank_json['contents']:
        id_list.append(contents['illust_id'])

    for id_ in id_list:
        headers_rf = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                '537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'Referer':
                'https://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + str(id_)
        }
        url = 'https://www.pixiv.net/artworks/' + str(id_)
        resp = requests.get(url=url, headers=headers)
        if resp.status_code == 200:
            img_page = resp.text
            parser = etree.HTMLParser(encoding="utf-8")  # 默认是XML解析器，碰到不规范的html文件时就会解析错误，增加解析器
            tree = etree.HTML(img_page, parser=parser)  # 实例化一个etree对象
            info = tree.xpath('//meta[@name="preload-data"]/@content')[0]
            info_dict = json.loads(info)  # json.loads()用于转化字符串为字典
            org_url = info_dict['illust'][str(id_)]['urls']['original']
            file_ex = re.findall('\.[jpgn]{3}', org_url)[0]
            page_count = info_dict['illust'][str(id_)]['pageCount']
            if page_count > 1:
                create_dir(dir_=f'./pixiv/{getYesterday()}/{id_}')
                for page in range(page_count):
                    multi_url = re.sub('p0', f'p{page}', org_url)  # 处理多页漫画的情况
                    b_img = requests.get(url=multi_url, headers=headers_rf).content
                    filepath = f'./pixiv/{getYesterday()}/{id_}/{id_}_p{page}{file_ex}'
                    with open(filepath, 'wb') as fp:
                        fp.write(b_img)
            else:
                b_img = requests.get(url=org_url, headers=headers_rf).content
                filepath = f'./pixiv/{getYesterday()}/{id_}_p{page_count-1}{file_ex}'
                with open(filepath, 'wb') as fp:
                    fp.write(b_img)
            print('id=%d Done.' % id_)
    print('All Done.')
    pass


if __name__ == '__main__':
    main()
