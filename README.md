# API Kitchen 

## What it is:

An automated API builder!

## Who it's for:

This will help you if you're doing something cool in Python and you want to make it available through a REST API, preferably rather quickly.
This will also help you if you haven't approached writing a backend before, but you have learned enough Python to do some basic experiments.

## What it's for:

Right now, this is only a backend that can accept a JSON specification (like the one in spec.json which describes this API and can be used for testing your local instance).
I'll be working on a few different front end clients for interfacing with it, but I'm publishing this backend repo as an open-source contribution.

## Why it's for:

Fun.

## How it works:

This tool takes advantage of a few very useful facts about Python.

1. There's not very much punctuation. A lot of the logic flow is done with indentation, which is really easy to generate with spaces.
2. There are libraries for EVERYTHING, and ChatGPT will gladly tell you all about most of them, including how you should use them to accomplish your goals.
3. It has [FastAPI](https://github.com/tiangolo/fastapi). FastAPI is an incredibly light-weight, self-documenting API framework that I could geek out about for much further than most attention spans span. Here's the highlights:
  - creates Swagger and Redoc documentation servers with ZERO CONFIG. It just reads your routes and documents them.
  - seamless integration with pydantic, a library for creating request and response models as well as any nested models within them. This makes request validation very quick and easy.
  - built-in uvicorn server reduces deployment to a few CLI commands

## Instructions:

Right now, as stated above, this is only a backend. If you want a front end, all it needs to do is build an object that is shaped like spec.json and send it to this application's api-gen endpoint. To run and/or modify this backend, follow these steps:

1. Clone this repo in a local directory. Make sure you have a Python environment (at least version 3.10)  set up there.
2. Use pip to install any of the imported libraries that your interpreter can't find in your local system. Key libs (listed by pip install command) include:
- fastapi
- matplotlib (for the charts example)
- pydantic
- uvicorn[standard] (for running the server)
3. From the app directory, run 
```
uvicorn main:app --reload
```
This will run a live development server with hot reload from localhost.

4. navigate to http://localhost:8000/docs to view the auto-generated documentation for your brand new REST API generator!

5. Copy the entire contents of spec.json and click the 'Try It Out' button in the Swagger UI. There, you can paste the json into the request body section. Don't forget to name your new test copy in the title field. Soon, this will be YOUR codebase you get to download.

6. Click Execute, scroll down past the (admittedly very large) request body, and click the Download File link in the response.

You should now have an exact copy of this codebase in a zip file!
And the unzipped contents should be under 100kb! (If not, please let me know)

That's it! Your API generation server just generated itself! Have fun modifying the spec to suit your needs!

I've provided a Dockerfile so that if you make local modifications to the codebase itself (much handier than modifying the spec.json without a front end), you can build your own image with the dependency chain intact. Just be sure to modify requirements.txt if you pull in any other dependencies or they will not be included in the container. To make that easier, you can run

```
python -m pip install pipreqs
pipreqs path/to/project
```

from the parent directory where the Dockerfile is contained. That will auto-generate a requirements.txt file by scanning your application's codebase.

Then you can run

```
docker build -t yourimagename:tag .
docker run -d --name yourcontainername -p 80:80 yourimagename:tag
```

Your modified API generator should be running locally on port 80. Navigate to http://localhost:80/docs to confirm your Swagger UI is properly documenting your API and you should be good to go!
