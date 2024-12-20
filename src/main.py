import os
from threading import Thread
from typing import Annotated
from enum import Enum

import uvicorn
from fastapi import FastAPI, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from parsers_annotators import run_parsers_annotators
from sentiment_analysis import run_sentiment_analysis
from topic_modeling import run_topic_modeling
from word2vec import run_word2vec
from sunburst_charts import run_sun_burst
#from style_analysis import run_style_analysis

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
    chartPackage: Annotated[str, Form()],
    transformation: Annotated[str, Form()],
    numberOfTopics: Annotated[int, Form()],
    topicModelingBERT: Annotated[bool, Form()] = False,
    splitToSentence: Annotated[bool, Form()] = False,
    topicModelingMALLET: Annotated[bool, Form()] = False,
    optimizeTopicIntervals: Annotated[bool, Form()] = False,
    topicModelingGensim: Annotated[bool, Form()] = False,
    removeStopwords: Annotated[bool, Form()] = False,
    lemmatizeWords: Annotated[bool, Form()] = False,
    nounsOnly_var: Annotated[bool, Form()] = False,
    Gensim_MALLET_var: Annotated[bool, Form()] = False,
):
    inputDirectory = os.path.join(os.path.expanduser("~"), "nlp-suite", "input")
    outputDirectory = os.path.join(os.path.expanduser("~"), "nlp-suite", "output")
    thread = Thread(
        target=lambda: run(
            app,
            lambda: run_topic_modeling(
                inputDir=inputDirectory,
                outputDir=outputDirectory,
                chartPackage=chartPackage, 
                dataTransformation=transformation,
                num_topics=numberOfTopics,
                BERT_var=topicModelingBERT,
                split_docs_var=splitToSentence,
                MALLET_var=topicModelingMALLET,
                optimize_intervals_var=optimizeTopicIntervals,
                Gensim_var=topicModelingGensim,
                remove_stopwords_var=removeStopwords,
                lemmatize_var=lemmatizeWords,
                nounsOnly_var=nounsOnly_var,
                Gensim_MALLET_var=Gensim_MALLET_var,
            ),
        )
    )
    thread.start()
    return PlainTextResponse("", status_code=200)

@app.post("/parsers_annotators")
def parsers_annotators(
    inputDir: Annotated[str, Form()] = '',
    dataTransformation: Annotated[str, Form()] = '',
    # extra_GUIs_var: Annotated[bool, Form()] = False,
    # extra_GUIs_menu_var: Annotated[str, Form()] = '',
    manual_Coref: Annotated[bool, Form()] = False,
    # open_GUI: Annotated[bool, Form()] = False,
    parser_var: Annotated[bool, Form()] = False,
    parser_menu_var: Annotated[str, Form()] = '',
    single_quote: Annotated[bool, Form()] = False,
    # CoNLL_table_analyzer_var: Annotated[bool, Form()] = False,
    chartPackage: Annotated[str, Form()] = 'Excel',
    annotators_var: Annotated[bool, Form()] = False,
    annotators_menu_var: Annotated[str, Form()] = '',
):
    # Define input and output directories
    inputFilename = inputDir # TODO
    inputDirectory = os.path.join(os.path.expanduser("~"), "nlp-suite", "input")
    outputDirectory = os.path.join(os.path.expanduser("~"), "nlp-suite", "output")

    # Start the processing in a separate thread
    thread = Thread(
        # target=lambda: run_parsers_annotators(
        #     inputFilename=inputFilename,
        #     inputDir=inputDirectory,
        #     outputDir=outputDirectory,
        #     chartPackage="Excel",    # Default chart package
        #     dataTransformation=transformation,
        #     extra_GUIs_var=extra_GUIs_var,
        #     extra_GUIs_menu_var=extra_GUIs_menu_var,
        #     manual_Coref=manual_Coref,
        #     open_GUI=open_GUI,
        #     parser_var=parser_var,
        #     parser_menu_var=parser_menu_var,
        #     single_quote=single_quote,
        #     CoNLL_table_analyzer_var=CoNLL_table_analyzer_var,
        #     annotators_var=annotators_var,
        #     annotators_menu_var=annotators_menu_var,
        # )
        target=lambda: run(
            app,
            lambda: run_parsers_annotators(
                inputFilename=inputFilename,
                inputDir=inputDirectory,
                outputDir=outputDirectory,
                chartPackage=chartPackage,
                dataTransformation=dataTransformation,
                manual_Coref=manual_Coref, 
                parser_var=parser_var,
                parser_menu_var=parser_menu_var,
                single_quote=single_quote,
                CoNLL_table_analyzer_var=False,
                annotators_var=annotators_var,
                annotators_menu_var=annotators_menu_var
            )
        )
    )
    thread.start()
    return PlainTextResponse("", status_code=200)

