Given a URL where the job listings are, this code calls gemini through it's python API and gets it to parse the html retrieved from a request. 

Gemini then converts the HTML into vaild JSON (hopefully....). However the structure of each json object is different. for example, culture amp json keys are ____ but REA group keys are ____. 


The flask web app does the following 2 things:
1) in a separate thread, perform the requests to the specified pages and update the database using the scraper
2) speak to the database and render the most current job listings. 

The base scraper class does the following:
1) using the URL, get the jobs.
2) from the retrieved jobs perform a bunch of checks here to only grab the new jobs, find expired jobs compared to last time, etc. 
3) From these, update the database


The flask app does the following
1) lets you perform a simple ping for the websites to determine if python can still talk to them (not the case if captchas present)
2) render and display all the current job listings for each current company
3) let you filter and interact with the data so that you can search for certain titles, locations, companies.


## How to start
ensure uv is installed

```$ uv sync```

The following environment variables need to be defined in the ```.env``` file:
- ```GEMINI_API_KEY``` : api key for calls to the Google Gemini LLM
- ```SENDER_EMAIL``` : self explanatory
- ```EMAIL_PASSWORD``` : app password for sender email from gmail server
- ```RECEIVER_EMAIL``` : self explanatory

```$ uv run app.py```

navigate to ```localhost:5000```

## Separate email notifications
