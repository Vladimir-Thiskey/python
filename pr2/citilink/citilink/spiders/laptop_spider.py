import scrapy
from bs4 import BeautifulSoup
# from time import sleep


class LaptopSpider(scrapy.Spider):

    name = 'laptops'
    allowed_domains = ['www.citilink.ru']
    start_urls = ['https://www.citilink.ru/catalog/noutbuki/']

    pages_count = 14

    def start_requests(self):

        for page in range(1, self.pages_count + 1):
            # sleep(2)
            url = f'https://www.citilink.ru/catalog/noutbuki/?p={page}'
            print('Окей')
            yield scrapy.Request(url, callback=self.parse_pages)


    def parse_pages(self, response):

        laptop_pages = response.css('div.ProductCardVertical__description a::attr(href)').extract()
        for laptop_page in laptop_pages:
            print('Окей ноут')
            # sleep(3)
            url = 'https://www.citilink.ru' + laptop_page + 'properties/'
            yield scrapy.Request(url, callback=self.parse)


    def parse(self, response, **kwargs):
        # Получение названия продукта
        name_list = response.css('h1.Heading.Heading_level_1::text').get().strip().split(',')[0].split(' ')
        del name_list[0]
        name = " ".join(name_list)


        specifications = {}
        specifications_full = response.css('div.SpecificationsFull').extract()

        for specification_full in specifications_full:
            soup = BeautifulSoup(str(specification_full), 'lxml')
            key_b = BeautifulSoup(str(soup.h4), 'lxml')
            key = key_b.get_text(strip=True)

            row = {}

            for spec in soup.find_all('div', class_='Specifications__row'):
                columns = spec.find_all('div', class_='Specifications__column')
                try:
                    columns[0].div.decompose()
                    row[columns[0].get_text(strip=True)] = columns[1].get_text(strip=True)
                except AttributeError:
                    row[columns[0].get_text(strip=True)] = columns[1].get_text(strip=True)

            # проверка пренадлежности row к object
            assert isinstance(row, object)
            specifications[key] = row
            specifications.pop('None', None)


        yield {
            'name': name,
            'price': response.css('div.ProductPrice span::text')[0].get().strip() + ' руб.',
            'specifications': specifications
        }
