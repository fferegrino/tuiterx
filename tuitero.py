from transformers import pipeline
import tweepy
import os
import sys
import random

client = tweepy.Client(
    consumer_key=os.environ["CONSUMER_KEY"],
    consumer_secret=os.environ["CONSUMER_SECRET"],
    access_token=os.environ["ACCESS_TOKEN"],
    access_token_secret=os.environ["ACCESS_TOKEN_SECRET"]
)


tuitero = pipeline('text-generation',model='./tuitero', tokenizer='DeepESP/gpt2-spanish')

prompts = [ 
    line.strip() for line in 
    open("prompts.txt").readlines()
]

prompts = random.choices(prompts, k=15)

gen = tuitero(prompts, clean_up_tokenization_spaces=True)
texts = [text[0]["generated_text"] for text in gen]

tweet = random.choice(texts)

client.create_tweet(text=tweet)
