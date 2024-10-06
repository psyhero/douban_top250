import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse

from ..items import Top250Item


class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]
    
    def start_requests(self):
        total = 250
        limit = 25
        for i in range(0,total,limit):
            url = f'https://movie.douban.com/top250?start={i}&filter='

            yield Request(url=url)
            
    def parse(self, response:HtmlResponse):
        
        blocks = response.css('.info .hd')
        for it in blocks:
            detail_link = it.css('a::attr(href)').get()

            yield Request(
                url=detail_link,
                callback=self.detail_parse
            )

    def detail_parse(self,responnse:HtmlResponse):
        item = Top250Item()

        item['title'] = responnse.css('#content > h1 > span[property="v:itemreviewed"]::text').get()
        item['rating'] = float(responnse.css('#interest_sectl > div.rating_wrap.clearbox > div.rating_self.clearfix > strong::text').get())
        item['poster'] = responnse.css('#mainpic > a > img[rel="v:image"]::attr(src)').get()
        item['director'] = responnse.css('#info a[rel="v:directedBy"]::text').get()
        
        intros = responnse.xpath('//*[@id="link-report-intra"]/span[1]')
        for el in intros:
            span_text = el.xpath('.//text()').getall()            
            span_text = [text.replace('<br>', '') for text in span_text]
            span_text = [text.replace(' ', '') for text in span_text]
        item['intro'] = ''.join(span_text).strip()

        wts = responnse.css('#info > span:nth-child(3) > span.attrs > a::text')
        writers = []
        for el in wts:
            e = el.get()
            writers.append(e)
        item['writer'] = writers

        acs = responnse.css('#info a[rel="v:starring"]::text')
        actors = []
        for el in acs:
            e = el.get()
            actors.append(e)
        item['actor'] = actors

        tps = responnse.css('#info span[property="v:genre"]::text')
        types = []
        for el in tps:
            e = el.get()
            types.append(e)
        item['types'] = types

        rls = responnse.css('#info span[property="v:initialReleaseDate"]')
        rels = []
        for el in rls:
            e = el.css('::attr(content)').get()
            rels.append(e)
        item['release'] = rels

        item['duration'] = int(responnse.css('#info span[property="v:runtime"]::attr(content)').get())
        
        yield item 