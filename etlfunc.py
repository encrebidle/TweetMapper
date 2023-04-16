

def tweetretreive(sword,fdate):
    
    import os
    import tweepy as tw
    import pandas as pd
    from tqdm import tqdm, notebook

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.width', None)
    api_key = "eDTNvP8goTAxpQpcCmYqNUMfS"
    api_secret ="iSfLYffRBJYzV3FfMu6EmPtxRxazjfLAZXHxEPf0w9OgZ4W6SV"
    access_key ="821033293688737792-rfY8oUypzHcDy7WVe4wIT0wQSm7mdXX"
    access_secret="U2z3ede3BW24fxIABI0NbQtO0K6zZomIizM58g3Rmm7Ty"
    #insert into tweetcon values("eDTNvP8goTAxpQpcCmYqNUMfS","iSfLYffRBJYzV3FfMu6EmPtxRxazjfLAZXHxEPf0w9OgZ4W6SV","821033293688737792-rfY8oUypzHcDy7WVe4wIT0wQSm7mdXX","U2z3ede3BW24fxIABI0NbQtO0K6zZomIizM58g3Rmm7Ty");
    auth = tw.OAuthHandler(api_key,api_secret)
    auth.set_access_token(access_key,access_secret)
    
    #auth = tw.OAuthHandler(api_key, api_secret)
    
    api = tw.API(auth, wait_on_rate_limit=True)
    
    tweets = tw.Cursor(api.search_tweets,q=sword,lang="en",since=fdate).items(10)
    
    tweets_copy = []
    
    for tweet in tqdm(tweets):
         tweets_copy.append(tweet)
    
    tweets_df = pd.DataFrame()
    for tweet in tqdm(tweets_copy):
        hashtags = []
        try:
            for hashtag in tweet.entities["hashtags"]:
                hashtags.append(hashtag["text"])
            text = api.get_status(id=tweet.id, tweet_mode='extended').full_text
        except:
            pass
        tweets_df = tweets_df.append(pd.DataFrame({'user_name': tweet.user.name, 
                                                   'user_location': tweet.user.location,\
                                                   'user_description': tweet.user.description,
                                                   'user_created': tweet.user.created_at,
                                                   'user_followers': tweet.user.followers_count,
                                                   'user_friends': tweet.user.friends_count,
                                                   'user_favourites': tweet.user.favourites_count,
                                                   'user_verified': tweet.user.verified,
                                                   'date': tweet.created_at,
                                                   'text': text, 
                                                   'hashtags': [hashtags if hashtags else None],
                                                   'source': tweet.source,
                                                   'is_retweet': tweet.retweeted}, index=[0]))
    
    #Read past fetched data if exists
    #tweets_old_df = pd.read_csv("covid19_tweets.csv")
    #Merge both old and new data
    #tweets_all_df = pd.concat([tweets_old_df, tweets_df], axis=0)
    #Removing duplicates if exists
    #tweets_all_df.drop_duplicates(subset = ["user_name", "date", "text"], inplace=True)
    #exporting data to update csv
    #tweets_all_df.to_csv("covid19_tweets.csv", index=False)
    name= sword[1:-16]
    #Read past fetched data if exists
    #tweets_old_df = pd.read_csv("covid19_tweets.csv")
    #Merge both old and new data
    #tweets_all_df = pd.concat([tweets_old_df, tweets_df], axis=0)
    #Removing duplicates if exists
    #tweets_all_df.drop_duplicates(subset = ["user_name", "date", "text"], inplace=True)
    #exporting data to update csv
    tweets_df.to_csv(name +"_tweets.csv", index=False)
    
    return tweets_df
            
