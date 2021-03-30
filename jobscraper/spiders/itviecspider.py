import re
import scrapy
import time
import random
import logging

from datetime import datetime

class itviecspider(scrapy.Spider):
    name = "itviec"

    start_urls = ["https://itviec.com/it-jobs"]

    def parse(self, response):
        for link in response.css("div.first-group > div.job::attr(data-search--job-selection-job-url)").getall():
            sleeping_interval = random.choice([2, 3, 5])
            time.sleep(sleeping_interval)
            logging.critical(f"Scraping {link}")
            yield response.follow(link, self.parseInnerPage)

        next_page = response.css("div.search-page__jobs-pagination > ul > li:last-child > a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)

        # For debugging
        # logging.info("MEE it-jobs/ky-su-phat-trien-ung-dung-smartphone-i-enter-asia-5226/content")
        # yield response.follow("it-jobs/ky-su-phat-trien-ung-dung-smartphone-i-enter-asia-5226/content", self.parseInnerPage)

    def parseInnerPage(self, response):
        yield {
            "id": re.search('\d+', response.url).group(),
            "title": response.css("h1.job-details__title::text").get(),
            "company_name": response.css("div.job-details__sub-title::text").get(),
            "tags": response.css("div.job-details__tag-list > a  > span::text").getall(),
            "location": response.css("div.job-details__overview > div:nth-child(3) > div > span::text, div:nth-child(4) > div > span::text").getall(),
            "scraped_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "posted_at": response.css("div > div.job-details__overview > div:last-child > div::text").get(),
            "three_reasons": response.css("div > div.job-details__top-reason-to-join-us > ul > li::text").getall(),
            "description": response.css("body > div.search-page__job-details > div > div:nth-child(7) *::text, div:nth-child(8) *::text").getall(),
            "required_skills": response.css("div.search-page__job-details > div > div:nth-child(9) *::text, div:nth-child(10) *::text").getall(),
            "benefits": response.css("div.search-page__job-details > div > div:nth-child(11) *::text, div:nth-child(12) *::text").getall(),
            "company_slogan": response.css("div.search-page-employer-overview__header > div.search-page-employer-overview__headline > span::text").get(),
            "company_type": response.css("div.search-page-employer-overview__content > div.search-page-employer-overview__characteristics > div:nth-child(1) > div::text").get(),
            "company_population": response.css("div.search-page-employer-overview__content > div.search-page-employer-overview__characteristics > div:nth-child(2) > div::text").get(),
            "working_days": response.css("div.search-page-employer-overview__content > div.search-page-employer-overview__characteristics > div:nth-child(3) > div::text").get(),
            "company_nationality": response.css("div.search-page-employer-overview__content > div.search-page-employer-overview__characteristics > div:nth-child(4) > div::text").get(),
            "OT_policy": response.css("div.search-page-employer-overview__content > div.search-page-employer-overview__characteristics > div:nth-child(5) > div::text").get()
        }
