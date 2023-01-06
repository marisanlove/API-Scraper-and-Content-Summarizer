# Newsroom Scraper and Content Summarizer

In this course you will learn how to connect to News APIs to pull relevant data on a topic of your choice. You will then build a BART model to generate a summary of the content, run through the Huggingface Inference API. You will then deploy your model to the web using Flask and create a display for your very own Newsroom.

## Learning Objectives
1. Utilize Twitter and News APIs to get tweets and articles ready for summarization
2. Understand the basics of NLP and the BART model
3. Implement a content summarizer
4. Connect everything into a working webpage

## Overview of Concepts

### What is an API
An API, or an application programming interface, is a set of rules and ways for how your program can interact with another. In other words, they let your program interact with another using the internet.

Within your program, you can send a variety of commands to the recieving program. For example, we are going to send GET requests from our program to Twitter. A GET request is a request that a program sends to an API asking for some information or to run a program that the receiving API knows. For our purposes throughtout this course, it will be news articles, tweets, and an AI summarization program.

To read about other types of requests than GET, read more [here](https://assertible.com/blog/7-http-methods-every-web-developer-should-know-and-how-to-test-them).

### What is NLP
Natural Language Processing (NLP) is a subfield of artificial intelligence that deals with the interaction between computers and human (natural) languages. It involves developing algorithms and models that can process, analyze, and generate human-like text and speech.

NLP has a wide range of applications, including language translation, chatbot development, sentiment analysis, and text summarization. We will be using the BART model for text summarization in this course.

### What is BART and How Does it Work
BART is a state of the art NLP model that is known for its ability to handle long sequences of text and maintain good performance even when the input text is significantly longer than the training data. Bart has more capabilities beyond summarization too, such as end-to-end machine translation and language modeling.

### Replit Database
This project uses Replit Database. You can find this tool on the bottom right of your screen in the "tools" area. Replit Database works much like a python dictionary, but stores the data seperate from the runtime, allowing our program to take up less power and storage in the CPU and RAM. For example you can access data stored in the database like this:
```python
value = db['key']
```
where value is the information you want and key is the key in the database. The syntax to set a value in the database is similar:
```python
db['key'] = value
```
You can find more information about the database tool in replit's documentation [here](https://docs.replit.com/hosting/database-faq).

## Creating a new Repl
When you create a Repl, make sure you choose the Python template.