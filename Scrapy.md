## Scrapy 项目流程

1. 创建一个Scrapy项目

   ```python
   scrapy startproject xxx
   ```

2. 定义提取的结构化数据(Item)

3. 编写Spider并提取结构化数据

   ```python
   scrapy genspider xxx "www.example.com"
   ```

   

   ```python
   import scrapy
   
   class xxxSpider(scrapy.Spider):
       name = "xxx"                     #爬虫名称，用于启动爬虫
       allowed_domains = ["example.com"]  #约束域名（域名后缀）
       start_urls = (
           'http://www.example.com/',     #起始域名，默认请求返回给parse()
       )
       '''
       默认的第一个请求函数，如果没有重写,
       将访问start_urls,并将response传递给parse()
       '''
       def start_requests(self):
           ...
           yield scrapy.Request(new_url, meta = {}, callback = parse)
   
       '''默认接受请求start_urls后返回的response并进行回调其他函数'''
       def parse(self,response):
           ...
           yield scrapy.Request(new_url, meta = {}, callback = next_parse)
       
       '''将最后获得数据放入Item中，并传递给Piplines'''
       def last_parse(self,response):
           ...
           item = xxxItem()
           for f in item.fields:
               try:
                   item[f] = eval(f)
               except Exception as e:
                   print(e)
           yield item
       
   ```

4. 编写Piplines加工和存储数据化数据(存储到MongoDB)

   ```python
   class MongoPipline(object):
       
       def __init__(self, mongo_uri, mongo_db):
           self.mongo_url = mongo_url
           self.mongo_db = mongo_db
   
   	'''
   	默认的实例化Pipline对象的方法'''
       @classmethod
       def from_crawler(cls, crawler):
           return cls(
               mongo_url=crawler.settings.get('MONGO_URL'),    #从setting里读取URL和DB
               mongo_db=crawler.settings.get('MONGO_DB')
           )
   	'''默认的spider启动方法，这里为了启动数据库服务进行了重载'''
       def open_spider(self, spider):
           self.client = pymongo.MongoClient(self.mongo_url)
           self.db = self.client[self.mongo_db]
           print(self.db)
   	'''默认的spider关闭方法，重载关闭数据库服务'''
       def close_spider(self, spider):
           self.client.close()
   	'''默认的item处理保存方法，这里将数据写入数据库'''
       def process_item(self, item, spider):
           self.db[item.table_name].update({'link': item.get('link')}, {'$set': dict(item)}, True)
           return item
   ```

   

1. 设置修改(settings)

   ```python
   DEFAULT_REQUEST_HEADERS = {}  #默认request头部
   
   ITEM_PIPELINES = {'MovieSpider.pipelines.MongoPipline': 300}  #指定处理Item的Piplines和顺序
   MONGO_URL = 'localhost'
   MONGO_DB = 'mongo_trailer'
   
   # Enable and configure HTTP caching (disabled by default)
   # HTTPCACHE_ENABLED = True
   # HTTPCACHE_EXPIRATION_SECS = 0
   # HTTPCACHE_DIR = 'httpcache'
   # HTTPCACHE_IGNORE_HTTP_CODES = []
   # HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
   
   DOWNLOAD_TIMEOUT = time        #下载超时
   ```

   ​                         
