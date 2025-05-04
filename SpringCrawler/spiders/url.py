import scrapy
import os

class URLSpider(scrapy.Spider):

    name = "url"
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        
        # Creates the folder if doesn't already exist
        output_dir = 'crawled_pages'
        os.makedirs(output_dir, exist_ok=True)

        # Sets the output filename to be the webpage's title
        title = response.css('title::text')[0].extract().replace(" ","")
        filename = os.path.join(output_dir, f"{title}.html")

        # Write to file
        with open(filename, 'wb') as file:
            file.write(response.body)

        # List of links to visit next
        links = response.css('a::attr(href)')