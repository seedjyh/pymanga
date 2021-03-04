import scrapy
import os
import re
import urllib.parse
from scrapy import Request
from scrapy.loader import ItemLoader
from pymanga import settings
from pymanga.utils.js.decrypter import Decrypter
from pymanga.items import ComicItem, VolumeItem, PictureItem, NewsItem

class Gugu5Spider(scrapy.Spider):
    name = 'gugu5'
    allowed_domains = ['gugu5.com', 'dmzj.com']
    __all_urls = []

    def __init__(self, url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__all_urls.append(url)

    def start_requests(self):
        for url in self.__all_urls:
            url_parsed = urllib.parse.urlparse(url)
            if url_parsed.netloc == 'www.gugu5.com':
                if os.path.splitext(url_parsed.path)[1]:
                    yield Request(url=url, callback=self.parse_volume_page)
                else:
                    yield Request(url=url, callback=self.parse_comic_page)

    def parse(self, response):
        """ This method is here only for fixing warning: must implement all abstract methods"""
        return self.parse_comic_page(response)

    def parse_comic_page(self, response):
        """parse a comic page"""
        root_path = settings.DOWNLOAD_STORE
        comic_title = response.xpath('//h1/text()').extract_first()
        comic_title = comic_title.replace(":", "_").replace("!", "_")
        comic_path = os.path.join(root_path, comic_title)
        # scrape comic item
        l = ItemLoader(item=ComicItem(), response=response)
        l.add_value('root_path', root_path)
        l.add_value('comic_title', comic_title)
        l.add_value('comic_path', comic_path)
        l.add_value('url', response.url)
        yield l.load_item()  # ?
        # scrape volume url
        url_parsed = urllib.parse.urlparse(response.url)
        for volume_url in response.xpath("//div[@class='cy_zhangjie']//li/a/@href").extract():
            real_volume_url = volume_url
            yield Request(url=real_volume_url, callback=self.parse_volume_page, meta={'comic_path': comic_path, 'comic_title': comic_title,})


    def parse_volume_page(self, response):
        """parse a volume page"""
        root_path = settings.DOWNLOAD_STORE
        comic_title = response.meta.get("comic_title", response.xpath('//script/text()').re_first('g_comic_name = "(.+)"'))
        comic_path = response.meta.get("comic_path", os.path.join(root_path, comic_title))
        volume_title = response.xpath('//script/text()').re_first('g_chapter_name = "(.*)"')
        volume_path = os.path.join(comic_path, volume_title)
        # scrape volume item
        l = ItemLoader(item=VolumeItem(), response=response)
        l.add_value('comic_path', comic_path)
        l.add_value('comic_title', comic_title)
        l.add_value('volume_title', volume_title)
        l.add_value('volume_path', volume_path)
        yield l.load_item()
        # scrape last volume
        prev_volume_url = urllib.parse.urljoin(response.url, response.xpath("//a[@id='prev_chapter']/@href").extract_first())
        yield Request(url=prev_volume_url, callback=self.parse_volume_page)
        # scrape next volume
        next_volume_url = urllib.parse.urljoin(response.url, response.xpath("//a[@id='next_chapter']/@href").extract_first())
        yield Request(url=next_volume_url, callback=self.parse_volume_page)
        # scrape picture url for current volume
        # pic_count = int(response.xpath("//script/text()").re("g_max_pic_count = (\d+)")[0]) # use less
        # picture page is same as volume page, except '#'. So process image url directly.
        eval_script = response.xpath("//script").re_first("eval\(function.*") # p,a,c,k,e,d
        pic_url_code_raw = Decrypter.decrypt_by_execjs(eval_script)
        print("=======================================", pic_url_code_raw)
        pic_url_list = re.search("\[(.*)\]", pic_url_code_raw).group(1).split(",")
        for i in range(len(pic_url_list)):
            url = urllib.parse.urljoin("https://images.dmzj.com", re.search("\"(.*)\"", pic_url_list[i]).group(1))
            url = url.replace("\\", "")
            l = ItemLoader(item=PictureItem(), response=response)
            l.add_value("volume_path", volume_path)
            l.add_value("comic_title", comic_title)
            l.add_value("volume_title", volume_title)
            l.add_value("index", i + 1)
            l.add_value("referer", response.url)
            l.add_value("file_urls", url)
            yield l.load_item()

