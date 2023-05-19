import re
from price_parser import Price
import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join, Compose
from urllib.parse import urlparse

""" 
    clean_product_name_maker remove extra space from string
     
     """


def clean_product_name_maker(product_name):
    return product_name.strip()


""" 
    clean_product_price_maker extract value of price without Currency Symbol
     
     """


def clean_product_price_maker(product_price):
    price_ = Price.fromstring(product_price)
    if price_:
        return str(price_.amount_float)
    return product_price


""" 
    clean_price_currency_maker extract Currency Symbol 

     """


def clean_price_currency_maker(price_currency):
    currency_ = Price.fromstring(price_currency)
    if currency_:
        currency = currency_.currency
        return currency
    return price_currency


""" 
 clean_product_unit_maker extract and clean space from EA unit 
 """


def clean_product_unit_maker(product_unit):
    print(product_unit)
    return " ".join(product_unit.split())


def make_links_maker(category):
    urls = "https://www.stratco.com.au/au/roofing--walling/gutters/"
    final_dict = {}

    final_dict.update({
        "name": category,
        "url": urls
    })
    return final_dict


""" 
    string_format method is used to clean up the category because category is extract in special character
    """


def string_format(category):
    string_ = None
    if "&" not in category and " " not in category:
        print("Single Category", category)
        return category
    else:
        if "&" in category:
            string_ = category.replace("&", "-")
            if " " in string_:
                string_ = string_.replace("  +", "-")
                if " " in string_:
                    string_ = string_.replace(" ", "")
        else:
            string_ = category.replace(" ", "-")
    return string_


""" 
url method is format the clink according to category
 """


def url(category):
    url_ = "https://www.stratco.com.au/"
    format_maker = url_ + "{}".format(string_format(category))
    url_ = format_maker
    return url_


""" 
    
    make_category_maker method is main method where category build  
 
 """


def make_category_maker(category):
    category_dict = {}
    if category == "Home":
        return category_dict.update({"Category": "None"})
    else:
        category_dict.update({
            "name": category,
            "link": url(category)
        })
        return category_dict


"""
    get_supplier_name Extract domain name 
"""


def get_supplier_name(supplier_name):
    web_name = urlparse(supplier_name).netloc
    return web_name[4:-7]


""" 
 clean_up_jpg method is used to remove width and height value of image after .jpg
 
 """


def clean_up_jpg(image):
    if ".jpg" in image:
        path_ = image.split(".jpg")[0] + ".jpg"
    else:
        path_ = image.split(".png")[0] + ".png"
    if path_:
        return path_


""" 
    The Image link build in image_url_ method
"""


def image_url_(image_urls):
    urls_ = "https://www.stratco.com.au{}".format(clean_up_jpg(image_urls))
    return urls_


"""  
Return complete image url
  """


def get_image_urls_maker(image_url):
    return image_url_(image_url)


def image_path_cleaner(image_path):
    if ".jpg" in image_path:
        path_ = image_path.split(".jpg")[0] + ".jpg"
    else:
        path_ = image_path.split(".png")[0] + ".png"
    if path_:
        return path_


"""
    get_image_path_maker method extract the image path of website
 """


def get_image_path_maker(image_path):
    return image_path_cleaner(image_path)


"""
    clean_description method clean the description
 """


def clean_description(description):
    bug_ = description
    if bug_:
        string_ = re.sub(r'[\n\t\s]+', ' ', bug_)
        return string_.strip()


class EcommerceItem(scrapy.Item):
    product_link = scrapy.Field(
        output_processor=TakeFirst())

    product_name = scrapy.Field(
        input_processor=MapCompose(clean_product_name_maker),
        output_processor=TakeFirst())

    gst_included = scrapy.Field(output_processor=TakeFirst())

    product_price = scrapy.Field(
        input_processor=MapCompose(clean_product_price_maker),
        output_processor=TakeFirst())

    product_old_price = scrapy.Field(
        input_processor=MapCompose(clean_product_price_maker),
        output_processor=TakeFirst())

    product_unit = scrapy.Field(
        input_processor=MapCompose(clean_product_unit_maker),
        output_processor=TakeFirst())

    AUD = scrapy.Field(
        input_processor=MapCompose(clean_price_currency_maker),
        output_processor=TakeFirst())

    category = scrapy.Field(
        input_processor=MapCompose(make_category_maker),
        output_processor=Compose())

    product_brand = scrapy.Field(
        output_processor=TakeFirst())

    supplier_name = scrapy.Field(
        input_processor=MapCompose(get_supplier_name),
        output_processor=TakeFirst())

    scraped_date = scrapy.Field(
        output_processor=TakeFirst())

    image_urls = scrapy.Field(
        input_processor=MapCompose(get_image_urls_maker),
        output_processor=Compose())

    stock_availability = scrapy.Field(
        output_processor=TakeFirst()
    )

    description = scrapy.Field(
        input_processor=MapCompose(clean_description),
        output_processor=Join())

    image_paths = scrapy.Field(
        input_processor=MapCompose(get_image_path_maker),
        output_processor=Compose())

    specifications = scrapy.Field(
        output_processor=Join()
    )

    """
     
     https://www.keelerhardware.com.au/ --> items start here  
     
     """


