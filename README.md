# Petlebi Product Scraper

This project is a web scraper built with Scrapy to scrape product information from the Petlebi website. It handles lazy loading using Scrapy-Splash to render JavaScript and extract all necessary product details.

## Requirements

- Python 3.x
- Scrapy
- Scrapy-Splash
- Docker (for running Splash)

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/petlebi-scraper.git
    cd petlebi-scraper
    ```

2. **Create a virtual environment and activate it (optional but recommended):**
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install the required packages:**
    ```bash
    pip install scrapy scrapy-splash
    ```

4. **Run Splash using Docker:**
    ```bash
    docker run -p 8050:8050 scrapinghub/splash
    ```

## Configuration

Add the following settings to your Scrapy project's `settings.py` file to configure Scrapy-Splash:

```python
SPLASH_URL = 'http://localhost:8050'

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
```

## Usage

1. **Navigate to the project directory:**
    ```bash
    cd petlebi-scraper
    ```

2. **Run the Scrapy spider:**
    ```bash
    scrapy crawl product_spider
    ```

3. **Output:**
    The scraped data will be saved in `petlebi_products.json`.

## Project Structure

- `product_spider.py`: Contains the Scrapy spider to scrape product data.
- `settings.py`: Scrapy settings for the project, including Scrapy-Splash configuration.
- `petlebi_products.json`: Output file where the scraped data is saved.

## Spider Explanation

- `start_requests()`: Initiates requests to the start URLs using Splash to handle JavaScript rendering.
- `parse()`: Extracts product links and follows them to scrape individual product pages. It also handles pagination if more products are loaded dynamically.
- `parse_product()`: Extracts product information from the JSON-LD structured data found in the product pages.
- `extract_product_info()`: Processes the JSON data to extract relevant product information.
- `closed()`: Writes the collected product information to a JSON file when the spider finishes running.



## Acknowledgments

- [Scrapy](https://scrapy.org/)
- [Scrapy-Splash](https://github.com/scrapy-plugins/scrapy-splash)
- [Petlebi](https://www.petlebi.com/)
