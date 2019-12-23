# coding: UTF-8
import config
from requests_oauthlib import OAuth1Session

CK      = config.TWITTER_CONSUMER_KEY
CS      = config.TWITTER_CONSUMER_SECRET
twitter = None

# 鍵アカウント
def setPrivate():
    global twitter
    twitter = OAuth1Session(CK, CS, config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET) #認証処理

# 公開アカウント
def setPublic():
    global twitter
    twitter = OAuth1Session(CK, CS, config.PUBLIC_TWITTER_OAUTH_TOKEN, config.PUBLIC_TWITTER_OAUTH_TOKEN_SECRET) #認証処理
