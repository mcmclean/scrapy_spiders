from bs4 import BeautifulSoup
import requests
import selenium

'''
https://doc.scrapy.org/en/latest/topics/practices.html
https://www.datacamp.com/community/tutorials/making-web-crawlers-scrapy-python#shell
https://blog.scrapinghub.com/2015/04/22/frontera-the-brain-behind-the-crawls
https://docs.scrapy.org/en/latest/topics/link-extractors.html

https://docs.scrapy.org/en/latest/topics/broad-crawls.html
'''

from scrapy.crawler import CrawlerProcess

from macon_spiders import BoundedDomainSpider, SinglePageSpider


if __name__ == '__main__':

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'AUTOTHROTTLE_ENABLED': True,
        'HTTPCACHE_ENABLED': True,
        'DOWNLOAD_DELAY': 5.0,
        'RANDOMIZE_DOWNLOAD_DELAY': True
    })

    '''
    process.crawl expects a Spider class, not a Spider instance
    '''

    # process.crawl(
    #     BoundedDomainSpider,
    #     name = 'Slashfilm Spider',
    #     allowed_domains = ['slashfilm.com'],
    #     start_urls = ['https://www.slashfilm.com/category/movie-marketing/movie-trailers/']
    # )
    #
    # process.crawl(
    #     BoundedDomainSpider,
    #     name = 'Scrapy Docs Spider',
    #     allowed_domains = ['scrapy.org'],
    #     start_urls = ['https://docs.scrapy.org/']
    # )

    # process.crawl(
    #     BoundedDomainSpider,
    #     name='Scrapy Docs Resources Spider',
    #     allowed_domains=['scrapy.org'],
    #     start_urls=['https://scrapy.org/resources/']
    # )

    process.crawl(
        SinglePageSpider,
        name = 'Single Page Spider',
        allowed_domains=['slashfilm.com'],
        start_urls = ['http://www.slashfilm.com']
    )

    process.start()
