from threading import Thread
from typing import Annotated
from fastapi import FastAPI, Form, Request
from fastapi.responses import PlainTextResponse

from sentiment_analysis import run_sentiment_analysis 

import os

app = FastAPI()
app.worker = False

def run(app, method):
    method()
    app.worker = False

@app.middleware("http")
async def single_runner(request: Request, call_next):
    if app.worker:
        return PlainTextResponse("The agent is currently busy running another job", status_code = 503)

    app.worker = True
    response = await call_next(request)
    if response.status_code >= 400:
        app.worker = False
    return response

@app.post("/sentiment_analysis")
def sentiment_analysis(inputDirectory: Annotated[str, Form()], outputDirectory: Annotated[str, Form()], transformation: Annotated[str, Form()], calculateMean: Annotated[bool, Form()], calculateMedian: Annotated[bool, Form()], algorithm: Annotated[str, Form()]):
    inputDirectory = os.path.join(os.path.expanduser("~"), "nlp-suite", "input")
    outputDirectory = os.path.join(os.path.expanduser("~"), "nlp-suite", "output")
    thread = Thread( target = lambda: run(app, lambda: run_sentiment_analysis(inputDirectory, outputDirectory, False, "Excel", transformation, calculateMean, calculateMedian, algorithm)))
    thread.start()
    return PlainTextResponse("", status_code=200)