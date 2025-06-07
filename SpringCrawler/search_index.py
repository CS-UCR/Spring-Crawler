import lucene
lucene.initVM()


from java.nio.file import Paths
from java.lang import String

from org.apache.lucene.store import FSDirectory
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.queryparser.classic import QueryParser

# Open index
index_dir = "lucene_index/"
directory = FSDirectory.open(Paths.get(index_dir))
reader = DirectoryReader.open(directory)
searcher = IndexSearcher(reader)

# Set up analyzer and parser for a single field (e.g., "body")
analyzer = StandardAnalyzer()
parser = QueryParser("body", analyzer)

# Parse the query string
query = parser.parse(String.valueOf("climate change"))

# Search top 10 results
top_docs = searcher.search(query, 10)

# Print results
for score_doc in top_docs.scoreDocs:
    doc = searcher.doc(score_doc.doc)
    print(f"Score: {score_doc.score}")
    print(f"Title: {doc.get('title')}")
    print(f"Body snippet: {doc.get('body')[:200]}")
    print("---")