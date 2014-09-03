#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
import sqlite3
import tweepy

request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'
authenticate_url = 'https://api.twitter.com/oauth/authorize'

consumer_key = ''
consumer_secret = ''

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)

try:
    auth_url = auth.get_authorization_url()
except tweepy.TweepError:
    print("ERROR! FAILED TO GET REQUEST TOKEN")
#request_tokenのkeyとsecretを取得
os.chdir('cgi-bin/')
con = sqlite3.connect('oauth.db')
con.execute(u'insert into oauth values (?,?)',(auth.request_token.key,auth.request_token.secret))
con.commit()
con.close()

#認証ページの提示
print "Content-type: text/html; charset: utf-8"
print
print '<html><head><meta charset="UTF-8"></head><body><a href="%s">あかんカウンター</a><p>%s</p></body></html>' % (auth_url,os.getcwd())