# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests
import os
import pymysql
import pymysql.cursors
from rentest1.items import Rentest1Item
from datetime import datetime
import re

class FilePipeline(object):
    def header(self,url):
        host = url.split('//')[1].split('/')[0]
        '''if '.img.xiaonei.com' in url:
            host = url[7:12]+'.img.xiaonei.com'
            print(host)
        elif 'img.xiaonei.com' in url:
            host = 'img.xiaonei.com'
        elif 'photos.album.5q.com' in url:
            host = 'photos.album.5q.com'
        elif 'pic.xiaonei.com' in url:

        else:
            host = 'fmn.rrimg.com'''


        headers = {
            'Host': host,
            'Pragma': 'no-cache',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/59.0.3071.115 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8'
        }

        return headers

    def process_item(self, item, spider):
        date = datetime.now()
        date_name = date.strftime('%b %d')

        if not os.path.exists('/users/junjieluo/photos/'+date_name):
            os.mkdir('/users/junjieluo/photos/'+date_name)
        user_name=item['user_id']
        if not os.path.exists('/users/junjieluo/photos/'+date_name+'/'+str(user_name)):
            os.mkdir('/users/junjieluo/photos/'+date_name+'/'+str(user_name))

        file_name = item['url'].replace('/','_')
        with open('/users/junjieluo/photos/{}/{}/{}'.format(date_name,user_name,file_name),'wb+') as f:
            f.write(requests.get(item['url'],headers=self.header(item['url'])).content)
        return item


class MySQLPipeline(object):
    

    def __init__(self,settings):
        self.settings = settings

    def process_item(self,item,spider):
        url=item['url']
        user_id = item['user_id']
        album_id = item['album_id']
        name = item['name']
        #print(url)''
        ItemInsert = 'insert into renphoto(url,user_id,album_id,name) values("%s","%s","%s","%s")' % (url,user_id,album_id,name)
       # UserInsert = 'insert into seen(user_id) values("%s")' % user_id
        print(ItemInsert)
        if url:
            self.cursor.execute(ItemInsert)
        #print(ItemInsert)
        #print('添加成功')

        return item

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler.settings)

    def open_spider(self,spider):
        
        self.connect = pymysql.connect(
            host = self.settings.get('MYSQL_HOST'),
            port = self.settings.get('MYSQL_POST'),
            db = self.settings.get('MYSQL_DBNAME'),
            user = self.settings.get('MYSQL_USER'),
            passwd = self.settings.get('MYSQL_PASSWD'),
            charset = 'utf8'
            )
        self.cursor = self.connect.cursor()
        #print('游标创建')
        self.connect.autocommit(1)
        #print('自动提交')

    def close_spider(self,spider):
        select_id = "select max(user_id) from renphoto"
        self.cursor.execute(select_id)
        result = self.cursor.fetchone()
        with open('id.txt','w+') as f:
            f.write('%s' % result)
        self.cursor.close()
        self.connect.close()
        #print('关闭数据库连接')









