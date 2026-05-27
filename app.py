from flask import Flask, request, jsonify
from scraper import scrape_pages

app = Flask(__name__)


@app.route("/scrape", methods=["POST"])
def scrape():
    body = request.get_json(silent=True) or {}
    urls = body.get("urls", [])
    custom_selectors = body.get("selectors")  # optional override

    if not urls or not isinstance(urls, list):
        return jsonify({"error": "'urls' must be a non-empty list"}), 400

    results = scrape_pages(urls, custom_selectors)
    return jsonify({"count": len(results), "results": results})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
