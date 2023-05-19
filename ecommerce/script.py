from scrapy.crawler import CrawlerProcess

from ecommerce.ecommerce.spiders.product_spider import ProductSpiderSpider
from ecommerce.spiders.keelerhardware import KeelerhardwareSpider


def script():
    process_ = CrawlerProcess()
    process_.crawl(ProductSpiderSpider)
    process_.crawl(KeelerhardwareSpider)
    process_.start()


if __name__ == "__main__":
    script()
