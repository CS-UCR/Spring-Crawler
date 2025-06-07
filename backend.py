from flask import Flask, request, render_template
import lucene
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser, QueryParserBase
from org.apache.lucene.search import IndexSearcher, CustomScoreQuery, FunctionScoreQuery
from org.apache.lucene.store import FSDirectory  # Standardized to FSDirectory
from org.apache.lucene.expressions.js import JavascriptCompiler
from org.apache.lucene.expressions import Expression
from org.apache.lucene.search import Sort, SortField

app = Flask(__name__)

lucene.initVM()
INDEX_DIR = "lucene_index"  # path to match build_index.py
directory = FSDirectory.open(Paths.get(INDEX_DIR))
searcher = IndexSearcher(DirectoryReader.open(directory))
analyzer = StandardAnalyzer()

@app.route('/', methods=['GET', 'POST'])
def search():
    query_text = ''
    results = []

    if request.method == 'POST':
        query_text = request.form.get('query', '').strip()
        if query_text:
            try:
                # Parse query with error handling for invalid syntax
                query = QueryParser("body", analyzer).parse(QueryParserBase.escape(query_text))

                hits = searcher.search(query, 10).scoreDocs

                for hit in hits:
                    doc = searcher.doc(hit.doc)
                    results.append({
                        'title': doc.get("title"),
                        'score': f"{hit.score:.2f}",
                        'url': doc.get("url"),
                        'snippet': doc.get("body")[:200] + "..."  #snippet
                    })
            except Exception as e:
                print(f"Search error: {e}")
                results = None  # Signal error to template

    return render_template('index.html', query=query_text, results=results)

if __name__ == '__main__':
    app.run(debug=True)