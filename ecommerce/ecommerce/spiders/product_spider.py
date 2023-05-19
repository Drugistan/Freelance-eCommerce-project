import ctypes

import scrapy

from ..items import EcommerceItem
from itemloaders import ItemLoader
import datetime


def get_date():
    current_date = datetime.date.today()
    return current_date


class ProductSpiderSpider(scrapy.Spider):
    name = "product_spider"
    allowed_domains = ["www.stratco.com.au"]
    start_urls = ["https://www.stratco.com.au"]

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'stratco.json',
        'FEED_EXPORT_INDENT': 4
    }

    def start_requests(self):
        urls = [
            'https://www.stratco.com.au/sitemap.xml'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_sitemap)

    def parse_sitemap(self, response, **kwargs):

        for loc in response.xpath('//xmlns:loc/text()',
                                  namespaces={'xmlns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}):
            yield scrapy.Request(url=loc.get(), callback=self.parse, dont_filter=True)

    def parse(self, response, **kwargs):
        category_css = None
        product_title = response.css('h1.product-detail__name::text').get()

        price_ = response.css("div.product-detail__quote > div.product-detail__price.hide-if-customised > \
                                 span.product-price__amount.product-price__amount--value:first-of-type > \
                                 span.product-price__dollars::text").get()

        if price_:
            price_handler_ = price_
        elif response.css("div.product-detail__quote > div.product-detail__price.hide-if-customised > \
                                 span.product-price__amount.product-price__amount--discount:first-of-type > \
                                 span.product-price__dollars::text").get():
            price_handler_ = response.css("div.product-detail__quote > div.product-detail__price.hide-if-customised > \
                                 span.product-price__amount.product-price__amount--discount:first-of-type > \
                                 span.product-price__dollars::text").get()
        else:
            price_handler_ = "".join("None")

        if response.css("div.product-detail__price.hide-if-customised > \
            span.product-price__amount.product-price__amount--value.product-price__amount--value-discount >\
             span.product-price__dollars::text").get():

            old_price = response.css("div.product-detail__price.hide-if-customised > \
            span.product-price__amount.product-price__amount--value.product-price__amount--value-discount > span.product-price__dollars::text").get()
        else:
            old_price = "".join("None")

        if response.css("div.layout.layout--pad-top-small.layout--pad-bottom-mid.layout-content >\
                        table > tbody > tr > td:nth-child(2)::text").getall():
            specification_ = response.css("div.layout.layout--pad-top-small.layout--pad-bottom-mid.layout-content >\
                        table > tbody > tr > td:nth-child(2)::text").getall()
        else:
            specification_ = "".join("None")

        if response.xpath("//div[@class='columns large-10 large-centered layout-content']//text()").getall():
            description_ = response.xpath(
                "//div[@class='columns large-10 large-centered layout-content']//text()").getall()
        else:
            description_ = "".join("None")


        if response.css(
                "ul.breadcrumbs li:not(:last-child) a::text").getall():
            category_css = response.css(
                "ul.breadcrumbs li:not(:last-child) a::text").getall()
        else:
            category_css = "".join("None")

        if product_title:
            item_loader = ItemLoader(item=EcommerceItem(), selector=response)

            item_loader.add_value(
                "product_link", response.url
            )
            item_loader.add_css(
                "product_name", "h1.product-detail__name::text"
            )
            item_loader.add_value(
                "gst_included", True
            )
            item_loader.add_value(
                "product_price", price_handler_
            )

            item_loader.add_value(
                "product_old_price", old_price
            )

            item_loader.add_css(
                "product_unit", "div.product-detail__price.hide-if-customised > \
                                span.product-price__quantity::text"
            )
            item_loader.add_css(
                "AUD", "div.product-detail__price.hide-if-customised > \
                                 span.product-price__amount.product-price__amount--value:first-of-type > \
                                 span.product-price__dollars:first-of-type::text"
            )
            item_loader.add_value(
                "category", category_css
            )
            item_loader.add_css(
                "product_brand", "p.product-detail__brand::text"
            )
            item_loader.add_value(
                "supplier_name", response.url
            )
            item_loader.add_value(
                "scraped_date", get_date()
            )
            item_loader.add_css(
                "image_urls", "img.product-detail-image-gallery__thumbnail-image.carousel-cell-image::attr(src)"
            )
            item_loader.add_value(
                "stock_availability", "None"
            )

            item_loader.add_value(
                "description", description_
            )
            item_loader.add_css(
                "image_paths", "img.product-detail-image-gallery__thumbnail-image.carousel-cell-image::attr(src)"
            )
            item_loader.add_value(
                "specifications", specification_
            )
            return item_loader.load_item()
