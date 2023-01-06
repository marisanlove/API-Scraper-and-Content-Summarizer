import http.client
import os
import json
import requests
import datetime
#from pprint import pprint
from replit import db
import time
from huggingface_hub.inference_api import InferenceApi
import pdb
from utils import *

#Hard Coded Vars
# key work for tweets
key_word = 'Artificial Intelligence'.replace(' ', '%20')
# lanuage, 'en' stand for English
language = 'en'

likeVal = 1
rtVal = 3
replyVal = 5
tweetsPerRequest = 10
minBetweenRefresh = 0.25


def getDB(start: int, end: int) -> list:
  """Returns tweets in the replit database that are from index start
  to index end in the form of a list."""
  output = []
  for i in range(start, end + 1):
    output.append(db[str(i)])

  return output


#


def pointVal(dict: dict, likeVal: int, rtVal: int, replyVal: int) -> int:
  """Returns an int that is the combined weighed popularity score of
  a tweets public metrics dictionary."""
  output = dict['like_count'] * likeVal
  output += dict['retweet_count'] * rtVal
  output += dict['reply_count'] * replyVal
  return output


#


def populate(lst):
  """Takes the full list of an api request and the first and last replit DB indexes to fill,
  and populates the replitDB with the tweets"""
  for i in range(len(lst)):
    db[str(i)] = lst[i]


#


def jsonToLst(jsondb):
  output = []
  for i in range(jsondb['meta']['result_count']):
    temp = {}
    temp['tweetID'] = jsondb['data'][i]['id']
    temp['text'] = jsondb['data'][i]['text']
    temp['authorID'] = jsondb['data'][i]['author_id']
    temp['date'] = jsondb['data'][i]['created_at']
    temp['retweets'] = jsondb['data'][i]['public_metrics']['retweet_count']
    temp['likes'] = jsondb['data'][i]['public_metrics']['like_count']
    temp['replies'] = jsondb['data'][i]['public_metrics']['reply_count']
    temp['popularity'] = pointVal(jsondb['data'][i]['public_metrics'], likeVal,
                                  rtVal, replyVal)
    output.append(temp)
  print("Tweets grabbed: " + str(len(output)))
  return output


#


#a quicksort partition for the popularitySort function
def popSortPart(lst, low, high):
  pivot = lst[high]["popularity"]

  i = low - 1

  for j in range(low, high):
    if lst[j]["popularity"] >= pivot:
      i += 1
      #swap value of index i and j
      (lst[i], lst[j]) = (lst[j], lst[i])

  #swap value of index i+1 and high
  (lst[i + 1], lst[high]) = (lst[high], lst[i + 1])
  return i + 1


#


#sorts the replitDB between indexes low and high by popularity score
#using quicksort algorithm (O(logn) time)
def popularitySort(lst, low, high):
  if low < high:
    part = popSortPart(lst, low, high)

    popularitySort(lst, low, part - 1)
    popularitySort(lst, part + 1, high)


#


def dbInitialPopulate(lst):  #for the first time we open the site
  popularitySort(lst, 0, len(lst) - 1)
  populate(lst)
  printDBLst(lst)


#


def dbUpdate(lst):  #for each 5 min update
  oldDB = getDB(0, tweetsPerRequest - 1)
  #print(len(lst+oldDB))
  popularitySort(lst + oldDB, 0, (tweetsPerRequest * 2) - 1)
  populate(lst)
  #printDBLst(lst)


#


def printDBLst(lst):
  print(lst[0]['text'])
  print(lst[0]['popularity'])
  print(len(lst))
  print(lst[-1]['text'])
  print(lst[-1]['popularity'])


#


