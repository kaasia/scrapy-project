# -*- coding: utf-8 -*-
import scrapy
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor 
from scrapy.selector import Selector
from zhilian.items import ZhilianItem 
class ZhaopinSpider(scrapy.Spider):
    name = "zhaopin"
    allowed_domains = ["sou.zhaopin.com"]
    start_urls = (
        'http://sou.zhaopin.com/jobs/searchresult.ashx?sg=f33d381291364665b40d9bb749ecf9ad&p=1',
    )
    rules = (
	Rule(LinkExtractor(allow=(r'http://sou.zhaopin.com/jobs/searchresult.ashx?sg=f33d381291364665b40d9bb749ecf9ad&p=\d')),callback="parse"),
    )

    def parse(self, response):
	yield scrapy.Request(response.url,callback=self.parse_content)
       	next_page = response.css('body > div.main > div.search_newlist_main > div.newlist_main > form > div.clearfix > div.newlist_wrap.fl > div.pagesDown > ul > li.pagesDown-pos > a').xpath('./@href').extract()[0]
	print next_page
	if next_page:
	    yield scrapy.Request(next_page,callback=self.parse)
    
    def parse_content(self, response):
	self.log('crawl_this_url: %s' % response.url)
	items=[]
	sel = Selector(response)
	sites_even = sel.css('#newlist_list_content_table > table')
	for i in range(1,len(sites_even)):
	    item = ZhilianItem()
	    item['zwmc'] = sites_even[i].css('tr:nth-child(1)>td.zwmc>div>a').xpath('text()').extract()
	    item['gsmc'] = sites_even[i].css('tr:nth-child(1)>td.gsmc>a').xpath('text()').extract()
 	    item['zwyx'] = sites_even[i].css('tr:nth-child(1)>td.zwyx').xpath('text()').extract()
	    item['gzdd'] = sites_even[i].css('tr:nth-child(1)>td.gzdd').xpath('text()').extract()
	    item['gxsj'] = sites_even[i].css('tr:nth-child(1)>td.gxsj>span').xpath('text()').extract()
	    items.append(item)
	yield items
	
