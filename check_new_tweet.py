# coding: UTF-8
import json
import config
import twitter_oauth
import csv
import datetime
import time
import calendar

def check_tweet():

    
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    params = {
        "user_id": config.USER_ID,
    }
    
    twitter_oauth.setPrivate()
    res = twitter_oauth.twitter.get(url, params=params)
    
    if res.status_code == 200:
        
        timeline = json.loads(res.text)

        
        for tweet in timeline:

            if tweet["text"].startswith("団"):
                # 団のみに通知を行う

                # tweetのunixTimeを取得する
                time_utc = time.strptime(tweet["created_at"], '%a %b %d %H:%M:%S +0000 %Y')
                tweet_time = calendar.timegm(time_utc)

                # 7分前のunixTimeを取得する
                now_time = int(time.time()) - (60 * 70)

                # 指定時間が経過しているかチェックする
                if 0 < (tweet_time - now_time):
                    

                    # 過去に通知処理を行っているか確認する
                    if tweet["favorited"]:
                        print(str(tweet['id']) + ' is pass.')
                        pass
                    else:
                        # 通知処理を行う
                        post_notification(tweet)


                else:
                    # 指定時間が経過している場合、公開アカウントへツイートを行う
                    post_global(tweet)
            else:
                # 公開アカウントへツイートを行う
                post_global(tweet)



# 団員への通知を行う
def post_notification(tweet):

    # DMを送信する

    tweetData = tweet["text"].split()

    url = 'https://api.twitter.com/1.1/direct_messages/events/new.json'
    headers = {'content-type': 'application/json'}
    params = {
        "event":{
            "type": "message_create",
            "message_create": {
                "target": {
                    "recipient_id": config.SEND_USER_ID
                },
                "message_data": {
                    "text": "[グラブル救援]\n" + tweetData[5]
                }
           }
        }
    }
    params = json.dumps(params)
    
    twitter_oauth.setPrivate()
    res = twitter_oauth.twitter.post(url, headers=headers, data=params)
    
    if not res.status_code == 200:
        print("direct_messages/events/new error. status_code => " + str(res.status_code))

    
    url = "https://api.twitter.com/1.1/favorites/create.json"
    params = {
        'id': tweet['id']
    }

    # 通知処理が成功した場合、該当tweetにfavoriteをcreateする
    twitter_oauth.setPrivate()
    res = twitter_oauth.twitter.post(url, params=params)
    if not res.status_code == 200:
        print("favorites/create error. status_code => " + str(res.status_code))



# 公開アカウントへツイートを行う
def post_global(tweet):

    url = "https://api.twitter.com/1.1/statuses/update.json"
    params = {
        'status': tweet["text"],
    }
    
    # 公開アカウントへPOSTする
    twitter_oauth.setPublic()
    res = twitter_oauth.twitter.post(url, params=params)

    if res.status_code == 200:

        url = "https://api.twitter.com/1.1/statuses/destroy.json"
        params = {
            'id': tweet['id']
        }

        # 上記通知処理が完了したら元のツイートを削除する
        twitter_oauth.setPrivate()
        res = twitter_oauth.twitter.post(url, params=params)
        if not res.status_code == 200:
            print("statuses/destroy error. status_code => " + str(res.status_code))
    else:
        print("statuses/update error. status_code => " + str(res.status_code))

check_tweet()

