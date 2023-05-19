import datetime

import scrapy
from itemloaders import ItemLoader

from bs4 import BeautifulSoup

from ..items import keelerItems

"""
    get_date method is used extract current date when spider is run
"""


def get_date():
    current_date = datetime.date.today()
    return current_date


class KeelerhardwareSpider(scrapy.Spider):
    name = "keelerhardware"
    allowed_domains = ["www.keelerhardware.com.au"]
    start_urls = ["https://www.keelerhardware.com.au/"]

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'Keeler.json',
        'FEED_EXPORT_INDENT': 4
    }

    """ 
    Read XML file Because i dnt have sitemap link
     """

    def start_requests(self):
        with open("spiders/file/sitemap.xml", "r") as filer_reader:
            data_ = filer_reader.read()
            try:
                if data_:
                    bs4_request = BeautifulSoup(data_, "xml")
                    for loc in bs4_request.find_all('loc'):
                        url_ = loc.text
                        yield scrapy.Request(
                            url=url_,
                            callback=self.product_inside_url)
            except Exception as e:
                print(e)

    def product_inside_url(self, response):
        url_css = response.css("div.caption > p.h3 > a::attr(href)").getall()
        for link in url_css:
            yield scrapy.Request(
                url=link,
                callback=self.parse)

    def parse(self, response, **kwargs):
        item_loader = ItemLoader(item=keelerItems(), selector=response)

        if response.css("div.available-box > div.available-header::text").get():
            stock_availability = response.css("div.available-box > div.available-header::text").get()
        else:
            stock_availability = "".join("None")

        if response.css("div.dah_pprice > div.productrrp.text-muted::text").get():
            is_old_price = response.css("div.dah_pprice > div.productrrp.text-muted::text").get()
        else:
            is_old_price = "".join("None")

        if response.css("div.dah_pprice > p.product-save-text::text").get():
            save_price = response.css("div.dah_pprice > p.product-save-text::text").get()
        else:
            save_price = "".join("None")

        if response.css(
                "div.tab-content > div#description > section.productdetails.n-responsive-content p::text").getall():
            description_ = response.css(
                "div.tab-content > div#description > section.productdetails.n-responsive-content p::text").getall()
        else:
            description_ = "".join("None")

        item_loader.add_value(
            "product_link", response.url
        )

        item_loader.add_css(
            "product_name", "div.wrapper-product-title.col-xs-12 > h1::text"
        )

        item_loader.add_value(
            "gst_included", True
        )

        item_loader.add_css(
            "product_price", "div.productprice.productpricetext::text"
        )

        item_loader.add_value(
            "product_unit", "None"
        )

        item_loader.add_css(
            "AUD", "div.productprice.productpricetext::text"
        )

        item_loader.add_xpath(
            "category", "//ul[@class='breadcrumb']//li[position() < last()]//a//text()"
        )

        item_loader.add_css(
            "product_brand", "div.row > div.wrapper-product-title.col-xs-12 > h1::text"
        )

        item_loader.add_value(
            "supplier_name", response.url
        )

        item_loader.add_value(
            "scraped_date", get_date()
        )

        item_loader.add_css(
            "image_urls", "a.thumb-image.fancybox > img.img-responsive.product-image-small::attr(src)"
        )

        item_loader.add_value(
            "stock_availability", stock_availability
        )

        item_loader.add_value(
            "description", description_
        )

        item_loader.add_css(
            "image_paths", "a.thumb-image.fancybox > img.img-responsive.product-image-small::attr(src)"
        )

        item_loader.add_css(
            "specifications", "#specifications table.table tbody tr td:nth-child(2)::text"
        )

        item_loader.add_value(
            "product_old_price", is_old_price
        )

        item_loader.add_value(
            "product_discounted_prince", save_price
        )

        return item_loader.load_item()
