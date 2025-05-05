import scrapy
import os

class URLSpider(scrapy.Spider):

    name = "url"

    def __init__(self, max_depth=1, num_pages=10000, seed_file="seeds.txt", *args, **kwargs):
        super(URLSpider, self).__init__(*args, **kwargs)
        self.max_depth = int(max_depth)
        self.max_pages = int(num_pages)
        self.n_pages = 0
        self.n_seen = 0


        # Check if the seed file exists        
        self.start_urls = []

        # Load the seed URLs from the specified file
        # If the file is not found, use a default seed URL
        try:
            with open(seed_file, 'r') as f:
                self.start_urls = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            if seed_file == "seeds.txt":
                self.logger.warning(f"Default seed file 'seeds.txt' not found. Using fallback URL.")
                
                # If the seed file is not found, use a default URL
                # This is the default URL for testing purposes
                self.start_urls = ['http://quotes.toscrape.com']
            else:
                raise FileNotFoundError(f"Seed file '{seed_file}' not found.")

    def parse(self, response):

        # Tracks the number of URLs the spider has seen
        self.n_seen += 1
        self.log(f"Seen {self.n_seen}")
        
        # Stop the spider if the maximum pages have been reached
        if self.n_pages >= self.max_pages:
            self.crawler.engine.close_spider(self, reason="Page limit reached")

        # Get current depth
        depth = response.meta.get('depth', 0)
        
        # Creates the folder if doesn't already exist
        output_dir = 'crawled_pages'
        os.makedirs(output_dir, exist_ok=True)

        # Sets the output filename to be the webpage's title
        # Probably should make the title unique in some way
        title = response.css('title::text')[0].extract().replace(" ","")
        filename = os.path.join(output_dir, f"{title}.html")

        # Write to file
        with open(filename, 'wb') as file:
            file.write(response.body)
        self.log(f"Saved file {filename} (depth {depth}, num {self.n_pages})") # Log to show depth + filename
        self.n_pages += 1

        # Expand if depth limit hasn't been reached
        if depth < self.max_depth:
            # Otherwise get links and follow them, incrimenting depth
            for link in response.css('a::attr(href)').getall():
                yield response.follow(link, callback=self.parse, meta={'depth': depth+1})