@app.post("/word2vec")
def word2vec(
    # inputFilename: Annotated[str, Form()], 
    inputDirectory: Annotated[str, Form()],
    outputDirectory: Annotated[str, Form()],
    transformation: Annotated[str, Form()],
    chartPackage: Annotated[str, Form()] = 'Excel',
    removeStopwords: Annotated[bool, Form()] = False,
    lemmatize: Annotated[bool, Form()] = False,
    wordSenseInduction: Annotated[bool, Form()] = False,
    wordEmbeddingsBERT: Annotated[bool, Form()] = False,
    word2VecGensim: Annotated[bool, Form()] = False,
    skipGram: Annotated[str, Form()] = "Skip-Gram",
    vectorSize: Annotated[int, Form()] = 100,
    windowSize: Annotated[int, Form()] = 5,
    minCount: Annotated[int, Form()] = 5,
    plotWordVectors: Annotated[str, Form()] = "Plot word vectors",
    dimension: Annotated[str, Form()] = "2D",
    computeWordDistances: Annotated[bool, Form()] = False,
    topWords: Annotated[int, Form()] = 200,
    keyWords: Annotated[str, Form()] = "",
    keywordInput: Annotated[str, Form()] = "",
    kMeansMin: Annotated[int, Form()] = 4,
    kMeansMax: Annotated[int, Form()] = 6,
    range20: Annotated[int, Form()] = 10,
    ngrams: Annotated[str, Form()] = "1-grams"
):
    inputFilename = ""
    inputDirectory = os.path.join(os.path.expanduser("~"), "nlp-suite", "input")
    outputDirectory = os.path.join(os.path.expanduser("~"), "nlp-suite", "output")
    thread = Thread(
        target=lambda: run(
            app,
            lambda: run_word2vec(
                inputFilename=inputFilename,
                inputDir=inputDirectory,
                outputDir=outputDirectory,
                chartPackage=chartPackage,
                dataTransformation=transformation, 
                remove_stopwords_var=removeStopwords,
                lemmatize_var=lemmatize,
                WSI_var=wordSenseInduction,
                BERT_var=wordEmbeddingsBERT,
                Gensim_var=word2VecGensim,
                sg_menu_var=skipGram,
                vector_size_var=vectorSize,
                window_var=windowSize,
                min_count_var=minCount,
                vis_menu_var=plotWordVectors,
                dim_menu_var=dimension,
                compute_distances_var=computeWordDistances,
                top_words_var=topWords,
                keywords_var=keyWords,
                keywordInput=keywordInput,
                range4=kMeansMin,
                range6=kMeansMax,
                range20=range20,
                ngramsDropDown=ngrams
            ),
        )
    )
    thread.start()
    return PlainTextResponse("", status_code=200)


# @app.post("/style_analysis")
# def style_analysis(
#         # inputFilename: Annotated[str, Form()],
#         inputDirectory: Annotated[str, Form()],
#         outputDirectory: Annotated[str, Form()],
#         chartPackage: Annotated[str, Form()] = 'Excel',
#         transformation: Annotated[str, Form()] = 'no_transformation',
#         extra_GUIs_var: Annotated[bool, Form()] = False,
#         complexity_analysis: Annotated[bool, Form()] = False,
#         analysis_dropdown: Annotated[str, Form()] = '*',
#         vocabulary_analysis: Annotated[bool, Form()] = False,
#         voc_options: Annotated[str, Form()] = '*',
#         gender_guesser: Annotated[bool, Form()] = False, 
#         min_rating: Annotated[int, Form()] = 5,
#         max_rating_sd: Annotated[int, Form()] = 2
# ):
#     inputFilename = ""
#     inputDirectory = os.path.join(os.path.expanduser("~"), "nlp-suite", "input")
#     outputDirectory = os.path.join(os.path.expanduser("~"), "nlp-suite", "output")
#     thread = Thread(
#         target=lambda: run(
#             app,
#             lambda: run_style_analysis(
#                 inputFilename = inputFilename,
#                 inputDir = inputDirectory,
#                 outputDir = outputDirectory,
#                 chartPackage = chartPackage, 
#                 dataTransformation = transformation,
#                 extra_GUIs_var = extra_GUIs_var,
#                 complexity_readability_analysis_var = complexity_analysis,
#                 complexity_readability_analysis_menu_var = analysis_dropdown,
#                 vocabulary_analysis_var = vocabulary_analysis,
#                 vocabulary_analysis_menu_var = voc_options,
#                 gender_guesser_var = gender_guesser,
#                 min_rating = min_rating,
#                 max_rating_sd = max_rating_sd
#             ),
#         )
#     )
#     thread.start()
#     return PlainTextResponse("", status_code=200)



@app.post("/sunburst_charts")
def sunburst_charts(
        sunburst_file_input: Annotated[str, Form()],
        inputDirectory: Annotated[str, Form()],
        outputDirectory: Annotated[str, Form()],
        file_data: Annotated[str, Form()] = "",
        filter_options_var: Annotated[str, Form()] = "No filtering",
        selected_pairs_data: Annotated[str, Form()] = "[]",
        piechart_var: Annotated[bool, Form()] = False, 
        treemap_var: Annotated[bool, Form()] = False,
):
    inputDirectory = os.path.join(os.path.expanduser("~"), "nlp-suite", "input")
    outputDirectory = os.path.join(os.path.expanduser("~"), "nlp-suite", "output")
    
    thread = Thread(
        target=lambda: run(
            app,
            lambda: run_sun_burst(
                inputFilename = sunburst_file_input,
                inputDir = inputDirectory,
                outputDir = outputDirectory,
                file_data = file_data,
                filter_options_var = filter_options_var,
                selected_pairs_data = selected_pairs_data,
                piechart_var = piechart_var,
                treemap_var = treemap_var 
            ),
        )
    )
    thread.start()
    return PlainTextResponse("", status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, port=3000, host="0.0.0.0")
