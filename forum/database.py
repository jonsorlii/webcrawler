from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode


"""
DEFINED DATABASE
"""
TABLES = {}

TABLES['ticker'] = ("CREATE TABLE `ticker` ("
                    "`ticker_name` varchar(8) NOT NULL,"
                    "PRIMARY KEY (`ticker_name`)"
                    ") ENGINE=InnoDB")

TABLES['thread'] = ("CREATE TABLE `thread` ("
                    "`thread_id` varchar(512) NOT NULL,"
                    "`views` int NOT NULL,"
                    "`last_updated`  datetime NOT NULL,"
                    "`replies` int NOT NULL,"
                    "`ticker_name` varchar(8) NOT NULL,"
                    "PRIMARY KEY (`thread_id`),"
                    "CONSTRAINT `thread_fk` FOREIGN KEY (`ticker_name`)"
                    "REFERENCES `ticker` (`ticker_name`) ON DELETE CASCADE"
                    ") ENGINE = InnoDB")


class Database():
    def __init__(self):
        self.tryConnection()
        self.DB_NAME = "scrapy"
        self.cnx = mysql.connector.connect(host='localhost' , user='root' , passwd='12345' , database='scrapy')
        self.cursor = self.cnx.cursor()
        self.create_database()
        self.create_tables()


    def tryConnection(self):
        try:
            cnx = mysql.connector.connect(host='localhost' , user='root' , passwd='12345' , database='scrapy')

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            cnx.close()

    def create_database(self):
        try:
            self.cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self.DB_NAME))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

        try:
            self.cursor.execute("USE {}".format(self.DB_NAME))
        except mysql.connector.Error as err:
            print("Database {} does not exists.".format(self.DB_NAME))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database(self.cursor)
                print("Database {} created successfully.".format(self.DB_NAME))
                self.cnx.database = self.DB_NAME
            else:
                print(err)
                exit(1)
    def create_tables(self):
        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print("Creating table {}: ".format(table_name) , end='')
                self.cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")

        self.cursor.close()
        self.cnx.close()


class databaseQuery():
    def __init__(self):
        self.cnx = mysql.connector.connect(user='root', password = '12345', database = 'scrapy')
        self.cursor = self.cnx.cursor()

    def insert_ticker(self):
        return ("INSERT INTO ticker "
                "(ticker_name) "
                "VALUES (%s)")

    def insert_views(self):
        return ("INSERT INTO thread "
                "(thread_id, views, last_updated, replies, ticker_name) "
                "VALUES (%s,%s,%s,%s,%s)")
    def get_views_replies(self):
        return ("SELECT thread_id, views, replies "
                "FROM thread"
                "WHERE ticker_name = ?")
    def get_ticker(self):
        return ("SELECT *"
                "FROM ticker")

