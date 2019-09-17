import scrapy
import json
from urllib.parse import urljoin


class RatingSpider(scrapy.Spider):
    name = "rating"
    start_urls = [
    'https://www.imdb.com/title/tt4154796/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt2527338/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt4154664/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt0448115/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt0033563/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt3741700/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt3513498/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt6320628/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt2386490/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt1979376/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt5113040/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt4520988/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt6095472/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt7349950/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt2283336/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt2139881/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt7329656/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt0103639/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt5884052/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt0167190/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt0110357/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt6565702/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt7975244/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt6823368/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt6513120/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt1206885/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt7634968/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt1560220/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt0160127/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt6806448/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt8155288/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt0233298/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt0437086/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt2049619/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt0101272/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt5968394/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt0379786/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt5961976/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt5886046/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt2452244/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt7043012/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt0075860/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt1298644/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt4777008/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt8350360/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt0098084/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt1488606/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt0043827/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt0162650/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt6198946/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt2011300/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt1781769/reviews?ref_=tt_urv', 
    'https://www.imdb.com/title/tt5574166/reviews?ref_=tt_urv'
    ]

    def parse(self, response):
        names = response.xpath(
            '//div[@class="display-name-date"]//span[@class="display-name-link"]//a/text()'
        ).extract()
        titles = response.xpath('//a[@class="title"]/text()').extract()
        ratings = response.xpath(
            "//div[@class='ipl-ratings-bar']//span[@class='rating-other-user-rating']//span[not(contains(@class, 'point-scale'))]/text()"
        ).extract()
        texts = response.xpath(
            "//div[@class='text show-more__control']/text()"
        ).extract()

        for name, title, rating, text in zip(names, titles, ratings, texts):
            content = {
                "names": name,
                "title": title,
                "ratings": rating,
                "review_text": text,
            }
            yield content

        key = response.css("div.load-more-data::attr(data-key)").get()
        orig_url = response.meta.get(
            "orig_url", response.url
        )  # Get original request url
        next_url = urljoin(orig_url, "reviews/_ajax?paginationKey={}".format(key))
        if key:
            yield scrapy.Request(next_url, meta={"orig_url": orig_url})  # call back

