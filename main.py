from threading import Thread
from typing import Annotated
from fastapi import FastAPI, Form, Request
from fastapi.responses import PlainTextResponse

from src.sentiment_analysis import run_sentiment_analysis 

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
    return await call_next(request)

@app.post("/sentiment_analysis")
def sentiment_analysis(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    thread = Thread( target = lambda: run(app, lambda: run_sentiment_analysis()))
    thread.start()
    return PlainTextResponse("", status_code=200)

if __name__ == "__main__":
    app