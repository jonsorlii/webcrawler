# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
from . import database
from .spiders.edit_data import EditData
import datetime as dt

class ForumPipeline(object):
    """
    Import items and insert into database
    """
    def __init__(self):
        self.create_queries = database.databaseQuery()
        self.manipulate = EditData()

    def process_item(self, item, spider):
        """
        manipulating data first
        """
        items = self.manipulate.fix_data(item)
        """
        Insert into db
        """
        ticker = item['TICKER']
        str_now = dt.datetime.now()
        print(items)
        """
        WORKS
        for key, item in items.items():
            item_1 = item[0]
            item_2 = item[1]
            print(key)
            self.create_queries.cursor.execute(self.create_queries.insert_views(), (str(key), int(item_1), str_now, int(item_2), ticker))
        self.create_queries.cnx.commit()
        """

        """
        Need to check if thread exists, if it exists, check dates and update 
        """
        return item


