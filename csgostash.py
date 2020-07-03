import requests


class CsgoStashScraper:

    def __init__(self):
        self.all_weapons_links = self.get_all_weapons_links()
        self.data = self.get_data()

    def get_links(self, url, split_str):
        links = []

        response = requests.get(url)
        with open('page.html', 'w') as html:
            html.write(response.text)

        with open('page.html', 'r') as html:
            for line in html:
                if line.startswith(split_str):
                    href = line.split()[1].split('"')[1]
                    links.append(href)

        return links

    def get_all_weapons_links(self):
        return self.get_links(url='https://csgostash.com/', split_str='<li><a href="https://csgostash.com/weapon')

    def get_weapon_skins_links(self, url):
        return self.get_links(url=url, split_str='<a href="https://csgostash.com/skin')

    def get_data(self):
        return [{'weapon': link[29:], 'skins': self.get_weapon_skins_links(link)} for link in self.all_weapons_links]
