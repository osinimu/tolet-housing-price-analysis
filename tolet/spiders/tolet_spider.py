import scrapy
from scrapy.selector import Selector
from scrapy.exceptions import CloseSpider
from scrapy.http import Request
from tolet.items import ToletItem

URL = "https://www.tolet.com.ng/property-for-rent?page=1"

class ToletSpider(scrapy.Spider):
    name= "tolet"
    allowed_domains = ["www.tolet.com.ng"]
    start_urls = [ "https://www.tolet.com.ng/property-for-rent",
     ]
   
    
    def parse(self, response):
        properties = Selector(response).xpath('//div[@class="property"]')
        
        
        for apartment in properties:
            item = ToletItem()
            item['property_name'] = apartment.xpath('div[@class="row"]/div[contains(@class, "property-caption col-lg-12")]/a/h2/text()').extract()
            item['Price'] = apartment.xpath('div[@class="row"]/div[contains(@class, "property-metadata col-lg-6")]/h5[@class="property-price"]/span[@itemprop="price"]/text()').extract()
            item['Address'] = apartment.xpath('div[@class="row"]/div[contains(@class, "property-metadata col-lg-6")]/h5[@class="property-area"]/text()').extract()
            yield item
            
        next_page = response.xpath("//a[@alt='view next property page']/@href").extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
            
        