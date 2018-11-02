# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import shutil
import time
from scrapy.exceptions import DropItem
from pymanga import settings
from pymanga.items import ComicItem, VolumeItem, PictureItem
from scrapy.pipelines.files import FilesPipeline


class WriteFilePipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, ComicItem):
            return self.process_comic_item(item, spider)
        elif isinstance(item, VolumeItem):
            return self.process_volume_item(item, spider)
        elif isinstance(item, PictureItem):
            return self.process_picture_item(item, spider)
        else:
            raise DropItem("Unhandled item: %s" % item)

    def process_comic_item(self, item, spider):
        """Create a directory for this comic book if it doesn't exist yet."""
        comic_path = item['comic_path'][0]
        if not comic_path:
            raise DropItem("Missing comic_path in %s" % item)
        if not os.path.exists(comic_path):
            os.makedirs(comic_path)
        self.write_url_file(item["url"][0], comic_path)
        return item

    def process_volume_item(self, item, spider):
        """Create a directory for this volume if it doesn't exist yet."""
        volume_path = item['volume_path'][0]
        if not volume_path:
            raise DropItem("Missing volume_path in %s" % item)
        if os.path.exists(volume_path):
            raise DropItem("Exists comic directory path %s in %s" % (volume_path, item))
        os.makedirs(volume_path)
        return item

    def process_picture_item(self, item, spider):
        """Rename and move file downloaded."""
        old_path = os.path.join(settings.FILES_STORE, item["files"][0]["path"])
        _, extension = os.path.splitext(item["files"][0]["path"])
        new_file_name = "_".join([item["comic_title"][0], item["volume_title"][0], str(item["index"][0]).zfill(6) + extension, ])
        new_path = os.path.join(item["volume_path"][0], new_file_name)
        shutil.move(old_path, new_path)

    def write_url_file(self, url, root_path):
        file_path = os.path.join(root_path, "url.txt")
        with open(file_path, "a") as f:
            f.write("%s|%s\n" % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), url))


class MyFilesPipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        request_list = super().get_media_requests(item, info)
        for request in request_list:
            request.headers.appendlist("Referer", item["referer"])
            yield request
