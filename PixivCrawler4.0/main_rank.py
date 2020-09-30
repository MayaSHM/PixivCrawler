from PixivCrawler4 import PixivCrawler


def main():
    """
        get_rank()方法需要传递mode_str和date_str两个参数,默认为'daily'和昨日
        mode_str = 'daily':每日 | 'weekly':每周 | 'male':受男性欢迎 | 'female':受女性欢迎  | 'rookie'新人 | 'original'原创
                   'daily_r18' | 'weekly_r18' | 'male_r18' | 'female_r18'
        date_str = 'yyyymmdd'
        已知在中午11点左右会出现昨日排行无法爬取的问题，可能是pixiv在这个时间才进行统计

        get_illustrator_imgs()需要传递uid_str参数
    """
    crawler = PixivCrawler()
    # crawler.get_rank(mode_str='daily', date_str='20200925')
    crawler.get_illustrator_imgs(uid_str='7638711')
    pass


if __name__ == '__main__':
    main()
