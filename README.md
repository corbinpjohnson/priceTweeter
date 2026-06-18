# priceTweeter

Watches product prices on [wholesalegaming.biz](http://www.wholesalegaming.biz) (Star Trek CCG
booster/starter boxes), detects changes since the last run, and tweets the differences. Built to
run as an AWS Lambda function with state stored in S3.

> **Status:** legacy (circa 2016). This is Python 2 and depends on services/APIs that have since
> changed (the old Twitter API, `scrapely`, `urllib2`). Kept for reference.

## How it works

1. **Scrape** — `main.py` trains [`scrapely`](https://github.com/scrapy/scrapely) on a sample page,
   then scrapes the configured product URLs and writes a timestamped price JSON.
2. **Compare** — it diffs the new prices against the most recent saved snapshot, flagging price
   changes, new products, and discontinued ones.
3. **Tweet** — `tweeter.py` (the Lambda handler) pulls state down from S3, runs the comparison,
   shortens product URLs, posts a tweet per change via [Twython](https://twython.readthedocs.io/),
   and uploads the updated state back to S3.

## Project layout

| File | Purpose |
| --- | --- |
| `main.py` | Scrapes prices and builds the comparison data |
| `product_extractor.py` | Regex-based extractor for product URLs/names |
| `tweeter.py` | AWS Lambda entry point — orchestrates download → compare → tweet → upload |
| `s3_file_download.py` / `s3_file_upload.py` | S3 state persistence helpers |

## Configuration

This project is hard-coded to use S3 for the JSON files it reads and writes. Before running you'll
need to provide:

- **AWS credentials + bucket** — set in the `__init__` of both `s3_file_*.py` files.
- **Twitter API keys** — a `twitter_keys.json` with `APP_KEY`, `APP_SECRET`, `OAUTH_TOKEN`,
  `OAUTH_TOKEN_SECRET`.

## License

[MIT](LICENSE) © Corbin Johnson
