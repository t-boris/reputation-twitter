import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

# Create a reference variable for Class TweetTokenizer
sia = SentimentIntensityAnalyzer()

# analyze the sentiment of a tweet and return json object with the tweet and sentiment
def analyze_sentiment(tweet):
    tweet['sentiment'] = sia.polarity_scores(tweet['text'])
    return tweet
