import requests
from pprint import pprint
from bs4 import BeautifulSoup


class CsgoStashScraper:

    def __init__(self):
        self.all_weapons_links = self.get_all_weapons_links()
        self.all_weapons_skins = self.get_all_weapons_skins()
        self.full_data = self.get_all_skins_data()

    def parse_html(self, response):
        return BeautifulSoup(response.text, 'lxml')

    def get_all_weapons_links(self, url='https://csgostash.com'):
        links = []

        response = requests.get(url)
        parsed_html = self.parse_html(response)

        for dropdown in parsed_html.find_all('li', {'class': 'dropdown'})[:5]:
            hrefs = [elem['href'] for elem in dropdown.find_all('a')[1:]]
            links += hrefs

        return links

    def get_weapon_skins_links(self, url):
        links = []

        response = requests.get(url)
        parsed_html = self.parse_html(response)

        for skin in parsed_html.find_all('div', {'class': 'well result-box nomargin'}):
            try:
                href = skin.find_all('a')[-1]['href']
                links.append(href)
            except:
                # Реклама
                pass

        return links

    def get_all_weapons_skins(self):
        return [{'weapon': link[29:], 'skins': self.get_weapon_skins_links(link)} for link in self.all_weapons_links]

    def get_skin_data_block(self, url):
        response = requests.get(url)
        return self.parse_html(response).find('div', {'class': 'price-details-table-wrapper'})

    def get_skin_data(self, url):
        data = {}
        price_block = self.get_skin_data_block(url).find('tbody')
        #print(price_block)
        for row in price_block.find_all('tr'):
            columns = row.find_all('td')

            quality = columns[0].text[1:-1]
            data.update({quality: {}})
            try:
                data.update({quality: {'price': float(columns[1].find('a').text.replace(' ', '')[:-4].replace(',', '.'))}
                             })
            except:
                data[quality]['price'] = None

            try:
                data[quality]['listings'] = int(columns[2].text[1:-1])
            except:
                data[quality]['listings'] = None

            try:
                data[quality]['median'] = columns[3].find('a').text.replace(' ', '')[:-4].replace(',', '.')
            except:
                data[quality]['median'] = None

            try:
                data[quality]['volume'] = int(columns[4].text[1:-1])
            except:
                data[quality]['volume'] = None

            try:
                data[quality]['bit_price'] = columns[5].find('a').text.replace(' ', '')[:-4].replace(',', '.')
            except:
                data[quality]['bit_price'] = None

        return data

    def get_all_skins_data(self):
        all_skins_data = []

        for weapon in self.all_weapons_skins:
            for skin in weapon['skins']:
                data = {}
                data['weapon'] = weapon['weapon']
                data['skin'] = skin
                data['market_data'] = self.get_skin_data(skin)

                all_skins_data.append(data)
                pprint(data)
            #print(all_skins_data)

        return all_skins_data

