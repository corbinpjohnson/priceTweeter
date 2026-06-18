from twython import Twython
import json
from main import CreateData
from pyshorteners import Shortener
import time
import requests
from config import load_config
from s3_file_download import FileDownload
from s3_file_upload import FileUpload


def lambda_handler(event, context):

    config = load_config()
    keys = config["twitter"]
    tweets = config["tweets"]

    twitter = Twython(keys["APP_KEY"], keys["APP_SECRET"], keys["OAUTH_TOKEN"],
                        keys["OAUTH_TOKEN_SECRET"])

    fdownload = FileDownload()
    fdownload.file_download()

    cd = CreateData()
    new_data_filename = cd.create_data()

    fupload = FileUpload()
    if new_data_filename:
        fupload.file_upload([new_data_filename])
    else:
        fupload.file_upload()

    price_comparison = {}

    with open("/tmp/price-comparison-recent.json", "rb") as fp:
        price_comparison = json.load(fp)

    #if any price comparisons have changed (as noted in their data) then we'll tweet the product and how it changed.

    if price_comparison:
        for product, info in price_comparison.iteritems():
            short_url_obtained = False

            try:
                shortener = Shortener('Google', api_key = keys["GOOGLE_URL_SHORTENER_KEY"])
                short_url = shortener.short(info["product_url"])
                short_url_obtained = True
            except(requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                time.sleep(2)
                if not short_url_obtained:
                    short_url = config["fallback_short_url"]

            if info["is_discontinued_product"] and (info["old_price"] not in "N/A"):
                #only tweet out if the old_price of a product is N/A.
                #deals with issue of the discontinued product not getting removed
                #from scraped site.
                twitter.update_status(status=tweets["discontinued"] % {
                    "product": product, "url": short_url})
            elif info["is_new_product"]:
                twitter.update_status(status=tweets["new_product"] % {
                    "product": product, "price": int(info["new_price"]), "url": short_url})
            elif info["is_difference"]:
                twitter.update_status(status=tweets["price_change"] % {
                    "product": product, "price": int(info["new_price"]),
                    "was": int(info["old_price"]), "url": short_url})
            else:
                print("no change for %s" % product)
