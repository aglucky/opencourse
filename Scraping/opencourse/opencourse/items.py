# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OCWItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    number = scrapy.Field()
    level = scrapy.Field()
    link = scrapy.Field()
    features = scrapy.Field()
    description = scrapy.Field()
    taught_in = scrapy.Field()
    pass

class OYCItem(scrapy.Item):
    name = scrapy.Field()
    number = scrapy.Field()
    link = scrapy.Field()
    date = scrapy.Field()
    professor = scrapy.Field()
    description = scrapy.Field()
    pass

class ccItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    date = scrapy.Field()
    features = scrapy.Field()
    description = scrapy.Field()
    pass


class UIUCItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    number = scrapy.Field()
    website = scrapy.Field()
    prereq = scrapy.Field()
    description = scrapy.Field()
    directors = scrapy.Field()
    last_updated = scrapy.Field()
    pass

class berkItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    number = scrapy.Field()
    type = scrapy.Field()
    text_profs = scrapy.Field()
    profs = scrapy.Field()
    websites = scrapy.Field()
    description = scrapy.Field()
    prerequisites = scrapy.Field()
    units = scrapy.Field()
    pass

class CMUItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    number = scrapy.Field()
    meta = scrapy.Field()
    last_offered = scrapy.Field()
    level = scrapy.Field()
    key_topics = scrapy.Field()
    background = scrapy.Field()
    prereq = scrapy.Field()
    units = scrapy.Field()
    level = scrapy.Field()
    permission = scrapy.Field()
    website = scrapy.Field()
    pass

class stanfordItem(scrapy.Item):
    name = scrapy.Field()
    number = scrapy.Field()
    link = scrapy.Field()
    prof = scrapy.Field()
    pass

class SAILItem(scrapy.Item):
    name = scrapy.Field()
    number = scrapy.Field()
    link = scrapy.Field()
    profs = scrapy.Field()
    pass

class cornellItem(scrapy.Item):
    name = scrapy.Field()
    sites = scrapy.Field()
    pass
