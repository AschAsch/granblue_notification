# coding: UTF-8
import json
import config
import twitter_oauth
import csv
import datetime
import time

def check_tweet():

    
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    params = {
        "user_id": config.USER_ID,
        "since_id": "1208643212375539712" # 基準となるTWEET_ID
    }
    
    twitter_oauth.setPrivate()
    res = twitter_oauth.twitter.get(url, params=params)
    
    if res.status_code == 200:
        
        # csvデータの読み込み
        dataId = []
        with open('tweet.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                dataId.append(str(row[1]))
    
        timeline = json.loads(res.text)
        
        for tweet in timeline:
            
            tweetData = tweet["text"].split()
            
            if "参戦ID" in tweet["text"] and not tweetData[0] in dataId:
                
                tweetStatus = tweetData[0] + tweetData[1] + "\n" + tweetData[3] + " " + tweetData[4]
                
                # 新しい救援ツイートデータをcsvへ書き込む
                with open('tweet.csv', 'a') as f:
                    writer = csv.writer(f)
                    tweetTimeUnix = str(time.time()).split(".")
                    tweetData.insert(0, tweetTimeUnix[0])
                    writer.writerows([tweetData])
                    print(tweetData)
                
                
                # Replyを送信する（希望によりコメントアウト中）
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
                                "recipient_id": config.SEND_USER_ID
                            },
                            "message_data": {
                                "text": "[グラブル救援]\n" + tweetStatus
                            }
                       }
                    }
                }
                params = json.dumps(params)
                
                twitter_oauth.setPrivate()
                res = twitter_oauth.twitter.post(url, headers=headers, data=params)
                
                if res.status_code == 200: 
                    url = "https://api.twitter.com/1.1/statuses/destroy.json"
                    params = {
                        'id': tweet['id']
                    }
                    # 上記通知処理が完了したら元のツイートを削除する
                    twitter_oauth.setPrivate()
                    res = twitter_oauth.twitter.post(url, params=params)
                    if not res.status_code == 200:
                        print("delete error. status_code => " + str(res.status_code))
        
        
        
        
        csvData = []
        
        with open('tweet.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                elapsedSec = int(time.time()) - int(row[0])
                if (7 * 60) < elapsedSec: # 時間経過しているかチェックする(7分)
                
                    tweetStatus = row[1] + row[2] + "\n" + row[3] + "\n" + row[4] + " " + row[5] + "\n" + row[6]
                    
                    url = "https://api.twitter.com/1.1/statuses/update.json"
                    params = {
                        'status': tweetStatus,
                    }
                    
                    # 公開アカウントへPOSTする
                    twitter_oauth.setPublic()
                    res = twitter_oauth.twitter.post(url, params=params)
                    if not res.status_code == 200:
                        csvData.append(row)
                else:
                    csvData.append(row)

        # csvデータを書き込む
        with open('tweet.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(csvData)
