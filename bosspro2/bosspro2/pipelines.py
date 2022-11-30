# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
import sqlite3


class Bosspro2Pipeline:
    def process_item(self, item, spider):
        # self.conn = pymysql.Connect(host="localhost", user="root", password="011223", db="job_information", charset='utf8')
        self.conn = sqlite3.connect(r'D:\job_information.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS python_liepin(job_name CHAR(100), job_salary CHAR(50), job_address CHAR(100),job_demand TEXT);')
        self.cursor.execute('insert into python_liepin (job_name,job_salary,job_address,job_demand) values("%s","%s","%s","%s")'%(item['job_name'],item['job_salary'],item['job_address'],item['job_demand']))
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

        return item

