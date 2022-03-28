import json
import pandas as pd
from glob import glob

preserve_fields = ["created_at", "reply_settings", "lang", "possibly_sensitive", "text"]

quoted_tweet = "https://quoted.com123456abcdefg"
image_tweet = "https://image.com123456abcdefg"
external = "https://externallink.com123456abcdefg"
mnt = "@mentionedmentioned"


def process_individual_tweet(tweet):
    new_tweet = {pf: tweet[pf] for pf in preserve_fields}

    public_metrics = tweet["public_metrics"]

    for metric, value in public_metrics.items():
        new_tweet[metric] = value

    referenced_tweets = tweet.get("referenced_tweets", [])
    new_tweet["referenced_tweets"] = len(referenced_tweets)

    quotes = set(rt["id"] for rt in referenced_tweets if rt["type"] == "quoted")
    new_tweet["quotes_tweet"] = len(quotes) > 0

    replied_to = set(rt["id"] for rt in referenced_tweets if rt["type"] == "replied_to")
    new_tweet["is_reply"] = len(replied_to) > 0

    entities = tweet.get("entities", {})
    new_tweet["entities"] = len(entities)
    text = new_tweet["text"]
    for kind, ents in entities.items():
        new_tweet[f"has_{kind}"] = True
        if kind == "urls":
            for url in ents:
                start = url["start"]
                end = url["end"]
                entity_length = end - start
                expanded_url = url["expanded_url"]

                if expanded_url.split("/")[-1] in quotes:
                    replacement = quoted_tweet
                elif expanded_url.startswith("https://twitter.com"):
                    replacement = image_tweet
                else:
                    replacement = external

                text = text[:start] + replacement[:entity_length] + text[end:]
        elif kind == "mentions":
            for mention in ents:
                start = mention["start"]
                end = mention["end"]
                entity_length = end - start
                text = text[:start] + str(mnt[:entity_length]) + text[end:]

    new_tweet["text"] = text
    return new_tweet


def process_line(tweets):
    return [process_individual_tweet(tweet) for tweet in tweets]


new_tweets = []
for file in glob("dataset/tweets/*-tweets.jsonl"):
    with open(file) as readable:
        for txt_line in readable:
            line = json.loads(txt_line)
            new_tweets.extend(process_line(line["data"]))

dataframe = pd.DataFrame(new_tweets)
dataframe.sample(frac=1).to_csv("tech-twitter.csv", encoding="utf8", index=False)
