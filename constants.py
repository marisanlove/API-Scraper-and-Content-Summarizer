import os
# Constants
language = 'en'
valueList = [1, 3, 5] # value of likes, retweets, and replys
tweetsPerRequest = 100
bearer_token = os.environ['bearer_token']
twitterHeaders = {
  'Authorization': 'Bearer ' + bearer_token,
  'Cookie': 'guest_id=v1%3A167150872451172946'
}
query = 'aritificial intelligence'