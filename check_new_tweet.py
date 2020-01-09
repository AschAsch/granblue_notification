# coding: UTF-8
import json
import config
import twitter_oauth
import csv
import datetime
import time
import calendar

def check_tweet():

    users = json.loads(config.TOKENS)

    for user in users['users']:

        url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        params = {
            "user_id": user['rescue_user_id'],
        }
        twitter_oauth.setToken(user['access_token'], user['access_token_secret'])

        res = twitter_oauth.twitter.get(url, params=params)

        if res.status_code == 200:
            print("statuses/user_timeline success. status_code => " + str(res.status_code))

            timeline = json.loads(res.text)

            for tweet in timeline:

                posted = False

                if tweet["text"].startswith("だん"):
                    # tweetのunixTimeを取得する
                    time_utc = time.strptime(tweet["created_at"], '%a %b %d %H:%M:%S +0000 %Y')
                    tweet_time = calendar.timegm(time_utc)

                    # 7分前のunixTimeを取得する
                    now_time = int(time.time()) - (60 * 7)

                    # 指定時間が経過しているかチェックする
                    if 0 < (tweet_time - now_time):

                        # 過去に通知処理を行っているか確認する
                        if tweet["favorited"]:
                            print(str(tweet['id']) + ' is pass.')
                            pass
                        else:
                            # 通知処理を行う
                            post_notification(tweet, user)
                            pass

                    else:
                        # 指定時間が経過している場合、公開アカウントへツイートを行う
                        posted = post_global(tweet)
                        pass
                else:
                    # 公開アカウントへツイートを行う
                    posted = post_global(tweet)
                    pass

                # 上記通知処理が完了したら元のツイートを削除する
                if posted:
                    url = "https://api.twitter.com/1.1/statuses/destroy.json"
                    params = {
                        'id': tweet['id']
                    }

                    twitter_oauth.setToken(user['access_token'], user['access_token_secret'])
                    res = twitter_oauth.twitter.post(url, params=params)

                    if res.status_code == 200:
                        print("statuses/destroy success. status_code => " + str(res.status_code))
                    else:
                        print("statuses/destroy error. status_code => " + str(res.status_code))
        else:
            print("statuses/user_timeline error. status_code => " + str(res.status_code))
    

# 団員への通知を行う
def post_notification(tweet, user):

    # DMを送信する

    tweetData = tweet["text"].split()

    url = 'https://api.twitter.com/1.1/direct_messages/events/new.json'
    headers = {'content-type': 'application/json'}
    params = {
        "event":{
            "type": "message_create",
            "message_create": {
                "target": {
                    "recipient_id": user['user_id']
                },
                "message_data": {
                    "text": "[グラブル救援]\n" + tweetData[5]
                }
           }
        }
    }
    params = json.dumps(params)
    
    twitter_oauth.setToken(user['access_token'], user['access_token_secret'])
    res = twitter_oauth.twitter.post(url, headers=headers, data=params)
    
    if res.status_code == 200:
        print("direct_messages/events/new success. status_code => " + str(res.status_code))
        pass
    else:
        print("direct_messages/events/new error. status_code => " + str(res.status_code))
        return False


    # 通知処理が成功した場合、該当tweetにfavoriteをcreateする
    
    url = "https://api.twitter.com/1.1/favorites/create.json"
    params = {
        'id': tweet['id']
    }

    res = twitter_oauth.twitter.post(url, params=params)
    if res.status_code == 200:
        print("favorites/create success. status_code => " + str(res.status_code))
    else:
        print("favorites/create error. status_code => " + str(res.status_code))



# 公開アカウントへツイートを行う
def post_global(tweet):

    url = "https://api.twitter.com/1.1/statuses/update.json"
    status = ""
    if tweet["text"].startswith("だん"):
        status = tweet["text"].split(" ", 1)
        status = status[1]
    else:
        if tweet["favorited"]:
            return False
        else:
            if "参戦ID" in tweet["text"]:
                status = tweet["text"]
            else:
                return False

    params = {
        'status': status,
    } 
    
    # POSTする
    twitter_oauth.setPublic()
    res = twitter_oauth.twitter.post(url, params=params)

    if res.status_code == 200:
        print("statuses/update success. status_code => " + str(res.status_code))
        return True
    else:
        print("statuses/update error. status_code => " + str(res.status_code))
        return False

    url = "https://api.twitter.com/1.1/statuses/destroy.json"
    params = {
        'id': tweet['id']
    }

def lambda_handler(event, context):
    check_tweet()