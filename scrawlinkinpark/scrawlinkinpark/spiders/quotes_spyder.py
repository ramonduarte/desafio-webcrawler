import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    def __init__(self, tag='', **kwargs):
        if tag:
            tag = f'tag/{tag}'
        self.start_urls = [f'https://quotes.toscrape.com/{tag}']
        super().__init__(**kwargs)


    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'title': quote.css('span.text::text').get(),
                'author': {
                    'name': quote.xpath('span/small/text()').get(),
                    'url': 'https://quotes.toscrape.com{}'.format(
                           quote.xpath('span/a/@href').get())
                },
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
