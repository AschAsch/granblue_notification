# coding: UTF-8
import json
import config
import twitter_oauth


url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
params = {
    "user_id": config.USER_ID,
    "count": 1,
}

response = twitter_oauth.twitter.get(url, params=params)

if response.status_code == 200:

    timeline = json.loads(response.text)
    
    for tweet in timeline:
        
        tweetData = tweet["text"].split()
        
        if not tweetData[1].startswith('Lv'):
            
            url = "https://api.twitter.com/1.1/statuses/update.json"
            params = {
                'status': "@" + config.SCREEN_NAME + "\n" + tweetData[3] + " " + tweetData[4],
            }
            
            res = twitter_oauth.twitter.post(url, params=params)
            
            if res.status_code == 200: 
                
                if "参戦ID" in tweet["text"]:
                    
                    url = "https://api.twitter.com/1.1/statuses/destroy.json"
                    params = {
                        'id': tweet['id']
                    }
                    # 一時的にコメントアウト
                    # res = twitter_oauth.twitter.post(url, params=params)

