import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/login"]

    current = 0
    max_page = 1

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
    }

    def parse(self, response):
        csrf_token = response.xpath('//input[@name="csrf_token"]/@value').get()
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'csrf_token': csrf_token,
                'username':'admin',
                'password':'admin'
            },
            callback=self.after_login
        )

    def after_login(self, response):
        elements = response.xpath("//div[@class='quote']")
        for element in elements:
            text = element.xpath(".//span[@class='text']/text()").get()
            author = element.xpath(".//small[@class='author']/text()").get()
            yield {
                'text': text,
                'author':author
            }

        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page is not None and self.current < self.max_page:
            self.current += 1
            yield response.follow(next_page, callback=self.after_login)