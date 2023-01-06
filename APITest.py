import json
import http.client
import datetime
from constants import *
from replit import db
import os

def makeTwitterRequest(query: str = query) -> dict:
  """
  Makes API request and records response.
  Returns: A string of the API JSON response.
  Note: Use postman to see an example result.
  """

  #edit out latest?

  Current_Date = datetime.datetime.today() - datetime.timedelta(hours=1)
 # inital population
  Previous_Date = datetime.datetime.today() - datetime.timedelta(days=7)
  start_time = Previous_Date.strftime("%Y-%m-%dT%H:%M:%SZ")
  end_time = Current_Date.strftime("%Y-%m-%dT%H:%M:%SZ")

  conn = http.client.HTTPSConnection("api.twitter.com")
  twitterPayload = ''

  query = query.replace(" ", "%20")

  conn.request(
    "GET", "/2/tweets/search/recent?query=" + query +
    "%20-is:retweet%20lang:" + language + "&start_time=" + start_time +
    "&end_time=" + end_time + "&max_results=" + str(tweetsPerRequest) +
    "&tweet.fields=author_id,created_at,lang,text,public_metrics",
    twitterPayload, twitterHeaders)

  res = conn.getresponse()
  data = res.read()
  res = {}  #initialize db as a dictionary
  res = json.loads(data.decode("utf-8"))
  # print error messages if any error happend
  if 'errors' in res:
    for err in res['errors']:
      print(err['message'])

  return res


def newsAPIRequest(query:str) -> dict:
  """
  Makes an api request to newsapi.org.
  Requires:
    query: str - the topic to search
  Returns:
    res: dict - a dictionary containing the response
  """
  query = query.replace(' ', '%20')
  fromDate = datetime.datetime.today() - datetime.timedelta(days=7)
  fromDate = fromDate.strftime('%Y-%m-%d')
  conn = http.client.HTTPSConnection("newsapi.org")
  payload = ''
  headers = { 
    #remember to store your api key in Secrets!
    'Authorization': os.environ['newsapi_apikey'],
    'User-Agent': os.environ['newsapi_apikey']
  }
  conn.request("GET", "/v2/everything?q=" + query +
               "&searchIn=title,description&from=" + fromDate +
               "&sortby=relevancy&language=en", payload, headers)
  res = conn.getresponse()
  data = res.read()
  res = json.loads(data.decode("utf-8"))
  return res

  
response = newsAPIRequest('Artificial Intelligence')
print(response['articles'][0])