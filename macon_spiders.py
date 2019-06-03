import scrapy
from pathlib import Path
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from scrapy.exceptions import CloseSpider

class AugmentedSpider(scrapy.Spider):

    @staticmethod
    def clean_url(url):
        url = url.replace('https', '').replace('http', '')
        url = url.replace('://', '')
        for char in ['<', '>', ':', '"', '\\', '|', '?']:  #, '/'
            url = url.replace(char, '_')
        if url[-1] == '/':
            url = url[:-1]
        return url

    @staticmethod
    def create_directory(url, stem_path):
        arr = [x for x in url.split('/') if len(x.strip()) > 0]
        file = arr[-1]
        if str(file).count('.html') == 0:
            file = file + '.html'
        arr = arr[:-1]
        for i, item in enumerate(arr):
            if not (stem_path / Path(*arr[:i+1])).is_dir(): # can probably tighten up some of this too
                if (stem_path / Path(*arr[:i+1])).exists():
                    continue
                else:
                    (stem_path / Path(*arr[:i+1])).mkdir()
        return stem_path / Path(*arr) / file

    @staticmethod
    def prep_write(response):
        stem = AugmentedSpider.clean_url(str(response.url))
        html_path = AugmentedSpider.create_directory(stem, Path.cwd())
        if html_path.exists(): # not sure if this is necessary anymore
            return None
        else:
            return html_path

    def parse(self, response):
        raise NotImplementedError


class BoundedDomainSpider(AugmentedSpider):

    def parse(self, response):
        for link in LinkExtractor().extract_links(response):
            request = Request(url=link.url)
            request.meta.update(link_text=link.text)
            yield request

        for item in self.parse_item(response):
            yield item

    @staticmethod
    def parse_item(response):
        outpath = AugmentedSpider.prep_write(response)
        if outpath is not None: # test if this will actually happen anymore
            with open(outpath, 'w', encoding = 'utf-8') as html_file: #TODO maybe a better way?
                # todo overwrite any existing file
                html_file.write(response.text)
        yield {
            'url': response.url
        }


class SinglePageSpider(AugmentedSpider):

    def parse(self, response, stem_path=Path.cwd()):
        outfile = AugmentedSpider.clean_url(str(response.url)) + '.html'
        outpath = str(stem_path / outfile)
        with open(outpath, 'w') as html_file:
            html_file.write(response.text)
        yield {
            'url': response.url
        }
        raise CloseSpider('Page {} scraped.'.format(str(response.url)))
