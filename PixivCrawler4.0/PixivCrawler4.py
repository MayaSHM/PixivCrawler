import requests
from lxml import etree
import re
import datetime
import os
import json


def get_yesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    return yesterday


class PixivRankCrawler():

    def __init__(self, mode='daily', date=re.sub("\D", "", str(get_yesterday()))):
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'Cookie':
            '__cfduid=d09f46e67f9f686349c8cd6cef06aef941599711884; first_visit_datetime_pc=2020-09-10+13%3A24%3A44; p_ab_id=4; p_ab_id_2=1; p_ab_d_id=1152997170; yuid_b=IlOSSXA; _fbp=fb.1.1599711887081.772867575; _ga=GA1.2.1341241396.1599711887; device_token=1074272169a6d1429a2585bd2a380e29; c_type=26; a_type=0; b_type=0; ki_r=; limited_ads=%7B%22responsive%22%3A%22%22%7D; adr_id=AV4ySzkc0eaaVMK0XJMqRc8k1YOmTtwVaaM3j6nCrsyB88rg; login_ever=yes; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^6=user_id=46341707=1^9=p_ab_id=4=1^10=p_ab_id_2=1=1^11=lang=zh=1; ki_t=1599711893954%3B1599976050070%3B1599978526647%3B3%3B9; __utmc=235335808; __utmz=235335808.1600322352.11.2.utmcsr=baidu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; p_b_type=2; categorized_tags=BeQwquYOKY~CADCYLsad0~EGefOqA6KB~IVwLyT8B6k~IfpAckJr8v~Ig5OcZugU6~RcahSSzeRf~RsIQe1tAR0~ayMvqitdaj~bXMh6mBhl8~iFcW6hPGPU~kxSeeOQL7R~m3EJRa33xU~pvU1D1orJa~s1DgbDGhu4~yPNaP3JSNF; _gid=GA1.2.477152317.1600322378; tag_view_ranking=Lt-oEicbBr~RTJMXD26Ak~jhuUT0OJva~lE8un-csVV~b1s-xqez0Y~azESOjmQSV~q303ip6Ui5~kxSeeOQL7R~osjGBvsNDJ~NT6HjMvlFJ~ZnmOm5LdC3~gpglyfLkWs~RKXr2H_ooU~2_IEt5mZob~J5qR5z9qZS~jk9IzfjZ6n~tgP8r-gOe_~xfYGFeocXg~s1DgbDGhu4~_fMf86iA_3~-StjcwdYwv~D0nMcn6oGk~RjyWcTb8JF~faHcYIP1U0~Ie2c51_4Sp~iFcW6hPGPU~RcahSSzeRf~0xsDLqCEW6~EGefOqA6KB~qvqXJkzT2e~HY55MqmzzQ~ETjPkL0e6r~yPNaP3JSNF~jH0uD88V6F~FGFzwIh-Ko~88R-whWgJ8~uusOs0ipBx~V_mXd5MUQh~2EpPrOnc5S~M_kcfifITK~_pwIgrV8TB~j3leh4reoN~_wgwZ79S9p~6HUSQEiWHT~6293srEnwa~sKWC9SVJ11~VMq-Vxsw8k~xYaPXYOqJJ~ABWTvyMCOF~zIv0cf5VVk~m3EJRa33xU~Ft9gUTvPbo~ZbQH8rzj7J~vFXX3OXCCb~nQRrj5c6w_~1Cu1TkXAKa~7ZfrUr9hCu~n7FOl20z1q~47mPW0XOXt~1F9SMtTyiX~zyKU3Q5L4C~eVxus64GZU~Nzi0U7n6AT~IEwLqSu8H-~ndg7A-BkFA~G8rSXZQWFW~cMiCsyf0bk~mzJgaDwBF5~IZhlWAh6lN~LJo91uBPz4~aFY1z2Bqk2~nhidBJEVl0~t6fkfIQnjP~nGMp8b3NYZ~vu8X1pzWO_~4SyVAI2yYS~EUwzYuPRbU~ZXRBqRlFWu~7qtAnPrz1r~p27QC63XHD~Bx3XxRyJlI~Ltq1hgLZe3~28gdfFXlY7~MhieHQxNXo~RDhRZJGFE1~4rDNkkAuj_~wKl4cqK7Gl~5oPIfUbtd6~wZbOwflF--~6gzQ1vZckJ~wUqOmKcFBf~J7eAA4z4Hd~hzLsBUtKYm~JO16HzBgpd~BaQprNPH_K~CwLGRJQEGQ~9OgM5t9f0L~znkteK6abh~U8X05tkQOK~2QTW_H5tVX; __utma=235335808.1341241396.1599711887.1600322352.1600327997.12; PHPSESSID=46341707_BVo920waYdWSsdxERnwo1E2DEAA5XLgU; privacy_policy_agreement=2; __utmt=1; __utmb=235335808.7.10.1600327997'
        }
        self.rank_url = 'https://www.pixiv.net/ranking.php'
        self.params = {
            'p': '1',
            'format': 'json',
            'mode': mode,
            'date': date,
        }
        self.id_list = []

    def create_dir(self, dir_path):
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

    def _get_headers_with_referer(self, id_):
        headers_with_referer = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                '537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'Referer':
                'https://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + str(id_)
        }
        return headers_with_referer

    def _get_info_dict(self, id_):
        url = 'https://www.pixiv.net/artworks/' + str(id_)
        resp = requests.get(url=url, headers=self.headers)
        if resp.status_code == 200:
            img_page = resp.text
            parser = etree.HTMLParser(encoding="utf-8")  # 默认是XML解析器，碰到不规范的html文件时就会解析错误，增加解析器
            tree = etree.HTML(img_page, parser=parser)  # 实例化一个etree对象
            info = tree.xpath('//meta[@name="preload-data"]/@content')[0]
        return json.loads(info)  # json.loads()用于转化字符串为字典

    def _get_org_url(self, info_dict, id_):
        return info_dict['illust'][str(id_)]['urls']['original']

    def _get_file_ex(self, org_url):
        return re.findall('\.[jpgn]{3}', org_url)[0]

    def _get_page_count(self, info_dict, id_):
        return info_dict['illust'][str(id_)]['pageCount']

    def _save_img(self, id_, page_count, file_ex, b_img):
        filepath = f'./pixiv/{get_yesterday()}/{id_}_p{page_count-1}{file_ex}'
        with open(filepath, 'wb') as fp:
            fp.write(b_img)

    def _save_imgs(self, id_, page, file_ex, b_img):
        filepath = f'./pixiv/{get_yesterday()}/{id_}/{id_}_p{page}{file_ex}'
        with open(filepath, 'wb') as fp:
            fp.write(b_img)

    def run(self):
        rank_json = requests.get(self.rank_url, params=self.params, headers=self.headers).json()
        for contents in rank_json['contents']:
            self.id_list.append(contents['illust_id'])
        self.create_dir(dir_path=f'./pixiv')
        self.create_dir(dir_path=f'./pixiv/{get_yesterday()}')
        for id_ in self.id_list:
            headers_rf = self._get_headers_with_referer(id_)
            info_dict = self._get_info_dict(id_)
            org_url = self._get_org_url(info_dict, id_)
            file_ex = self._get_file_ex(org_url)
            page_count = self._get_page_count(info_dict, id_)
            if page_count > 1:
                self.create_dir(dir_path=f'./pixiv/{get_yesterday()}/{id_}')
                for page in range(page_count):
                    multi_url = re.sub('p0', f'p{page}', org_url)  # 处理多页漫画的情况
                    b_img = requests.get(url=multi_url, headers=headers_rf).content
                    self._save_imgs(id_, page, file_ex, b_img)
            else:
                b_img = requests.get(url=org_url, headers=headers_rf).content
                self._save_img(id_, page_count, file_ex, b_img)
            print('id=%d Done.' % id_)
        print('All Done.')

