from bs4 import BeautifulSoup
import lucene
import os
import json
lucene.initVM()
from java.nio.file import Paths
from org.apache.lucene.store import FSDirectory
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.document import Document, Field, StringField, TextField

# Helper function to parse the html file into text
def parse_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    title = soup.title.string if soup.title else ''
    body = soup.get_text(separator=' ', strip=True)
    
    return title, body

# Initialize lucene index
index_dir = "lucene_index"
store = FSDirectory.open(Paths.get(index_dir))
analyzer = StandardAnalyzer()
config = IndexWriterConfig(analyzer)
writer = IndexWriter(store, config)

# Local variables
html_dir = 'newcrawl'
simhash_map = {}
n = 0
nbad = 0

# Read in the JSON file of URLs
with open('hashmap.json', 'r') as file:
    simhash_map = json.load(file)

# Create a document with the file and add to the collection
for filename in os.listdir(html_dir):
    if filename.endswith('.html'):
        try:
            title, body = parse_html_file(os.path.join(html_dir, filename))
            doc = Document()
            doc.add(StringField("filename", filename, Field.Store.YES))
            doc.add(StringField("url", simhash_map[filename[0:len(filename)-5]], Field.Store.YES))
            doc.add(TextField("title", title, Field.Store.YES))
            doc.add(TextField("body", body, Field.Store.YES))
            # Maybe we want to find, parse, and save tags?
            writer.addDocument(doc)
        except Exception as e:
            print(f"Error: {e}")
            print(f"filename:  {filename}")
            nbad += 1
        finally:
            n += 1
            if n % 100 == 0:
                print(f"bad: {nbad}, tot: {n}")

print(f"Index built. Rejected {nbad} files out of {n} ({100*nbad/n}%)")

writer.commit()
writer.close()