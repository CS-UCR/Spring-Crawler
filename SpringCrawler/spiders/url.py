import scrapy
import os
from SpringCrawler.deduplication import is_duplicate as dd

class URLSpider(scrapy.Spider):

    name = "url"
    start_urls = []
    simhash_table = {}
    

    def __init__(self, max_depth=4, num_pages=100000, seed_file="seeds.txt", output_dir="newcrawl",*args, **kwargs):
        super(URLSpider, self).__init__(*args, **kwargs)
        self.max_depth = int(max_depth)
        self.max_pages = int(num_pages)
        self.n_pages = 0
        self.n_seen = 0
        self.n_skip = 0
        self.output_dir = os.path.abspath(output_dir)
        self.seed_file = os.path.abspath(seed_file)
        # Creates the folder if doesn't already exist
        os.makedirs(self.output_dir, exist_ok=True)

        # Load the seed URLs from the specified file
        # If the file is not found, use a default seed URL
        try:
            with open(self.seed_file, 'r') as f:
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
        self.log(f"Seen {self.n_seen} pages so far.")

        # Checks if the page is a near-duplicate
        if dd.is_duplicate(response.body):
            self.log(f"Skipped duplicate page: {response.url}")
            self.n_skip += 1
            return

        # Stop the spider if the maximum pages have been reached
        if self.n_pages >= self.max_pages:
            self.crawler.engine.close_spider(self, reason="Page limit reached")
            return

        # Get current depth
        depth = response.meta.get('depth', 0)

        # Sets the output filename to be the webpage's simhash
        doc_simhash = dd.comput_simhash(dd.get_text_from_html(response.body))
        filename = os.path.join(self.output_dir, f"{doc_simhash.value}.html")

        # Maps the simhash to the url
        if doc_simhash.value in self.simhash_table:
            self.logger.warning(f"Simhash collision detected for {doc_simhash.value}")
        self.simhash_table[doc_simhash.value] = response.url

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

    def closed(self, reason):
        self.log(f"Spider closed: {reason}")
        self.log(f"Total pages visited: {self.n_seen}")
        self.log(f"Near duplicates skipped: {self.n_skip}")
        self.log(f"Files saved: {self.n_pages}")
        # Build hashmap.json
        json_obj = json.dumps(self.simhash_table, indent=4)
        with open('hashmap.json','w') as file:
            file.write(json_obj)