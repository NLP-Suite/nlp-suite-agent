import os
from threading import Thread
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from sentiment_analysis import run_sentiment_analysis

app = FastAPI()
origins = [
    "*",
    "http://172.16.0.11:8000",
    "http://0.0.0.0:8000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.worker = False


def run(app, method):
    method()
    app.worker = False


@app.middleware("http")
async def single_runner(request: Request, call_next):
    if app.worker:
        return PlainTextResponse(
            "The agent is currently busy running another job", status_code=503
        )

    app.worker = True
    response = await call_next(request)
    if response.status_code >= 400:
        app.worker = False
    return response


@app.get("/status")
def status():
    thread = Thread(
        target=lambda: run(
            app,
            lambda: None,
        )
    )
    thread.start()
    return PlainTextResponse("", status_code=200)


@app.post("/sentiment_analysis")
def sentiment_analysis(
    inputDirectory: Annotated[str, Form()],
    outputDirectory: Annotated[str, Form()],
    transformation: Annotated[str, Form()],
    calculateMean: Annotated[bool, Form()],
    calculateMedian: Annotated[bool, Form()],
    algorithm: Annotated[str, Form()],
):
    inputDirectory = os.path.join(os.path.expanduser("~"), "nlp-suite", "input")
    outputDirectory = os.path.join(os.path.expanduser("~"), "nlp-suite", "output")
    thread = Thread(
        target=lambda: run(
            app,
            lambda: run_sentiment_analysis(
                inputDirectory,
                outputDirectory,
                False,
                "Excel",
                transformation,
                calculateMean,
                calculateMedian,
                algorithm,
            ),
        )
    )
    thread.start()
    return PlainTextResponse("", status_code=200)

class PackageChoice(str, Enum):
    spaCy = "spaCy"
    stanfordCoreNLP = "stanfordCoreNLP"
    stanza = "stanza"
    openIE = "openIE"

class TransformationType(str, Enum):
    no_transformation = "no_transformation"
    Ln = "Ln"
    Log = "Log"
    Square = "Square root"
    Z_score = "Z score"

@app.post("/svo")
def svo(
    inputDirectory: Annotated[str, Form()] = Form(...),
    outputDirectory: Annotated[str, Form()] = Form(...),
    coreferenceResolution: Annotated[bool, Form()] = Form(False),
    manualCoreference: Annotated[bool, Form()] = Form(False),
    package: Annotated[PackageChoice, Form()] = Form(...),
    lemmatizeS: Annotated[bool, Form()] = Form(False),
    filterS: Annotated[bool, Form()] = Form(False),
    lemmatizeV: Annotated[bool, Form()] = Form(False),
    filterV: Annotated[bool, Form()] = Form(False),
    lemmatizeO: Annotated[bool, Form()] = Form(False),
    filterO: Annotated[bool, Form()] = Form(False),
    SOgender: Annotated[bool, Form()] = Form(False),
    SOquote: Annotated[bool, Form()] = Form(False),
    network_graphs: Annotated[bool, Form()] = Form(False),
    wordcloud: Annotated[bool, Form()] = Form(False),
    google_earth_maps: Annotated[bool, Form()] = Form(False),
    transformation: Annotated[TransformationType, Form()] = Form(...),
):
    inputDir = os.path.join(os.path.expanduser("~"), "nlp-suite", "input")
    outputDir = os.path.join(os.path.expanduser("~"), "nlp-suite", "output")
    thread = Thread(
        target=lambda: run_svo(
            inputFilename, inputDir, outputDir, openOutputFiles, chartPackage,
            transformation, coreferenceResolution, manualCoreference, package.value, SOgender, SOquote,
            filterS, filterV, filterO,
            lemmatizeS, lemmatizeV, lemmatizeO,
            network_graphs, wordcloud, google_earth_maps
        )
    )
    thread.start()
    return PlainTextResponse("SVO extraction initiated", status_code=200)


if __name__ == "__main__":
    uvicorn.run(app, port=3000, host="0.0.0.0")
