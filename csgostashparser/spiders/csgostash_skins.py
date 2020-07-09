import scrapy
from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup

from csgostashparser.items import SkinParserItem


class CsgoStashSkinSpider(scrapy.Spider):
    name = 'csgostash'
    site_name = 'csgostash.com'
    allowed_domains = ['csgostash.com']
    start_urls = ['https://csgostash.com/']
    next_page_href_xpath = "//a[@class='bloko-button HH-Pager-Controls-Next HH-Pager-Control']/@href"
    vacancies_href_xpath = "//a[@class='bloko-link HH-LinkModifier']/@href"
    vacancy_name_xpath = "//h1[@class='bloko-header-1']/text()"
    vacancy_salary_xpath = "//span[@class='bloko-header-2 bloko-header-2_lite']/text()"

    href_list = ['https://csgostash.com/weapon/CZ75-Auto', 'https://csgostash.com/weapon/Desert+Eagle', 'https://csgostash.com/weapon/Dual+Berettas', 'https://csgostash.com/weapon/Five-SeveN', 'https://csgostash.com/weapon/Glock-18', 'https://csgostash.com/weapon/P2000', 'https://csgostash.com/weapon/P250', 'https://csgostash.com/weapon/R8+Revolver', 'https://csgostash.com/weapon/Tec-9', 'https://csgostash.com/weapon/USP-S', 'https://csgostash.com/weapon/AK-47', 'https://csgostash.com/weapon/AUG', 'https://csgostash.com/weapon/AWP', 'https://csgostash.com/weapon/FAMAS', 'https://csgostash.com/weapon/G3SG1', 'https://csgostash.com/weapon/Galil+AR', 'https://csgostash.com/weapon/M4A1-S', 'https://csgostash.com/weapon/M4A4', 'https://csgostash.com/weapon/SCAR-20', 'https://csgostash.com/weapon/SG+553', 'https://csgostash.com/weapon/SSG+08', 'https://csgostash.com/weapon/MAC-10', 'https://csgostash.com/weapon/MP5-SD', 'https://csgostash.com/weapon/MP7', 'https://csgostash.com/weapon/MP9', 'https://csgostash.com/weapon/PP-Bizon', 'https://csgostash.com/weapon/P90', 'https://csgostash.com/weapon/UMP-45', 'https://csgostash.com/weapon/MAG-7', 'https://csgostash.com/weapon/Nova', 'https://csgostash.com/weapon/Sawed-Off', 'https://csgostash.com/weapon/XM1014', 'https://csgostash.com/weapon/M249', 'https://csgostash.com/weapon/Negev', 'https://csgostash.com/weapon/Nomad+Knife', 'https://csgostash.com/weapon/Skeleton+Knife', 'https://csgostash.com/weapon/Survival+Knife', 'https://csgostash.com/weapon/Paracord+Knife', 'https://csgostash.com/weapon/Classic+Knife', 'https://csgostash.com/weapon/Bayonet', 'https://csgostash.com/weapon/Bowie+Knife', 'https://csgostash.com/weapon/Butterfly+Knife', 'https://csgostash.com/weapon/Falchion+Knife', 'https://csgostash.com/weapon/Flip+Knife', 'https://csgostash.com/weapon/Gut+Knife', 'https://csgostash.com/weapon/Huntsman+Knife', 'https://csgostash.com/weapon/Karambit', 'https://csgostash.com/weapon/M9+Bayonet', 'https://csgostash.com/weapon/Navaja+Knife', 'https://csgostash.com/weapon/Shadow+Daggers', 'https://csgostash.com/weapon/Stiletto+Knife', 'https://csgostash.com/weapon/Talon+Knife', 'https://csgostash.com/weapon/Ursus+Knife']
    href_index = 0

    def parse(self, response: HtmlResponse):
        if self.href_index == len(self.href_list):
            yield
        next_page = self.href_list[self.href_index]
        self.href_index += 1
        yield response.follow(next_page, callback=self.parse)

        skins_list = response.xpath('//div[@class="well result-box nomargin"]/a[2]/@href').extract()
        for skin in skins_list:
            yield response.follow(skin, callback=self.skin_parse)

    def skin_parse(self, response: HtmlResponse):
        name = response.xpath('//div[@class="well result-box nomargin"]/h2/a/text()').extract()[0] + ' | ' + \
               response.xpath('//div[@class="well result-box nomargin"]/h2/a/text()').extract()[1]

        parsed_html = BeautifulSoup(response.body, 'lxml')
        info_table = {}
        price_block = parsed_html.find('tbody')
        for row in price_block.find_all('tr'):
            columns = row.find_all('td')

            quality = columns[0].text[1:-1]
            info_table.update({quality: {}})
            try:
                info_table.update(
                    {quality: {'price': float(columns[1].find('a').text.replace(' ', '')[:-4].replace(',', '.'))}
                     })
            except:
                info_table[quality]['price'] = None

            try:
                info_table[quality]['listings'] = int(columns[2].text[1:-1])
            except:
                info_table[quality]['listings'] = None

            try:
                info_table[quality]['median'] = columns[3].find('a').text.replace(' ', '')[:-4].replace(',', '.')
            except:
                info_table[quality]['median'] = None

            try:
                info_table[quality]['volume'] = int(columns[4].text[1:-1])
            except:
                info_table[quality]['volume'] = None

            try:
                info_table[quality]['bit_price'] = columns[5].find('a').text.replace(' ', '')[:-4].replace(',', '.')
            except:
                info_table[quality]['bit_price'] = None

        csgostash_url = response.url
        site_name = self.site_name
        yield SkinParserItem(name=name, info_table=info_table, href=csgostash_url, site_name=site_name)








