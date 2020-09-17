import requests
import datetime
import os

def getYesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    return yesterday

def create_dir():
    img_dir = f'./pixiv/{getYesterday()}'
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)

def main():
    headers = {
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    }  # UA伪装

    # 获取排行数据
    rank_url = 'https://api.pixivic.com/ranks'
    params = {
        'page': '1',
        'date': getYesterday(),  # YYYY-MM-DD的当日信息
        'mode': 'day',
        'pageSize': '30',
    }
    rank_json = requests.get(url=rank_url, params=params, headers=headers).json()
    create_dir()
    # 批量下载
    print('Getting pictures...')
    for img_info in rank_json['data']:
        headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'Referer':
            'https://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + str(img_info['id']),
        }  # 批量UA伪装，Referer是绕开403错误的关键
        for urls in img_info['imageUrls']:  # 处理一份图片不止一张的情况
            b_img = requests.get(url=urls['original'], headers=headers).content
            # content返回二进制形式的图片数据
            img_name = f"pixiv/{getYesterday()}/{img_info['id']}_p{img_info['imageUrls'].index(urls)}.png"
            with open(img_name, 'wb') as fp:
                fp.write(b_img)
    print('Done.')
    pass

if __name__ == '__main__':
    main()