# function used to get tweets using API request and return the output in list format
def newAPIRequest():
  # 'end_time'must be a minimum of 10 seconds prior to the request time.
  # latest time set up to be 1 hours ago from the currently time
  Current_Date = datetime.datetime.today() - datetime.timedelta(hours=1)
  Previous_Date = datetime.datetime.today() - datetime.timedelta(days=7)
  # converting time format to API required format
  start_time = Previous_Date.strftime("%Y-%m-%dT%H:%M:%SZ")
  end_time = Current_Date.strftime("%Y-%m-%dT%H:%M:%SZ")

  conn = http.client.HTTPSConnection("api.twitter.com")
  payload = ''
  headers = {
    # passed the bearer_token access code
    'Authorization': "Bearer " + os.environ['bearer_token'],
    'Cookie': 'guest_id=v1%3A167150872451172946'
  }
  # Get the tweets (only in English post and excluding public ads) based on the key_word input that contains the information such as posted times, author id, text and public_metrics (like_count, quote_count,reply_count and retweet_count) from API
  conn.request(
    "GET",
    "/2/tweets/search/recent?query=" + key_word +
    # I believe the '20-is:ad' is meant to be a '%20-is:ad,'
    # but in any case twitter throws an 'Invalid Operator' error;
    # is:ad is invalid?
    # changed "%20-is:ad&start_time=" to "&start_time="
    "%20-is:retweet%20lang:" + language + "&start_time=" + start_time +
    "&end_time=" + end_time + "&max_results=" + str(tweetsPerRequest) +
    "&tweet.fields=author_id,created_at,lang,text,public_metrics",
    payload,
    headers)
  res = conn.getresponse()
  data = res.read()
  #pprint(data.decode("utf-8"))
  # print(json.loads(data.decode("utf-8")))

  jsondb = {}  #initialize db as a dictionary
  jsondb = json.loads(
    data.decode("utf-8"))  #turn data into utf-8 json then a string
  return jsonToLst(jsondb)  #return a list


#


def cleansText(orig_list: list) -> str:
  """Given a json in the format of a list, cleans the text of the tweets of urls, emojis, and symbols, preparing it for summerization."""
  text_list = [temp_dict['text'] for temp_dict in orig_list]
  whole_text = ''
  for text in text_list:
    temp_text = url_free_text(text)
    temp_text = give_emoji_free_text(temp_text)
    temp_text = symbol_free_text(temp_text)
    whole_text += temp_text
  return whole_text


def summarize(input_text):
  inf_headers = {"Authorization": f"Bearer {os.environ['inference_api']}"}
  API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

  def query(payload):
    data = json.dumps(payload)
    response = requests.request("POST",
                                API_URL,
                                headers=inf_headers,
                                data=data)
    return json.loads(response.content.decode("utf-8"))

  summary = query({
    "inputs": input_text,
    "parameters": {
      "do_sample": False,
      'min_length': 120,
      'max_length': 180
    },
  })
  return summary


if __name__ == "__main__":
  #Main Program
  jsonLst = newAPIRequest()
  print("Made it here")
  pdb.set_trace()
  clean_text = cleansText(jsonLst)
  summary = summarize(input_text=clean_text)[0]['summary_text']
  print('Summary: ', summary)
  dbInitialPopulate(jsonLst)
  uptime = 0  #initialize uptime limit
  uptimeLimit = 20  #limit of uptime in minutes
  while (uptime <= (uptimeLimit * 60)):  #limit uptime to 20min
    time.sleep(minBetweenRefresh * 60)
    uptime += (minBetweenRefresh * 60)
    jsonLst = newAPIRequest()
    summary = summarize(input_text=clean_text)[0]['summary_text']
    print('Summary: ', summary)
    dbUpdate(jsonLst)
  #
"""
#store tweet info as linked lists
authorL, idL, textL, = [], [], []  #initialize idList as a list
dateL, metricL = [], []

for i in range(jsondb['meta']['result_count']):  #for every tweet in the result count
  idL.append(jsondb['data'][i]['id'])  #add the id of the tweet
  textL.append(jsondb['data'][i]['text'])  #add the text of the tweet
  authorL.append(jsondb['data'][i]['author_id']) #add author of tweet
  dateL.append(jsondb['data'][i]['created_at']) #add the date of the tweet
  metricL.append(jsondb['data'][i]['public_metrics']) #add the public metrics dict

#point value linked list
ptsL = [pointVal(dict, likeVal, rtVal, replyVal) for dict in metricL]
"""
#db["test"] = "1"
print("done")
"""
#TODO
#Get most popular tweets for query (wait 5min inbetween)
  #get name of the author of each tweet
#clean api response into dictionary
#use AI to verify the tweet is actually talking about the topic
#start website using flask(?)
#utilize database to give data to front end
"""

# model = T5ForConditionalGeneration.from_pretrained('t5-base')
# tokenizer = T5Tokenizer.from_pretrained('t5-base')
# preprocessed_text = "summarize: " + whole_text
# tokens_input = tokenizer.encode(preprocessed_text,return_tensors="pt", truncation=True)
# summary_ids = model.generate(tokens_input,
#                               min_length=60,
#                               max_length=180,
#                               length_penalty=4.0)
# summary = tokenizer.decode(summary_ids[0])
# print(summary)

# tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
# model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")

# tokens_input = tokenizer.encode("summarize: "+whole_text, return_tensors='pt', max_length=512, truncation=True)
# ids = model.generate(tokens_input, min_length=80, max_length=120)
# summary = tokenizer.decode(ids[0], skip_special_tokens=True)
# print(summary)
