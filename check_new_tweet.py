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
        
        if "参戦ID" in tweet["text"]:
            
            txt = tweetData[3] + " " + tweetData[4]
            
            # Replyを送信する
            # url = "https://api.twitter.com/1.1/statuses/update.json"
            # params = {
            #     'status': "@" + config.SCREEN_NAME + "\n" + txt,
            # }
            # res = twitter_oauth.twitter.post(url, params=params)
            
            # DMを送信する
            url = 'https://api.twitter.com/1.1/direct_messages/events/new.json'
            headers = {'content-type': 'application/json'}
            params = {
                "event":{
                    "type": "message_create",
                    "message_create": {
                        "target": {
                            "recipient_id": config.USER_ID
                        },
                        "message_data": {
                            "text": "[グラブル救援]\n" + txt
                        }
                   }
                }
            }
            params = json.dumps(params)
            
            res = twitter_oauth.twitter.post(url, headers=headers, data=params)
            
            if res.status_code == 200: 
                
                if "参戦ID" in tweet["text"]:
                    
                    url = "https://api.twitter.com/1.1/statuses/destroy.json"
                    params = {
                        'id': tweet['id']
                    }
                    # 一時的にコメントアウト
                    # res = twitter_oauth.twitter.post(url, params=params)

