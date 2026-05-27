from flask import Flask, request, jsonify
from scraper import scrape_pages
from logger import get_logger

app = Flask(__name__)
log = get_logger(__name__)


@app.route("/scrape", methods=["POST"])
def scrape():
    body = request.get_json(silent=True) or {}
    urls = body.get("urls", [])
    custom_selectors = body.get("selectors")  # optional override

    if not urls or not isinstance(urls, list):
        log.warning("Invalid request: 'urls' missing or not a list")
        return jsonify({"error": "'urls' must be a non-empty list"}), 400

    log.info("Scraping %d URL(s)", len(urls))
    results = scrape_pages(urls, custom_selectors)
    log.info("Scrape complete: %d result(s)", len(results))
    return jsonify({"count": len(results), "results": results})


@app.route("/health", methods=["GET"])
def health():
    log.info("Health check")
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
