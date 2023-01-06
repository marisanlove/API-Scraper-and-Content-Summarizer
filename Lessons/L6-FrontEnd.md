
#  Building a Web App for Your Program

In this lesson, we will put together everything we have so far and create a newsroom web application. This app allows users to interact with the APIs through a simple user interface. You will learn how to use Flask to handle user request and render data to your frontend website.

Because user interfaces are highly customizable, we won't go in to the details on web design. In this scaffold, we used vanilla HTML and CSS. You can make changes to it as you like or create your own design from scratch. We will also include some resources on web design in the references section.

## How to run the app
Before we start building, let's try out the app to see how it works. 

There are two ways to run the application. You can click on the green run button at the top of the repl. If the run is successful, you should see a message similar to this in the `Console`. 

![console](/images/runAppSuccess.png)

Alternatively, you can open up a `Shell` window and enter `python3 app.py`. You should see the same message appear in your shell. 

To see your web app, head to the side bar on the left, select `Tools` then click on `Webview` 
![webview](/images/webview.png)

# Intro to Flask

In our web application we need to display information, allow users to input and submit data, and interact with other APIs. When developing these features, we often use a [web framework](https://intelegain-technologies.medium.com/what-are-web-frameworks-and-why-you-need-them-c4e8806bd0fb#:~:text=GeeksforGeeks%20describes%20%E2%80%98web,miscalculations%20and%20faults).

The web framework we will be using is Flask. It provides a set of tools and libraries that allow us to build web applications in Python. 

In this tutorial, we will walk you througih the structure of our application and highlight the things you need to understand and implement. If you are interested in learning more about Flask, we have a list of recommended resources in the last section. 


# Program Structure
```
./
├── app.py
├── templates/
│   ├── index.html
│   └── home.html
├── static/
│   └── main.css
├── utils.py
└── constants.py
```


### `app.py`

This is were we create our Flask application that connects everything together. In this file we handle user input, routing , and rendering content. We will go more in-depth on how this works in the code walk-through section.

### templates folder
Templates are HTML files that defines the structure of your webpages. In Flask, all the html files shoudl live in a folder called `templates`. 

### static folder 
Static files are usually style sheets for our HTML files, and images, video or audio files we want to render on your webpages. These files should always be stored in a `static` folder. 

### `utils.py`
We put helper functions and functions that runs in the background here to keep our `app.py` clean. 

### `constants.py` 
This file holds all the constant variables used across scripts. 

Having a separate file keeps our main scripts clean and makes our life easier. We don't need to search through multiple files to find the variable we want to change.

```python
  # Example
  # in constants.py
  MY_CONSTANT = 1 
    
  # in main.py (or any script where you want to import the constants)
  from constants import * 
  print(MY_CONSTANT)
    
  >>> 1
```

# Code Walk-through
In this section we will walk through our code base, highlighting what you need to implement.

For simplicity, we will use news data as examples in this section, but implementing the same features for twitter data is similar. 

## `app.py`
### importing libraries and modules
```python
from flask import Flask, render_template, url_for, request
from replit import db  
from constants import *
from utils import *
```
In Python, we can use `import` statements to include code from external Python libraries or other files in our program. 

In our application, we need to import Flask framework and replit database. We also need to import our own code from `constants.py` and `utils.py`. 

When we use `from utils import *` in `app.py`, we are simply importing all the functions and variables from `utils.py`. Then we can use these functions and variables as if we defined them in `app.py`.

### Create a Flask application instance 
```python
app = Flask(__name__)
```

The `__name__` argument is passed in the Flask class to create its [instance](https://towardsdatascience.com/practical-python-class-vs-instance-variables-431fd16430d). We assign it to a variable named `app`, which represents our application. 


### Context variable
The context variable is a dictionary that stores all the data we would like to serve to the frontend when we make API calls. We'll talk more about how excatly the context variable is served to the frontend in a later section.

```python
context = {
  'tweets': [], 
  'news': [],
  'articles_summary': '',
  'tweet_summary': '',
  'articles_count': 0,
  'tweet_count': 0,
}  
```


Here we assign them some default values so that when an API call fails, we would still be able to have a functioning web page (just rendering these empty values).


### Routing
`route()` is a special Python [decorator](https://realpython.com/primer-on-python-decorators/#:~:text=Decorators%20provide%20a%20simple%20syntax,function%20without%20explicitly%20modifying%20it.) that tells Flask **which URL should trigger which function**. 
```python
@app.route('/')
def home():
  return render_template('home.html')
```


In this case if we navigate to our root url, Flask will call the `home()` function, which renders `home.html` file. We'll cover more details on template rendering in a later section.


### User request
Try entering a query and hit submit, you will notice that you are redirected to a url ending with `/query`. What happens under the hood is that you send a `POST` request to the application, asking the it to perform a query based on your input.

`POST` request is an [HTTP method](https://www.ibm.com/docs/en/cics-ts/5.3?topic=protocol-http-requests#:~:text=An%20HTTP%20request%20is%20made%20by%20a%20client%2C%20to%20a%20named%20host%2C%20which%20is%20located%20on%20a%20server.%20The%20aim%20of%20the%20request%20is%20to%20access%20a%20resource%20on%20the%20server.) that 
sends input to a server to create/update a resource.

To handle a `POST` request in Flask when the input is a text field, we need to do the following steps: 

**1. Create a `<form>` element in the template.**
   
```html
<form action={{ url_for('query') }} method="POST">
``` 

The `action` attribute specifies the URL user will be redirected to when they submit the form, and the `method` specifies the HTTP method user invokes. 

`url_for()` accepts the name of a function and returns the route/URL the function is bind to. We can also put `"/query"` here, but using `url_for()` is always preferred. When we change the route of a function, `url_for()` always returns the updated route.

In this case, when a user hits submit, we redirect them to `/query`. Remember what happens when the user navigate to a route?  Flask will run `query()`.

**2. Add a methods attribute to the function decorator.**

```python
	@app.route('/query/', methods=['GET', 'POST'])
```

We can use decorator to specify which HTTP methods are allowed for a particular route. By default, the decorator allows the `GET` method, which is used to retrieve information from the application. 

In our case, the user will be **sending data** to our app, which is an example of `POST` method.
	
**3. Using Flask request method**
   
In Flask, user requests are handled with the **request** object. To use the Flask request object, we need to import it with `from flask import request`.

Then we need to retrieve specific fields the user provided through this HTML form we defined. 


```html
	<!-- in index.html, we created a field with name = "query" inside the <form> tag -->

	<input type="text" name="query" placeholder='Type Here...'>
```
In Flask, the information is sent back in `request.form` as a dictionary. The keys of this dictionary are the form `name` attributes and values are the corresponding inputs. 

```python
	# in app.py
	query = request.form['query']  
```

In `query()` we access the input field by its `name` attribute.

We store this value in a variable so we can use it in the script to run API requests. 



### Render templates with variables
We've seen how to render a static webpage with `render_templates()` in `home()` function. 

What's powerful about the `render_template()` function is its ability to serve dynamic content.

We can provide it with a template and some variables. It then generates the final HTML page by filling in the placeholders with the variables and returning it to the user.

Let's take a look at the `query()` function as an example
```python
# in app.py
def query()
  ...
  context['articles_summary'] = summaryModel()

return render_template('index.html', **context)
```

```html
<!-- in index.html -->
<p> {{ articles_summary }} </p>
```

In `query()`, we generate a summary for tweets, and store it in the context variable. Recall that the context variable is a dictionary. In the template file, we access the value by wrapping its **key** in `{{ }}`. 

### Using Jinja2 to generate dynamic content
The above example demonstrated how we can pass a single value back to a reserved space in the frontend. In our application, we want to achieve something more complex.

We have a list of 10 news articles we want to generate. The naive approach is to create 10 key-value pairs in `app.py` and create 10 `<li>` elements like this 
```html
<li class='news' id='1'>
    <p class='card_heading'> {{ art1.title }} </p>
	  <p id='news_article'> {{ art1.description }} </p>
</li>
<li class='news' id='2'>
    <p class='card_heading'> {{ art2.title }} </p>
	  <p id='news_article'> {{ art2.description }} </p>
</li>
.
.
.
<li class='news' id='10'>
    <p class='card_heading'> {{ art10.title }} </p>
	  <p id='news_article'> {{ art10.description }} </p>
</li>
```
There are two issues with this approach. 
First, depending on the query, we might get less than 10 results from the API calls. Then some of the key-value pairs will be undefined, causing errors in our program.

Second, we are writing a lot of redundant code in HTML. All the element looks exactly the same except for the content. 



>If you were to work with a list variable of unknown length in Python, where you would apply the same operation to all the elements, what would you usually do? 

You would use a **for loop**!


In Flask, we can use a tool called [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/templates/) to write for loops in html files. 

Let's see how it works.
First we store our posts in a list of dictionaries 
```python
# in app.py
context['news'] = news
# news is a list of dictionaries; see `getNewsFeed()` for details.
```

Then in `index.html` we can use the following syntax to run a for loop through  `context['news']`

```html
{% for art in news %} 
<li class='news'>
      <p class='card_heading'>{{ art.title }} </p>
	  <p id='news_article'> {{ art.description }} </p>
</li>
{% endfor %} 
   ```
Every iteration of the loop will create an `<li>` element and fill in the article's title and description.


### Running the application
Finally we want to configure the app such that when we run `python3 app.py`, the app will start.
```python
if __name__ == "__main__":
  app.run(debug=True) 
```
The `if __name__ == "__main__":` block is a common idiom in Python that's used to specify that the code inside the block should only be executed if the script is run directly, rather than imported as a module.

The `app.run()` function starts the server. We set debug to `True` so that when there's an error, Flask will show the detailed error message on the webpage.


# Replit Database
Having a database in our project makes it possible to access the same data from different scripts. It also makes sure we don't lose data we retrieved when we stop running the application. 

Replit [database](https://docs.replit.com/hosting/database-faq) is a key value storage built in to every repl. Repl also supports SQLite3. We chose Replit DB because it provides us with the most flexibility. We can store data in any data structure and add a new field at anytime without having to worry about the structure of existing data. 

**How to use:**
```python3
# import it in the script you need to use the database
from replit import db 

# it functions exactly like a python dictionary
db['key'] = 'x' 
db['my_list'] = [1, 2, 3]

print(db['key'])
>>> 'x'

print(db['my_list'])
>>> [1, 2, 3]
```


# References
### Frontend Design
- [HTML](https://www.w3schools.com/html/html_intro.asp) defines the structure of your webpage
- [CSS](https://www.w3schools.com/html/html_css.asp) defines the style of your webpage elements
- [Bootstrap](https://www.w3schools.com/bootstrap5/index.php) and [Tailwind](https://tailwindcss.com/) are css frameworks that make stylizing your webpage easier

### Flask 
- [QuickStart](https://flask.palletsprojects.com/en/1.1.x/quickstart/#quickstart)
- TODO Notes on local deployment