import os
from threading import Thread
from typing import Annotated
from enum import Enum

import uvicorn
from fastapi import FastAPI, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from sentiment_analysis import run_sentiment_analysis
from topic_modeling import run_topic_modeling
#from svo import run_svo
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
    algorithm: Annotated[str, Form()],
    calculateMean: Annotated[bool, Form()] = False,
    calculateMedian: Annotated[bool, Form()] = False,
    
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

@app.post("/topic_modeling")
def topic_modeling(
    inputDirectory: Annotated[str, Form()],
    outputDirectory: Annotated[str, Form()],
    transformation: Annotated[str, Form()],
    numberOfTopics: Annotated[int, Form()],
    topicModelingBERT: Annotated[bool, Form()] = False,
    splitToSentence: Annotated[bool, Form()] = False,
    topicModelingMALLET: Annotated[bool, Form()] = False,
    optimizeTopicIntervals: Annotated[bool, Form()] = False,
    topicModelingGensim: Annotated[bool, Form()] = False,
    removeStopwords: Annotated[bool, Form()] = False,
    lemmatizeWords: Annotated[bool, Form()] = False,
    # dataTransformation: Annotated[str, Form()],
    # num_topics: Annotated[int, Form()],
    # BERT_var: Annotated[bool, Form()],
    # split_docs_var: Annotated[bool, Form()],
    # MALLET_var: Annotated[bool, Form()],
    # optimize_intervals_var: Annotated[bool, Form()],
    # Gensim_var: Annotated[bool, Form()],
    # remove_stopwords_var: Annotated[bool, Form()],
    # lemmatize_var: Annotated[bool, Form()],
    # nounsOnly_var: Annotated[bool, Form()],
    # Gensim_MALLET_var: Annotated[bool, Form()],
):
    inputDirectory = os.path.join(os.path.expanduser("~"), "nlp-suite", "input")
    outputDirectory = os.path.join(os.path.expanduser("~"), "nlp-suite", "output")
    thread = Thread(
        target=lambda: run(
            app,
            lambda: run_topic_modeling(
                inputDir=inputDirectory,
                outputDir=outputDirectory,
                openOutputFiles=False,  # openOutputFiles
                chartPackage="Excel",  # chartPackage
                dataTransformation=transformation,
                num_topics=numberOfTopics,
                BERT_var=topicModelingBERT,
                split_docs_var=splitToSentence,
                MALLET_var=topicModelingMALLET,
                optimize_intervals_var=optimizeTopicIntervals,
                Gensim_var=topicModelingGensim,
                remove_stopwords_var=removeStopwords,
                lemmatize_var=lemmatizeWords,
                nounsOnly_var=lemmatizeWords,
                Gensim_MALLET_var=False,
                # dataTransformation,
                # num_topics,
                # BERT_var,
                # split_docs_var,
                # MALLET_var,
                # optimize_intervals_var,
                # Gensim_var,
                # remove_stopwords_var,
                # lemmatize_var,
                # nounsOnly_var,
                # Gensim_MALLET_var,
            ),
        )
    )
    thread.start()
    return PlainTextResponse("", status_code=200)

@app.post("/parsers_annotators")
def parsers_annotators(
    inputFilename: Annotated[str, Form()] = '',
    transformation: Annotated[str, Form()] = '',
    extra_GUIs_var: Annotated[bool, Form()] = False,
    extra_GUIs_menu_var: Annotated[str, Form()] = '',
    manual_Coref: Annotated[bool, Form()] = False,
    open_GUI: Annotated[bool, Form()] = False,
    parser_var: Annotated[bool, Form()] = False,
    parser_menu_var: Annotated[str, Form()] = '',
    single_quote: Annotated[bool, Form()] = False,
    CoNLL_table_analyzer_var: Annotated[bool, Form()] = False,
    annotators_var: Annotated[bool, Form()] = False,
    annotators_menu_var: Annotated[str, Form()] = '',
):
    # Define input and output directories
    inputDirectory = os.path.join(os.path.expanduser("~"), "nlp-suite", "input")
    outputDirectory = os.path.join(os.path.expanduser("~"), "nlp-suite", "output")

    # Start the processing in a separate thread
    thread = Thread(
        target=lambda: run(
            inputFilename=inputFilename,
            inputDir=inputDirectory,
            outputDir=outputDirectory,
            openOutputFiles=False,  
            chartPackage="Excel",    # Default chart package
            dataTransformation=transformation,
            extra_GUIs_var=extra_GUIs_var,
            extra_GUIs_menu_var=extra_GUIs_menu_var,
            manual_Coref=manual_Coref,
            open_GUI=open_GUI,
            parser_var=parser_var,
            parser_menu_var=parser_menu_var,
            single_quote=single_quote,
            CoNLL_table_analyzer_var=CoNLL_table_analyzer_var,
            annotators_var=annotators_var,
            annotators_menu_var=annotators_menu_var,
        )
    )
    thread.start()
    return PlainTextResponse("Processing started.", status_code=200)

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

# @app.post("/svo")
# def svo(
#     inputDirectory: Annotated[str, Form()] = Form(...),
#     outputDirectory: Annotated[str, Form()] = Form(...),
#     coreferenceResolution: Annotated[bool, Form()] = Form(False),
#     manualCoreference: Annotated[bool, Form()] = Form(False),
#     package: Annotated[PackageChoice, Form()] = Form(...),
#     lemmatizeS: Annotated[bool, Form()] = Form(False),
#     filterS: Annotated[bool, Form()] = Form(False),
#     lemmatizeV: Annotated[bool, Form()] = Form(False),
#     filterV: Annotated[bool, Form()] = Form(False),
#     lemmatizeO: Annotated[bool, Form()] = Form(False),
#     filterO: Annotated[bool, Form()] = Form(False),
#     SOgender: Annotated[bool, Form()] = Form(False),
#     SOquote: Annotated[bool, Form()] = Form(False),
#     network_graphs: Annotated[bool, Form()] = Form(False),
#     wordcloud: Annotated[bool, Form()] = Form(False),
#     google_earth_maps: Annotated[bool, Form()] = Form(False),
#     transformation: Annotated[TransformationType, Form()] = Form(...),
# ):
#     inputDirectory = os.path.join(os.path.expanduser("~"), "nlp-suite", "input")
#     outputDirectory = os.path.join(os.path.expanduser("~"), "nlp-suite", "output")
#     thread = Thread(
#         target=lambda: run_svo(
#             inputDirectory, outputDirectory,
#             transformation, coreferenceResolution, manualCoreference, package.value, SOgender, SOquote,
#             filterS, filterV, filterO,
#             lemmatizeS, lemmatizeV, lemmatizeO,
#             network_graphs, wordcloud, google_earth_maps
#         )
#     )
#     thread.start()
#     return PlainTextResponse("SVO extraction initiated", status_code=200)


if __name__ == "__main__":
    uvicorn.run(app, port=3000, host="0.0.0.0")
