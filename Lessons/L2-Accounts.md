## How to use Postman to generate API GET code

### Steps to make Twitter and Postman

The following steps walk you through setting up an account with Twitter API and Postman and requesting the Twitter API using Postman. Postman is a popular online API management tool that is helpful in building API calls and will be used in this course.

Note: while this part is unfortunately not very code-heavy, it is important that we do all of this before getting our hands dirty in the code (which we will next lesson).


* Step 1:
  *  Create a [Twitter Developer](https://developer.twitter.com/en/docs/twitter-api) account and make sure to *save* your given **API Key, API Key Secret and Bearer Token**.
      *  This requires creating (or, as it's worded, 'applying for') a Twitter Developer account, which is tied to your regular Twitter account, and will give you access to the [Developer Portal](https://developer.twitter.com/en/portal/dashboard). The account creation screen looks like: ![Twitter Developer Account Creation screen](/images/developer_account_creation.png)
      *  Once you get past the account creation and name your app whatever you'd like, you will be shown your three app keys (API Key, API Key Secret and Bearer Token)—**hold onto these, as these are very important** because they are what give you access to the Twitter API v2. Be sure to save these in the [Replit Secrets Manager](https://docs.replit.com/programming-ide/storing-sensitive-information-environment-variables), located under 'Tools' (bottom left of screen). Call your bearer token secret 'tBearer'. We will come back to the secrets manager later when we need to access the keys.
  *  Create a [Postman](https://www.postman.com) account
* Step 2:
  *  In the [Tweets lookup](https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/quick-start) page, under **Steps to build a GET /tweets request**, load the Twitter API v2 Postman collection into your Postman environment by *clicking* **Add Twitter API v2 to Postman** (it may take a quick second to load) ![Add Twitter API v2 to Postman](/images/Add_Twitter_API_Postman.png)
      *  You may notice the term 'endpoint' used here (and later, in Postman)—an API endpoint is the point at which an API connects with the software program and exchanges information; typically, it is usually just a URL that your program will *request* for information (i.e., access) via a **GET request**. In our case, the Twitter API v2 endpoint for tweet information is ```https://api.twitter.com/2/tweets```. If you try accessing the endpoint from your browser, notice that you will get an 'Unsupported Authentication' error because the browser is not sending the proper key information needed to access the API. We will get into requesting the API programatically with all of the correct key information soon. There are plenty of good articles and videos explaining APIs and different request types more in depth, [here is one](https://www.smashingmagazine.com/2018/01/understanding-using-rest-api/) to get you started.

* Step 3:
  * After adding the Twitter API into Postman, you will be brought to the Twitter Public Workspace, which is analogous to a public view-only google doc. Twitter has already preconfigured and added all of the Postman methods needed to request its API (boxed in red), we can just fork (copy) the workspace—which we will do together below—and start using them: ![search by keyword](/images/postman_twitter_workspace.png) Let's take a look at how to use these methods, starting with the ```Recent search``` GET method (in the ```Search Tweets``` folder): ![search by keyword](/images/postman_method_screen.png) This method enables us to search recent tweets with a given keyword. In order to do this, we must provide the keyword(s) we want to search for. We can do this by entering it in the ```VALUE``` field of the ```query``` parameter (you may have to scroll to the top of the parameters to find it). Notice how there are lots of other parameters we can check. Those serve to provide more information to the API to narrow down our request even further. Also notice how when we do check or modify a parameter value, the URL (endpoint) in the ```GET``` bar is modified to include the parameter. The image below is just showing the query parameter with value 'ArtificialIntelligence'—feel free to explore with others!
        ![search by keyword](/images/keyword.png)
Before we can click the Send button to send our request to the API, Postman will ask us to create a fork (akin to copying a google doc) into our own personal workspace. From there you will be taken to a screen identical to when you first added the Twitter Public Workspace into Postman, only this time, it's in your personal workspace.

* Step 4:
  * Find the ```Recent search``` method again (located in the same spot in your method folders) and fill in the ```query``` parameter once more.
  Now if we try sending our request, we get a response! But instead of a list of tweets, we get an 'Unauthorized' error? ![bearer token](/images/postman_failed_send.png)
The reason for this is, like when you tried requesting the URL with your browser, we still haven't put the Twitter API app keys we got earlier into our request. Postman lets us do this very easily: select the ```Authorization``` tab under the URL bar, choose ```Bearer Token```, retrieve the Bearer token you entered into the the Replit secrets manager, and enter it into the ```Token``` field.
        ![bearer token](/images/bearer_token.png)

* Step 5:
  * Tada! Hit send, and we now get tweet data from 10 tweets that contain the given keyword(s)!
  * Now that we know our request works, we can see the Python code (complete with the Bearer token in the Authorization key of the headers dictionary) for the request by clicking the ```</>``` on the right handside of the screen and choosing the language—be sure to choose ```Python - http.client```.
     ![Code](/images/code.png)

  Armed with this code, let's move on to the next lesson to actually start implementing the newsroom!

### Useful links
* [How to use Twitter API v2 | Tweet lookup, User lookup, Likes, Timelines, Search, Tweet count](https://www.youtube.com/watch?v=kgNNhjTGLN0) 
* [Getting started with Postman](https://developer.twitter.com/en/docs/tutorials/postman-getting-started)
* [Twitter API v2](https://documenter.getpostman.com/view/9956214/T1LMiT5U)
* [Authentication](https://developer.twitter.com/en/docs/authentication/api-reference)