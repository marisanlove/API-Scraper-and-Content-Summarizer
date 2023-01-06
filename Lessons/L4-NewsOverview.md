# Lesson Outline
We also want to display popular news articles next to the Tweets that we've pulled. We can do this by accessing the [NewsAPI](https://newsapi.org/).

In the following three lessons, we will learn how do to the following:

1. Make the API request and read the response
2. Clean the response
3. Send the cleaned response to the database

# What is the NewsAPI 

NewsAPI is a simple and easy-to-use API that allows developers to 
access current and historical news articles from various news 
sources and blogs. It allows users to search for articles by keyword, filter results by source or language, and sort articles by relevance, popularity, or date published.
![jsonimage](/images/newsapi.png)

## Getting Started

Similar to how we scraped tweets, lets create a new function in ```utils.py``` whose purpose is to call other functions. The only parameter it takes is the query.
```python
def newsPopulateDB(query: str):
```
Now let's get started writing the first function we're going to call!