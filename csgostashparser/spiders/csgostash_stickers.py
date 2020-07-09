import scrapy
from scrapy.http import HtmlResponse
#from csgostashparser.items import JobparserItem


class CsgoStashSkinSpider(scrapy.Spider):
    name = 'csgostash'
    site_name = 'csgostash.com'
    allowed_domains = ['csgostash.com']
    start_urls = ['https://csgostash.com/']
    next_page_href_xpath = "//a[@class='bloko-button HH-Pager-Controls-Next HH-Pager-Control']/@href"
    vacancies_href_xpath = "//a[@class='bloko-link HH-LinkModifier']/@href"
    vacancy_name_xpath = "//h1[@class='bloko-header-1']/text()"
    vacancy_salary_xpath = "//span[@class='bloko-header-2 bloko-header-2_lite']/text()"

    href_list = ['https://csgostash.com/stickers/tournament/Berlin+2019', 'https://csgostash.com/stickers/tournament/Katowice+2019', 'https://csgostash.com/stickers/tournament/London+2018', 'https://csgostash.com/stickers/tournament/Boston+2018', 'https://csgostash.com/stickers/tournament/Krakow+2017', 'https://csgostash.com/stickers/tournament/Atlanta+2017', 'https://csgostash.com/stickers/tournament/Cologne+2016', 'https://csgostash.com/stickers/tournament/MLG+Columbus+2016', 'https://csgostash.com/stickers/tournament/Cluj-Napoca+2015', 'https://csgostash.com/stickers/tournament/Cologne+2015', 'https://csgostash.com/stickers/tournament/Katowice+2015', 'https://csgostash.com/stickers/tournament/DreamHack+2014', 'https://csgostash.com/stickers/tournament/Cologne+2014', 'https://csgostash.com/stickers/tournament/Katowice+2014']
    href_index = 0

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(self.next_page_href_xpath).extract_first()
        if next_page is None:
            yield
        yield response.follow(next_page, callback=self.parse)

        vac_list = response.xpath(self.vacancies_href_xpath).extract()
        for link in vac_list:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath(self.vacancy_name_xpath).extract()[0]
        salary = response.xpath(self.vacancy_salary_xpath).extract()
        href = response.url
        site_name = self.site_name
        #yield JobparserItem(name=name, salary=salary, href=href, site_name=site_name)








