# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PymangaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ComicItem(scrapy.Item):
    root_path = scrapy.Field()
    comic_title = scrapy.Field()
    comic_path = scrapy.Field()
    url = scrapy.Field()


class VolumeItem(scrapy.Item):
    comic_path = scrapy.Field()
    comic_title = scrapy.Field()
    volume_title = scrapy.Field()
    volume_path = scrapy.Field()


class PictureItem(scrapy.Item):
    volume_path = scrapy.Field()
    comic_title = scrapy.Field()
    volume_title = scrapy.Field()
    index = scrapy.Field() # start from 1
    referer = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
	
