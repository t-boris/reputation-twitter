# API_KEY = '0SR0dxBu7Viplr0DbEO8EBEGS'
# SECRET_KEY = '8RVCm37A81Jit8rkrNyHvN5h3FlDENAWi5gURKuzbEL1uvilWq'
# BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAIcuoQEAAAAA%2BJZb8IOMgmYBQXrHXldbHx3W2LE%3DMHgOFIOZoN9jeifDxtledJNKI9Fb7cfwLt5OGpguTY1pNzpzX7'
# ACCESS_TOKEN = '14929677-gZFFjmQcvSVtak42faNAZ05M9h1pDLGo06aL6mdMV'
# ACCESS_TOKEN_SECRET = 'E7we2lBZq9jR4So8ATcfZGuhda0v4t84f6z5Jh4KSCnDa'
import json

from searchtweets import ResultStream, gen_request_parameters, load_credentials

import sentiment

if __name__ == "__main__":

    # Load credentials from the .twitter_keys.yaml file
    premium_search_args = load_credentials(".twitter_keys.yaml", yaml_key="search_tweets_api", env_overwrite=False)

    # Define the search term and the date_since date
    search_words = "amway"
    date_since = "2023-06-15"

    # Generate the rule payload
    rule = gen_request_parameters(search_words,
                                  results_per_call=100,
                                  start_time=date_since,
                                  end_time="2023-06-21",
                                  tweet_fields="author_id,created_at,geo")

    # Collect tweets
    rs = ResultStream(request_parameters=rule, max_tweets=1000, max_results=1000, **premium_search_args)

    # Save tweets to a file
    counter = 0
    with open("amway-all-lang-simple.json", "a", encoding="utf-8") as file:
        results = list(rs.stream())
        for result in results:
            for tweet in result['data']:
                counter += 1
                print(f"{counter}: Processing tweet {tweet['id']}...\n")
                entry = {
                    'tweet_id': tweet['id'],
                    'username': tweet['author_id'],
                    'date': tweet['created_at'],
                    'text': tweet['text'],
                }
                entry = sentiment.analyze_sentiment(entry)  # add
                file.write(json.dumps(entry) + "\n")



    print("Tweets saved to 'tweets.txt'")
