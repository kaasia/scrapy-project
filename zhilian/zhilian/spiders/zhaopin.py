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
    allowed_domains = ["http://sou.zhaopin.com/jobs/searchresult.ashx"]
    start_urls = (
        'http://sou.zhaopin.com/jobs/searchresult.ashx',
    )
    rules = (
	Rule(LinkExtractor(allow=(r'http://sou.zhaopin.com/jobs/searchresult.ashx?p=\d+')),callback="parse"),
    )

    def parse(self, response):
        '''
	item = ZhilianItem()
	item['zwmc'] = response.selector.css('.newlist .zwmc').xpath('//span/text()').extract()
	item['gsmc'] = response.selector.css('.newlist .gsmc').xpath('text()').extract()
	item['zwyx'] = response.selector.css('.newlist .zwyx').xpath('text()').extract()
	item['gzdd'] = response.selector.css('.newlist .gzdd').xpath('text()').extract()
	yield item
	'''
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
	return items
	
