import requests
import re
import datetime
import os
import sys

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
    rank_json = requests.get(rank_url, params=params, headers=headers).json()

    # 爬取图片
    create_dir(dir_=f'./pixiv/{getYesterday()}')
    for contents in rank_json['contents']:
        # https://i.pximg.net/c/240x480/img-master/img/2020/09/10/00/45/04/84269486_p0_master1200.jpg
        date = re.search('/\d{4}(/\d{2}){5}/', contents['url']).group()
        headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
            '537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'Referer':
            'https://www.pixiv.net/member_illust.php?mode=medium&illust_id='+str(contents['illust_id'])
        }
        illust_pages = int(contents['illust_page_count'])
        if illust_pages > 1:
            create_dir(dir_=f"./pixiv/{getYesterday()}/{contents['illust_id']}")
            for pages in range(illust_pages):
                url_jpg = 'https://i.pximg.net/img-original/img'+date+str(contents['illust_id'])+'_p'+str(pages)+'.jpg'
                b_img = requests.get(url=url_jpg, headers=headers).content
                if sys.getsizeof(b_img) > 200:
                    img_name = f"pixiv/{getYesterday()}/{contents['illust_id']}/{contents['illust_id']}_p{pages}.jpg"
                    with open(img_name, 'wb') as fp:
                        fp.write(b_img)
                else:
                    url_png = 'https://i.pximg.net/img-original/img' + date + str(contents['illust_id']) + '_p' + \
                              str(pages) + '.png'
                    b_img = requests.get(url=url_png, headers=headers).content
                    img_name = f"pixiv/{getYesterday()}/{contents['illust_id']}/{contents['illust_id']}_p{pages}.png"
                    with open(img_name, 'wb') as fp:
                        fp.write(b_img)

        else:
            illust_pages -= 1  # 从0开始
            url_jpg = 'https://i.pximg.net/img-original/img' + date + str(contents['illust_id']) + '_p' + \
                      str(illust_pages) + '.jpg'
            b_img = requests.get(url=url_jpg, headers=headers).content
            if sys.getsizeof(b_img) > 200:
                img_name = f"pixiv/{getYesterday()}/{contents['illust_id']}_p{illust_pages}.jpg"
                with open(img_name, 'wb') as fp:
                    fp.write(b_img)
            else:
                url_png = 'https://i.pximg.net/img-original/img' + date + str(contents['illust_id']) + '_p' + \
                          str(illust_pages) + '.png'
                b_img = requests.get(url=url_png, headers=headers).content
                img_name = f"pixiv/{getYesterday()}/{contents['illust_id']}_p{illust_pages}.png"
                with open(img_name, 'wb') as fp:
                    fp.write(b_img)

        print('id=%d Done.' % contents['illust_id'])
    print('All Done.')
    pass


if __name__ == '__main__':
    main()
