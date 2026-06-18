import json

# Loads the user's configuration. Copy config.example.json to config.json and
# fill in your own values (target site, product URLs, Twitter keys, S3 bucket).


def load_config():
    with open("config.json") as fp:
        return json.load(fp)
