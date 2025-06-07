from flask import Flask, request, render_template
import lucene
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import SimpleFSDirectory

app = Flask(__name__)

lucene.initVM()
INDEX_DIR = "/mnt/data/lucene_index"
directory = SimpleFSDirectory(Paths.get(INDEX_DIR))
searcher = IndexSearcher(DirectoryReader.open(directory))
analyzer = StandardAnalyzer()

@app.route('/', methods=['GET', 'POST'])
def search():
    query_text = ''
    results = []

    if request.method == 'POST':
        query_text = request.form.get('query', '').strip()
        if query_text:
            query = QueryParser("body", analyzer).parse(query_text)
            hits = searcher.search(query, 10).scoreDocs

            for hit in hits:
                doc = searcher.doc(hit.doc)
                results.append({
                    'title': doc.get("title"),
                    'score': f"{hit.score:.2f}",
                    'path': doc.get("path")
                })

    return render_template('index.html', query=query_text, results=results)

if __name__ == '__main__':
    app.run(debug=True)
