# -*- coding: utf-8 -*-
import scrapy
import json
#from scrapy.spiders import CrawlSpider,Rule
#from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request,FormRequest
from rentest1.items import Rentest1Item
import requests
import re
import math

class RenrenSpider(scrapy.Spider):
  name = 'renphoto1'
  allowed_domains = ['renren.com']
  
  #start_urls = ['http://follow.renren.com/list/965740621/pub/v7']
  #todo_urls = 
  #seen_urls = 
  #rules = (
  # Rule(LinkExtractor(allow = ('http://follow.renren.com/list/\d{9}/pub/v7')),callback='parse_urls',follow=True))
  
  def start_requests(self):
    return [Request('http://www.renren.com/SysHome.do',callback=self.post_login,dont_filter=True)]

  def post_login(self, response):
    print('OK1')
    return [FormRequest.from_response(response,formdata={
      'email':'13689024414',
      #'icode':'',                        
      #'origURL':'http://www.renren.com/home',
      #'domain':'renren.com',
      #'key_id':'1',
      #'captcha_type':'web_login',
      'password':'19950708',
      #'rkey':'9169051cc2aba8b879f01dfda84ce597',
      #'f':'http%3A%2F%2Fzhibo.renren.com%2Ftop',
      },
#     meta = {'cookiejar':1},
      callback = self.parse_user_id,
      dont_filter=True
      )]

  def parse_user_id(self,response):
    print('OK3')
    with open('id.txt','r') as f:
      user_id = int(f.read())
    
    for i in range(0,10000):
        user_id = user_id
        url='http://photo.renren.com/photo/' + '%s' % str(user_id) + '/albumlist/v7'
        yield Request(url,
        meta = {#'cookiejar':response.meta['cookiejar'],
        'user_id':user_id},
        callback=self.parse_album_urls,
  #        dont_filter=True
                    )
      
  '''def parse_user_ids(self,response):
    
    yield Request("http://photo.renren.com/photo/500999244/albumlist/v7?offset=0&limit=40#",
      meta = {'cookiejar':response.meta['cookiejar'],'user_id':'500999244'},
      callback=self.parse_album_urls,
      dont_filter=True)'''

  def parse_album_urls(self,response):
    album_pages = response.xpath('/*').re(r'"albumId":"\d{9}"')
    album_numbers = response.xpath('/*').re(r'"photoCount":\d+')
    if not album_pages:
      return 
    
    album_ids = []
    for album_page in album_pages:      
      album_id= album_page[11:20]
      album_ids.append(album_id)
    
    album_counts=[]
    for album_number in album_numbers:      
      album_count = album_number[13:]     
      album_counts.append(album_count)
    
    album_urls=[]
    json_urls=[]
    for i in range(0,len(album_ids)):
      for x in range(1,math.ceil(int(album_counts[i])/20)+1):
        url = 'http://photo.renren.com/photo/' + str(response.meta['user_id']) + '/album-' + str(album_ids[i]) + '/bypage/ajax/v7?page=%d&pageSize=20' % x           
           #http://photo.renren.com/photo/500999244/album-848184418/bypage/ajax/v7?page=3&pageSize=20
    
        yield Request(url,
          meta={
          #'cookiejar':response.meta['cookiejar'],
          'user_id':response.meta['user_id'],'album_id':album_ids[i]},
          callback = self.save_item,
#          dont_filter = True
          )

  def save_item(self,response):
    print(response.status)

    if response.status == 302:
      yield Request('http://www.renren.com/SysHome.do',callback=self.post_login,dont_filter=True)
    js = json.loads(response.body)
    for j in js['photoList']:
      item = Rentest1Item()
      item['user_id'] = response.meta['user_id']
      item['album_id'] = response.meta['album_id']
      item['url']= j['url']
      name = j['url'].replace('/','_')
      item['name'] = name
      print(item)
      yield item


