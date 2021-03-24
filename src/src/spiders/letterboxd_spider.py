# imports
import scrapy


class LetterboxdSpider(scrapy.Spider):
    name = "letterboxd"
    allowed_domains = ["letterboxd.com"]
    start_urls = ["https://letterboxd.com/fruityjames/films/"]


    def parse(self, response):
        data = {}
        data['title'] = response.css
