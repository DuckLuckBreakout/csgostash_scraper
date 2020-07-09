# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Item
from pymongo import MongoClient
from csgostashparser.items import SkinParserItem


class CsgostashparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.skins

    def process_item(self, item: Item, spider):
        collection = self.mongobase[spider.name]
        items = parse_info_table(item, spider.name)
        collection.insert_many(items)
        return item


def parse_info_table(item: Item, spider_name):
    items = []

    table = item['info_table']
    print(table)
    for quality in table.keys():
        row = table[quality]
        items.append(SkinParserItem(name=item['name'],
                                    href=item['href'],
                                    quality=quality,
                                    price=row['price'],
                                    listings=row['listings'],
                                    median=row['median'],
                                    volume=row['volume'],
                                    bit_price=row['bit_price'],
                                    site_name=item['site_name']))


    item.pop('info_table')

    return items


