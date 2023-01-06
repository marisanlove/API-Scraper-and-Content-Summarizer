# Lesson Outline
We need to clean up the tweets that we obtained in the previous lessons.

The purpose of the Twitter Newsroom we're building is to allow users to quickly and efficiently track and understand certain content being shared on Twitter, at any time. Displaying all this data can be overwhelming to the user, so we need to break it down and make these Tweets easier to read.

Here are the refining steps we need to take:

1. Filter out Profanity
2. Filter out unwanted content (URLS, '@' Tags, Hashtags, and emojis )
3. Summarizing and condensing Tweets into their essential content


Twitter is an extremely vibrant community- tweets often contain emojis and symbols that may not be relevant to the content of the tweets and can potentially interfere with the summarization process, while profanity may not be suitable for all audiences.

## Here's how we'll do it:


### APIs
We'll be making good use of APIs to do this. APIs have been covered in earlier lessons, so either review those or look up "What are APIs?" for more information. 

Here are the APIs we will be using:

1. **HuggingFace API**- we'll be using the Huggingface API to interface with their BART text summarization model, to summarize our tweets.
2. **PurgoMalum API**- This API will be used to cleanse the tweets from profanity



### Regular expressions and other Libraries
We'll be using Regular expressions, or Regex, to filter out unwanted symbols and text such as tags or hashtags. 

These topics will be covered in detail in the following lessons. 


