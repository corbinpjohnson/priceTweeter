# priceTweeter

Tracks the price of a list of online product pages, detects changes since the last run, and tweets
the differences — price drops/increases, newly available items, and discontinued ones. Built to run
as an AWS Lambda function with state persisted in S3.

Point it at any store: you provide one sample product page to teach the scraper what a "product" and
"price" look like, then a list of product URLs to watch.

> **Status:** legacy (circa 2016). This is Python 2 and depends on services/APIs that have since
> changed (the old Twitter API, `scrapely`, the Google URL shortener). Kept for reference and as a
> starting point.

## How it works

1. **Scrape** — `main.py` trains [`scrapely`](https://github.com/scrapy/scrapely) on the sample page
   from your config, then scrapes each configured product URL and writes a timestamped price JSON.
2. **Compare** — it diffs the new prices against the most recent saved snapshot, flagging price
   changes, new products, and discontinued ones.
3. **Tweet** — `tweeter.py` (the Lambda handler) pulls state down from S3, runs the comparison,
   shortens product URLs, posts a tweet per change via [Twython](https://twython.readthedocs.io/)
   using your configurable templates, then uploads the updated state back to S3.

## Project layout

| File | Purpose |
| --- | --- |
| `tweeter.py` | AWS Lambda entry point — orchestrates download → compare → tweet → upload |
| `main.py` | Trains the scraper, scrapes the configured URLs, builds the comparison data |
| `config.py` | Loads `config.json` |
| `s3_file_download.py` / `s3_file_upload.py` | S3 state persistence helpers |
| `config.example.json` | Template configuration — copy to `config.json` |

## Configuration

Copy the example and fill in your own values:

```bash
cp config.example.json config.json
```

`config.json` holds everything site-specific:

- **`training`** — one sample product `url` and a `sample` of the `product`/`price` text on that page.
  This is how `scrapely` learns the layout of your target site.
- **`product_urls`** — the list of product pages to track.
- **`twitter`** — your Twitter API keys plus a URL-shortener key.
- **`s3`** — AWS credentials and the bucket used to persist state between runs.
- **`tweets`** — message templates for the discontinued / new-product / price-change cases.
  Available fields: `%(product)s`, `%(price)s`, `%(was)s`, `%(url)s`.
- **`fallback_short_url`** — used if URL shortening fails.

`config.json` is gitignored so you don't commit secrets.

## Requirements

```bash
pip install -r requirements.txt
```

Targets Python 2.7. Designed to run on AWS Lambda, with the two JSON state files
(`prices-recent.json`, `price-comparison-recent.json`) living in your S3 bucket.

## License

[MIT](LICENSE) © Corbin Johnson
