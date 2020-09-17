from PixivCrawler4 import PixivRankCrawler


def main():
    """
        PixivRankCrawler所需参数：
        
        mode: 默认daily
        'daily': 每日 'weekly': 每周 'monthly'：本月
        'male': 受男性欢迎 'female': 受女性欢迎  'rookie'：新人  'original'：原创

        date：默认前一天。格式：'yyyymmdd'
    """
    crawl = PixivRankCrawler(mode='daily')
    crawl.run()
    pass


if __name__ == '__main__':
    main()
