from flask import Flask, request, jsonify
from newspaper import Article
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin access (for Flutter to call this)

@app.route('/extract', methods=['POST'])
def extract():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        article = Article(url)
        article.download()
        article.parse()

        return jsonify({
            'title': article.title,
            'author': article.authors,
            'text': article.text,
            'image': article.top_image,
            'published': str(article.publish_date),
            'source': url.split('/')[2]  # just the domain
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
