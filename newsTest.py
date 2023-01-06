import http.client
import json
import os

# constants
articlesPerReq = 100
query = "artificial intelligence"


def newsAPIRequest(query: str = query) -> dict:
  """
  Makes an api request to newsapi.org.
  Requires:
    query: str - the topic to search
  Returns:
    res: dict - a dictionary containing the response
  """
  query = query.replace(' ', '%20')

  conn = http.client.HTTPSConnection("newsapi.org")
  payload = ''
  headers = {
    'Authorization': os.environ['newsapi_apikey'],
    'User-Agent': os.environ['newsapi_apikey']
  }

  conn.request(
    "GET",
    "/v2/everything?q=" + query +
    #"pageSize=" + str(articlesPerReq) +
    "&searchIn=title,description&from=12/16/2022&sortby=relevancy",
    payload,
    headers)
  
  res = conn.getresponse()
  data = res.read()
  res = json.loads(data.decode("utf-8"))
  
  return res


def cleanNewsAPIRes(data: dict, query: str = query) -> list:
  """
  Cleans the API response dictionary into a list of dictionaries, with each
  dictionary holding the info for one article. Any articles that do not have the
  query in the description or title are dropped.
  Requires:
    data: dict - a dictionary of the api response
    query: str - the query of the search
  Returns:
    output: list - a list of dictionaries, each an article
  """

  output = []

  for art in data['articles']:
    if (query in art['description']) or (query in art['title']):
      temp = {
        'source': art['source']['name'],
        'author': art['author'],
        'title': art['title'],
        'description': art['description'],
        'url': art['url'],
        'imageLink': art['urlToImage'],
        'date': art['publishedAt'],
        'content': art['content']
      }
      output.append(temp)
    #
  #
  return output


#


# example:
def main():
  newsAPIRes = newsAPIRequest(query)
  # print(newsAPIRes)

  cleanedRes = cleanNewsAPIRes(newsAPIRes, query)

  print("\n---------- Cleaned Res ----------")
  print(cleanedRes)


main()
