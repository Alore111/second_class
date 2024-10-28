from celery import shared_task
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from my_scrapy_project.spiders.my_spider import MySpider


@shared_task(bind=True)
def scrape_task(self, url, keywords):
    # 使用Scrapy的CrawlerProcess来运行爬虫
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    # 传递参数给爬虫，这里假设你的爬虫接受url和keywords作为参数
    process.crawl(MySpider, start_urls=[url], keywords=keywords)
    process.start()  # 启动爬虫

    # Celery任务完成后可以返回一个结果或者状态信息
    return {'status': 'Scraping task completed'}