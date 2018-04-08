# -*- coding: utf-8 -*-
import scrapy,os,time
from scrapy import Request
from SinaChina.items import SinachinaItem


class SianchinaSpider(scrapy.Spider):
    name = 'sinachina'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):

        myitems = []
        item = SinachinaItem()

        datas = response.xpath("//div[@class='clearfix']")

        for data in datas:
            if not len(data.xpath("./h3[@class='tit02']/a/text()")) == 0:
                # print(response.xpath("./h3[@class='tit02']/a/text()"),response.xpath("./h3[@class='tit02']/a/@href"))
                big_title = data.xpath("./h3[@class='tit02']/a/text()")


            else:
                if not len(data.xpath("./h3[@class='tit02']/span/text()")) == 0:
                    # print(response.xpath("./h3[@class='tit02']/span/text()"),' ')
                    big_title = data.xpath("./h3[@class='tit02']/span/text()")
                    # biglist.append()
                else:
                    # print(response.xpath("./h3[@class='tit02']/text()"),' ')
                    big_title = data.xpath("./h3[@class='tit02']/text()")
                    # biglist.append()

            # print(big_title.extract()[0])


            lines = data.xpath("./ul//li")
            for line in lines:
                small_title = line.xpath("./a/text()").extract()[0]
                url = line.xpath("./a/@href").extract()[0]

                # print('---', small_title, url)

                time.sleep(0.5)

                request =  Request(url=url,callback=self.nav_parse)
                request.meta['big_title'] = big_title.extract()[0]
                request.meta['small_title'] = small_title
                yield request




    def nav_parse(self,response):

        # print(response.meta['big_title'])
        # print('---', response.meta['small_title'])

        nav_list = response.xpath("//div[@class='second-nav']//div//div//a")

        for nav in nav_list:
            nav_title = nav.xpath("./text()").extract()[0]
            nav_url = nav.xpath("./@href").extract()[0]
            # print('-----', nav_title, nav_url)

            request =  Request(nav_url,callback=self.china_parse)

            request.meta['big_title'] = response.meta['big_title']
            request.meta['small_title'] = response.meta['small_title']
            request.meta['nav_title'] = nav_title
            yield request


    def china_parse(self, response):
        # print(response.text)

        # 下一页的连接
        new_url = response.xpath("//div[@class='pagebox']//span[@class='pagebox_next']//a/@href")
        # print(new_url)

        page_num = 1

        if not len(new_url) == 0 and page_num < 5:

            new_url = new_url.extract()[0][2:]

            urllist = response.url.split('/')

            next_page = ""
            for i in range(len(urllist) - 1):
                next_page += urllist[i]
                next_page += '/'
            next_page += new_url

            lines = response.xpath("//ul[@class='list_009']//li")

            if not len(lines) == 0:
                for line in lines:
                    page_url = line.xpath("./a/@href").extract()[0]
                    # print(page_url)
                    request =  Request(url=page_url, callback=self.get_page)
                    request.meta['big_title'] = response.meta['big_title']
                    request.meta['small_title'] = response.meta['small_title']
                    request.meta['nav_title'] = response.meta['nav_title']
                    yield request

                yield Request(url=next_page,callback=self.china_parse)
            else:
                print('已经没有文章了，spider结束')
            page_num += 1
        else:
            print('当前没有新闻列表！')


    def get_page(self,response):
        item = SinachinaItem()

        title = response.xpath("//h1[@class='main-title']/text()").extract()

        if not len(title) == 0:

            item['big_title'] = response.meta['big_title']
            item['small_title'] = response.meta['small_title']
            item['nav_title'] = response.meta['nav_title']

            item["title"]=title[0]

            lines = response.xpath("//div[@id='article']//p/text()").extract()
            content = ""
            for line in lines:
                content += line
                content += '\n'
            # print(content)

            item["content"] = content

            yield item
        else:
            print('-----存储%s文章出错！！-----' % title)

