from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from csgostashparser import settings
from csgostashparser.spiders.csgostash_skins import CsgoStashSkinSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(CsgoStashSkinSpider)
    process.start()
