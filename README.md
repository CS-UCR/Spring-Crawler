# Spring-Crawler
CS172 Spring 2025 Group 22

### Instructions
Run Requirements:
Python
Pip
(Optional) Create a virtual environment
Create virtual environment 
Windows: python -m venv venv	
Linux/MacOs: python3 -m venv venv
Activate virtual environment 
Windows: call venv\Scripts\activate.bat	
Linux/MacOs: source venv/bin/activate 
Install dependencies:  
pip install --upgrade pip 	pip install -r requirements.txt


For Mac/Linux Platforms
Navigate to the Spring-Crawler directory.
Make sure the file has permission to run. 
Run chmod +x crawler.sh in the terminal
Now run the program.
./crawler.sh <seed-file> <num-pages> <depth> <output-dir>
For Windows Platforms
Navigate to the Spring-Crawler directory.
Run the program.
.\crawler.sh <seed-file> <num-pages> <depth> <output-dir>





### System Architecture
Our web crawler is built with a Python Scrapy framework to crawl HTML pages from a starting seed and collect raw data. The main component in the architecture of our system is the spider (url.py), where the crawling strategy is defined. Specifically, the spider sets up the crawler and controls how the spider will search through the web, collect data, look for duplicates and save the pages based on the given parameters. These parameters include the seed file, number of pages, maximum depth, and output directory. 
Additionally, the deduplication module in our system is responsible for detecting duplicate pages to prevent the crawler from saving the same pages. For this, the deduplication module uses the simhashing technique to ensure that the crawler collects different and meaningful pages from the set of websites that they crawl. Overall, this part of the system helps to make the crawler more effective and efficient.
Finally, we have our executables for both Windows and Linux that provide a user-friendly interface to run the crawler. The user is able to specify their own parameters, where the seed file and number of pages parameters are required while the depth and output directory parameters are optional. Before launching the crawler, however, the venv is activated and requirements.txt is installed to set up the environment (in case they are missing). Based on the parameters given by the user, the file runs the command to start the crawler.

