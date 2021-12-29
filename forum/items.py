# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ForumscannerItem(scrapy.Item):
    TICKER = scrapy.Field()
    THREAD_KEY_TODAY = scrapy.Field()
    THREAD_KEY_YESTERDAY= scrapy.Field()
    REPLIES_TODAY= scrapy.Field()
    REPLIES_YESTERDAY= scrapy.Field()
    VIEWS_TODAY= scrapy.Field()
    VIEWS_YESTERDAY= scrapy.Field()
