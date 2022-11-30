import scrapy
from ..items import Bosspro2Item

# scrapy crawl boss2 --nolog
class Boss2Spider(scrapy.Spider):
    name = 'boss2'
    # allowed_domains = ['boss2.com']
    start_urls = [
        'https://www.liepin.com/zhaopin/?inputFrom=www_index&workYearCode=0&key=python&scene=input&ckId=b3i52zdict8edus6j0r2ce0t5ae2jmo8',
        'https://www.liepin.com/zhaopin/?headId=3c956d797348b5d520fe79ecd07cf202&ckId=unngerm104trn9nf0zqb0i1gx0xbhqm8&oldCkId=3c956d797348b5d520fe79ecd07cf202&fkId=jfp4r24m20uq19dcs8h2bzjzngifoqr8&skId=jfp4r24m20uq19dcs8h2bzjzngifoqr8&sfrom=search_job_pc&key=python&currentPage=1&scene=page',
        'https://www.liepin.com/zhaopin/?headId=3c956d797348b5d520fe79ecd07cf202&ckId=uon1dlmkl324w21d74chvzwmnx0weqta&oldCkId=3c956d797348b5d520fe79ecd07cf202&fkId=jfp4r24m20uq19dcs8h2bzjzngifoqr8&skId=jfp4r24m20uq19dcs8h2bzjzngifoqr8&sfrom=search_job_pc&key=python&currentPage=2&scene=page',
    ]


    def parse(self, response, **kwargs):
        li_list = response.xpath('/html/body/div/div/section[1]/div/ul/li')
        for li in li_list:
            item = Bosspro2Item()
            url_detail = li.xpath('./div/div/div[1]/div/a[1]/@href').extract_first()
            item['job_salary'] = li.xpath('./div/div/div[1]/div/a[1]/div[1]/span/text()').extract_first()
            print(item['job_salary'])
            # print(url_detail)
            yield scrapy.Request(url_detail,callback=self.detail_parse,meta={'item': item})
        pass

    def detail_parse(self, response, **kwargs):
        item = response.meta['item']
        item['job_name'] = response.xpath('/html/body/section[3]/div[1]/div[1]/span[1]/text()').extract_first()
        item['job_address'] = response.xpath('/html/body/section[3]/div[1]/div[2]/span[1]/text()').extract_first()
        item['job_demand'] = response.xpath('/html/body/main/content/section[2]/dl/dd/text()').extract_first()

        yield item
        pass