def keeler_product_name_cleaner(product_name):
    print("product_name", product_name)
    string_ = product_name.strip()
    return string_


def keeler_url(category):
    url_ = "https://www.keelerhardware.com.au/"
    format_maker = url_ + "{}".format(string_format(category))
    url_ = format_maker
    return url_


def keeler_make_category_maker(category):
    category_dict = {}
    if category == "Home":
        return category_dict.update({"Category": "None"})
    else:
        category_dict.update({
            "name": category,
            "link": keeler_url(category)
        })
        return category_dict


def keeler_make_brand_maker(product_brand):
    brand_ = product_brand.split()
    if brand_:
        return brand_[0]


def keeler_clean_up_jpg(image):
    if ".jpg" in image:
        path_ = image.split(".jpg")[0] + ".jpg"
    else:
        path_ = image.split(".png")[0] + ".png"
    if path_:
        return path_


def get_full_size(image_urls):
    divider_ = image_urls.split('/', 3)
    combiner_ = divider_[0] + '/' + "full" + '/' + divider_[3]
    return combiner_


def image_checker(image):
    if "_thumb" in image:
        new_string = image.replace('_thumb', '')
    else:
        new_string = image.replace("thumb", 'full')
    if new_string:
        return new_string


def image_url_keeler_(image_urls):
    x = image_checker(image_urls)
    urls_ = "https://www.keelerhardware.com.au{}".format(keeler_clean_up_jpg(x))
    return urls_


def keeler_get_image_urls_maker(image_url):
    print("URK", image_url)
    return image_url_keeler_(image_url)


def keeler_stock_availability_cleaner(stock_availability):
    return stock_availability[:-1]


def keeler_get_description_cleaner(list_):
    copy_list = list_
    for c in copy_list:
        if c == "\n":
            copy_list = c.lstrip("\n").rstrip("\n")
    return copy_list


class keelerItems(scrapy.Item):
    product_link = scrapy.Field(

        output_processor=TakeFirst())

    product_name = scrapy.Field(
        input_processor=MapCompose(keeler_product_name_cleaner),
        output_processor=TakeFirst())

    gst_included = scrapy.Field(
        output_processor=TakeFirst()
    )

    product_price = scrapy.Field(
        input_processor=MapCompose(clean_product_price_maker),
        output_processor=TakeFirst())

    product_unit = scrapy.Field(
        output_processor=TakeFirst())

    AUD = scrapy.Field(
        input_processor=MapCompose(clean_price_currency_maker),
        output_processor=TakeFirst())

    category = scrapy.Field(
        input_processor=MapCompose(keeler_make_category_maker),
        output_processor=Compose())

    product_brand = scrapy.Field(
        input_processor=MapCompose(keeler_make_brand_maker),
        output_processor=TakeFirst())

    supplier_name = scrapy.Field(
        input_processor=MapCompose(get_supplier_name),
        output_processor=TakeFirst())

    scraped_date = scrapy.Field(
        output_processor=TakeFirst())

    image_urls = scrapy.Field(
        input_processor=MapCompose(keeler_get_image_urls_maker),
        output_processor=Compose())

    stock_availability = scrapy.Field(
        input_processor=MapCompose(keeler_stock_availability_cleaner),
        output_processor=TakeFirst()
    )

    description = scrapy.Field(
        input_processor=MapCompose(keeler_get_description_cleaner),
        output_processor=Join())

    image_paths = scrapy.Field(
        input_processor=MapCompose(get_image_path_maker),
        output_processor=Compose())

    specifications = scrapy.Field(
        output_processor=Join()
    )

    product_old_price = scrapy.Field(
        input_processor=MapCompose(clean_product_price_maker),
        output_processor=TakeFirst()
    )

    product_discounted_prince = scrapy.Field(
        input_processor=MapCompose(clean_product_price_maker),
        output_processor=TakeFirst()
    )
