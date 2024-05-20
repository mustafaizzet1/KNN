import scrapy
import json
import re
from scrapy import Selector
from scrapy_splash import SplashRequest

class ProductSpider(scrapy.Spider):
    name = 'product_spider'
    start_urls = ['https://www.petlebi.com/kedi-petshop-urunleri','https://www.petlebi.com/kopek-petshop-urunleri','https://www.petlebi.com/kus-petshop-urunleri','https://www.petlebi.com/kemirgen-petshop-urunleri']
    custom_settings = {
        'ROBOTSTXT_OBEY': True,  # Respect robots.txt rules
    }
    all_product_info = []

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint='execute', args={'wait': 2})

    def parse(self, response):
        product_links = response.css('a.p-link::attr(href)').extract()
        for product_link in product_links:
            yield SplashRequest(url=response.urljoin(product_link), callback=self.parse_product, endpoint='execute', args={'wait': 2})

        # Check if there are more products to load and make additional requests if necessary
        next_page = response.css('a[rel="next"]::attr(href)').extract_first()
        if next_page:
            yield SplashRequest(url=response.urljoin(next_page), callback=self.parse, endpoint='execute', args={'wait': 2})

    def parse_product(self, response):
        json_ld_scripts = response.xpath('//script[@type="application/ld+json"]/text()').getall()
        id_value= response.xpath('//div[@id="ETBIS"]/div/@id').get()

        for json_ld_script in json_ld_scripts:
            corrected_json = json_ld_script.replace("&amp;", "&").replace("\n", "").replace("\r", "")
            corrected_json = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', corrected_json)
            try:
                product_data = json.loads(corrected_json)
                product_info = self.extract_product_info(product_data, id_value)
                # Append the product_info dictionary to the list
                self.all_product_info.append(product_info)
            except json.JSONDecodeError as e:
                print("Error parsing JSON:", e)
                # Optionally, you can log the error or handle it in another way
            except Exception as e:
                print("An unexpected error occurred:", e)
                # Handle any other unexpected errors here

    def extract_product_info(self, product_data, id_value):
        product_url = product_data.get('offers', {}).get('url')
        product_name = product_data.get('name')
        product_barcode = id_value
        product_price = product_data.get('offers', {}).get('price')
        product_stock = product_data.get('offers', {}).get('availability')
        product_images = product_data.get('image')
        product_description = product_data.get('description')
        product_sku = product_data.get('sku')
        product_category = product_data.get('category')
        product_id = product_data.get('gtin13')
        product_brand = product_data.get('brand', {}).get('name')

        return {
            'product_url': product_url,
            'product_name': product_name,
            'product_barcode': product_barcode,
            'product_price': product_price,
            'product_stock': product_stock,
            'product_images': product_images,
            'product_description': product_description,
            'product_sku': product_sku,
            'product_category': product_category,
            'product_id': product_id,
            'product_brand': product_brand
        }

    def closed(self, reason):
        self.writing()

    def writing(self):
        with open('petlebi_products.json', 'a', encoding='utf-8') as json_file:
            json.dump(self.all_product_info, json_file, indent=4, ensure_ascii=False)
