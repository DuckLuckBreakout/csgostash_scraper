# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SkinParserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    info_table = scrapy.Field()
    quality = scrapy.Field()
    price = scrapy.Field()
    listings = scrapy.Field()
    median = scrapy.Field()
    volume = scrapy.Field()
    bit_price = scrapy.Field()
    href = scrapy.Field()
    site_name = scrapy.Field()



# class superjobItem(scrapy.Item):
