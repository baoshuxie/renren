# README
1. 本项目用来从人人网抓取图片
2. 主要思路为，从某个ID开始，每次去访问这个User-id的相册主页，再抓取相册中每个相册的url，并访问，在抓取每个相册中照片的url，访问照片的url并保存到本地
3. 要求已有名为rentest1的数据库，并有名为renphoto的数据表，列为user_id,album_id,name,_url