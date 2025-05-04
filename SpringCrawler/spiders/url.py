import scrapy
import os

class URLSpider(scrapy.Spider):

    name = "url"
    start_urls = ['http://quotes.toscrape.com']

    def __init__(self, max_depth=1, *args, **kwargs):
        super(URLSpider, self).__init__(*args, **kwargs)
        self.max_depth = int(max_depth)

    def parse(self, response):

        # Get current depth
        depth = response.meta.get('depth', 0)
        
        # Creates the folder if doesn't already exist
        output_dir = 'crawled_pages'
        os.makedirs(output_dir, exist_ok=True)

        # Sets the output filename to be the webpage's title
        # TODO: Need unique names for webpages due to overwriting for duplicates.
        # Or need to prune duplicate pages (ie page 1 + page 2)
        title = response.css('title::text')[0].extract().replace(" ","")
        filename = os.path.join(output_dir, f"{title}.html")

        # Write to file
        with open(filename, 'wb') as file:
            file.write(response.body)
        self.log(f"Saved file {filename} (depth {depth})") # Log to show depth + filename

        # Break if depth is at or past max depth
        if depth >= self.max_depth:
            return

        # Otherwise get links and follow them, incrimenting depth
        for link in response.css('a::attr(href)').getall():
            yield response.follow(link, callback=self.parse, meta={'depth': depth+1})