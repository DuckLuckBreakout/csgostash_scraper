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

    href_list = ['https://csgostash.com/case/303/Prisma-2-Case', 'https://csgostash.com/case/277/Shattered-Web-Case', 'https://csgostash.com/case/293/CS20-Case', 'https://csgostash.com/case/274/Prisma-Case', 'https://csgostash.com/case/259/Danger-Zone-Case', 'https://csgostash.com/case/244/Horizon-Case', 'https://csgostash.com/case/238/Clutch-Case', 'https://csgostash.com/case/1/CS:GO-Weapon-Case', 'https://csgostash.com/case/4/CS:GO-Weapon-Case-2', 'https://csgostash.com/case/10/CS:GO-Weapon-Case-3', 'https://csgostash.com/case/38/Chroma-Case', 'https://csgostash.com/case/48/Chroma-2-Case', 'https://csgostash.com/case/141/Chroma-3-Case', 'https://csgostash.com/case/2/eSports-2013-Case', 'https://csgostash.com/case/5/eSports-2013-Winter-Case', 'https://csgostash.com/case/19/eSports-2014-Summer-Case', 'https://csgostash.com/case/50/Falchion-Case', 'https://csgostash.com/case/144/Gamma-Case', 'https://csgostash.com/case/172/Gamma-2-Case', 'https://csgostash.com/case/179/Glove-Case', 'https://csgostash.com/case/17/Huntsman-Weapon-Case', 'https://csgostash.com/case/3/Operation-Bravo-Case', 'https://csgostash.com/case/18/Operation-Breakout-Weapon-Case', 'https://csgostash.com/case/208/Operation-Hydra-Case', 'https://csgostash.com/case/11/Operation-Phoenix-Weapon-Case', 'https://csgostash.com/case/29/Operation-Vanguard-Weapon-Case', 'https://csgostash.com/case/112/Operation-Wildfire-Case', 'https://csgostash.com/case/111/Revolver-Case', 'https://csgostash.com/case/80/Shadow-Case', 'https://csgostash.com/case/207/Spectrum-Case', 'https://csgostash.com/case/220/Spectrum-2-Case', 'https://csgostash.com/case/7/Winter-Offensive-Weapon-Case']
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
       # yield JobparserItem(name=name, salary=salary, href=href, site_name=site_name)








