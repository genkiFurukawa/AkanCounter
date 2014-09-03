#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import cgi
import urlparse
import tweepy
import os
import sqlite3

request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'
authenticate_url = 'https://api.twitter.com/oauth/authorize'

consumer_key = ''
consumer_secret = ''

print "Content-type: text/html; charset: utf-8"
print
print '<html><head><meta charset="UTF-8"></head><body>'

#auth_tokenとauth_verifierを取得
if 'QUERY_STRING' in os.environ:
    query = urlparse.parse_qs(os.environ['QUERY_STRING'])
else:
    query = {}

print '<p>%s</p><br>' % query
print '<p>%s</p><br>' % os.getcwd()
#auth_token_secretを取得
os.chdir('cgi-bin/')
con = sqlite3.connect('oauth.db')
auth_token_secret = con.execute(u'select secret from oauth where key = ?', [query['oauth_token'][0]]).fetchone()[0]
con.close()

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_request_token(query['oauth_token'][0],auth_token_secret)

try:
    auth.get_access_token(query['oauth_verifier'][0])
except tweepy.TweepError:
    print('Error! Failed to get access token.')

auth.set_access_token(auth.access_token.key,auth.access_token.secret)
api = tweepy.API(auth_handler = auth)

TL = api.home_timeline(count=200)

for tweet in TL:
    print '<p>%s</p>' % tweet.text

print '</body></html>'