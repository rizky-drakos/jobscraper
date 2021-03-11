import scrapy


class itviecspider(scrapy.Spider):
    name = "itviec"

    start_urls = ["https://itviec.com/it-jobs"]

    def parse(self, response):
        for link in response.css("div.first-group > div.job::attr(data-search--job-selection-job-url)").getall():
            yield response.follow(link, self.parseInnerPage)

    def parseInnerPage(self, response):
        print(response.css("h1.job-details__title::text").get())