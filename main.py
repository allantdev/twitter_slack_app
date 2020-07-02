#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Inital Code borrowed and modified from Twitter Dev Sample
# Modified by Allan Thompson as a Demo for Interviews
# https://developer.twitter.com/en/docs/labs/filtered-stream/quick-start
# It makes use of Twitter Labs Stream Filter to open a stream
# watch a user, then the pizza emoji tweets are sent via url to a Slack app via webhooks
# The Slack app channel must have the Twitter integration turned on, but not setup to watch that account

import os
import requests
import json
from time import sleep
import logging
import logging.handlers
from pprint import pprint
from requests.auth import AuthBase
from requests.auth import HTTPBasicAuth

# Environmental Variables Import Class
class EnvKeys(object):
    all_keys = os.environ
    client_key = all_keys.get("CLIENT_KEY")
    client_secret = all_keys.get("CLIENT_SECRET")
    slack_url = all_keys.get("SLACK_URL")
    rules_url = all_keys.get("RULES_URL")
    twitter_user = all_keys.get("TWITTER_USER")
    # Makes attribute is callable like a module
    def __init__(self, x):
        if x:
            self.x = x
        else:
            raise NameError(x)

# Gets a bearer token
class BearerTokenAuth(AuthBase):
  def __init__(self, consumer_key, consumer_secret):
    self.bearer_token_url = "https://api.twitter.com/oauth2/token"
    self.consumer_key = consumer_key
    self.consumer_secret = consumer_secret
    self.bearer_token = self.get_bearer_token()

  def get_bearer_token(self):
    response = requests.post(
      self.bearer_token_url, 
      auth=(self.consumer_key, self.consumer_secret),
      data={'grant_type': 'client_credentials'},
      headers={'User-Agent': 'TwitterDevFilteredStreamQuickStartPython'})

    if response.status_code != 200:
      raise Exception(f"Cannot get a Bearer token (HTTP %d): %s" % (response.status_code, response.text))

    body = response.json()
    return body['access_token']

  def __call__(self, r):
    r.headers['Authorization'] = f"Bearer %s" % self.bearer_token
    r.headers['User-Agent'] = 'TwitterDevFilteredStreamQuickStartPython'
    return r

# Send Notification to Slack
def notify_slack(text):    
    url = EnvKeys.slack_url
    payload = {"text": text}
    r = requests.post(url, data=json.dumps(payload))
    return(r.status_code)

def get_all_rules(rules_url, auth):
  
  response = requests.get(rules_url, auth=auth)

  if response.status_code != 200:
    raise Exception(f"Cannot get rules (HTTP %d): %s" % (response.status_code, response.text))

  return response.json()


def delete_all_rules(rules, rules_url, auth):
  if rules is None or 'data' not in rules:
    return None

  ids = list(map(lambda rule: rule['id'], rules['data']))

  payload = {
    'delete': {
      'ids': ids
    }
  }

  response = requests.post(rules_url, auth=auth, json=payload)

  if response.status_code != 200:
    raise Exception(f"Cannot delete rules (HTTP %d): %s" % (response.status_code, response.text))

def set_rules(rules, rules_url, auth):
  if rules is None:
    return

  payload = {
    'add': rules
  }

  response = requests.post(rules_url, auth=auth, json=payload)

  if response.status_code != 201:
    raise Exception(f"Cannot create rules (HTTP %d): %s" % (response.status_code, response.text))

def response_process(data):
    # Convert JSON response into dictionary
    tweet_data = json.loads(data)
    # Isolate Tweet Data 
    twitter_connection = tweet_data.get('connection_issue', False)
    #Test for connection issue
    if twitter_connection:
        return twitter_connection
    else:
        pass
    # Get Tweet ID for Filter
    tweet_id = tweet_data.get('data').get('id', False)
    if tweet_id:
        twitter_uname = EnvKeys.twitter_user
        # Build Tweet URL
        tweet_url = "https://twitter.com/{}/status/{}".format(twitter_uname, tweet_id)
        slack_response = notify_slack(tweet_url)
        url_status = "{}, {}".format(tweet_url, slack_response)
        return url_status
    else:
        return "Nothing to see here waiting for the next tweet"

def setup_rules(auth):
  rules_url = "https://api.twitter.com/labs/1/tweets/stream/filter/rules"
  filter_rules = [
    { 'value': 'from:1278071662009696256 🍕' },
    ]
  current_rules = get_all_rules(rules_url, auth)
  delete_all_rules(current_rules, rules_url, auth)
  set_rules(filter_rules, rules_url, auth)

def stream_connect(auth):
  stream_url = "https://api.twitter.com/labs/1/tweets/stream/filter"
  response = requests.get(stream_url, auth=auth, stream=True)
  for response_line in response.iter_lines():
    if response_line:
        tweet_content = response_process(response_line)
        pprint(tweet_content)

def main():
    
    consumer_key = EnvKeys.client_key  # Add your API key here
    consumer_secret = EnvKeys.client_secret # Add your API secret key here
    bearer_token = BearerTokenAuth(consumer_key, consumer_secret)

    # Comment this line if you already setup rules and want to keep them
    setup_rules(bearer_token)

    # Listen to the stream.
    # This reconnection logic will attempt to reconnect when a disconnection is detected.
    # To avoid rate limites, this logic implements exponential backoff, so the wait time
    # will increase if the client cannot reconnect to the stream.
    timeout = 0
    while True:
        pprint("Starting twitter stream reader. Printed URLs are posted to Slack")
        stream_connect(bearer_token)
        pprint("Stream reader stopped, backing off and retrying connection")
        sleep(2 ** timeout)
        timeout += 1

if __name__ == "__main__":
    main()