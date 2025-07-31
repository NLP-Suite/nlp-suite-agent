import os
from threading import Thread
from typing import Annotated, List
from enum import Enum

import uvicorn
from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, RedirectResponse

from parsers_annotators import run_parsers_annotators
from sentiment_analysis import run_sentiment_analysis
from topic_modeling import run_topic_modeling
from word2vec import run_word2vec
from sunburst_charts import run_sun_burst
from colormap_chart import run_colormap
from sankey_flowchart import run_sankey
from CoNLL_main import run_conll
from wordcloud_visual import run_wordcloud

from style_analysis import run_style_analysis
from SVO import run_svo
from NGrams_CoOccurrences import run_ngrams

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
    try: 
        method()
        
    except Exception as e:
        app.worker_exception = e
        
    finally:
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
    if hasattr(app, 'worker_exception') and app.worker_exception:
        e = app.worker_exception
        app.worker_exception = None
        
        raise HTTPException(status_code=500, detail=str(e))

    # thread = Thread(
    #     target=lambda: run(
    #         app,
    #         lambda: None,
    #     )
    # )
    # thread.start()
    # return PlainTextResponse("", status_code=200)


@app.post("/sentiment_analysis")
def sentiment_analysis(
    inputDirectory: Annotated[str, Form()],
    outputDirectory: Annotated[str, Form()],
    transformation: Annotated[str, Form()],
    algorithm: Annotated[str, Form()],
    calculateMean: Annotated[bool, Form()] = False,
    calculateMedian: Annotated[bool, Form()] = False,
    
):
    try:
        inputDirectory = os.path.expanduser(inputDirectory)

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
    
    except Exception as e:
        print("Error: ", e)
        return RedirectResponse("./error.html", status_code=302)

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
    try:
        inputDirectory = os.path.expanduser(inputDirectory)
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
    except Exception as e:
        print("Error: ", e)
        return RedirectResponse("./error.html", status_code=302)

@app.post("/parsers_annotators")
def parsers_annotators(
    inputDirectory: Annotated[str, Form()],
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
    inputFilename =  ''
    inputDirectory = os.path.expanduser(inputDirectory)
    outputDirectory = os.path.join(os.path.expanduser("~"), "nlp-suite", "output")
    openOutputFiles = False
    # Start the processing in a separate thread
    thread = Thread(
        target=lambda: run(
            app,
            lambda: run_parsers_annotators(
                inputFilename=inputFilename,
                inputDir=inputDirectory,
                outputDir=outputDirectory,
                openOutputFiles=openOutputFiles,
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
    ngrams: Annotated[str, Form()],
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
):
    inputFilename = ""
    inputDirectory = os.path.expanduser(inputDirectory)
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

@app.post("/CoNLL_table_analyzer_main")
def conll_table_analyzer(
    inputFilename: Annotated[str, Form()], 
    inputDirectory: Annotated[str, Form()],
    outputDirectory: Annotated[str, Form()], 
    chart_packages: Annotated[str, Form()],
    transformation: Annotated[str, Form()], 
    conll_search_field: Annotated[str, Form()], 
    search_kw: Annotated[str, Form()], 
    postag: Annotated[str, Form()], 
    deprel: Annotated[str, Form()], 
    postag_b: Annotated[str, Form()], 
    deprel_b: Annotated[str, Form()],
    Begin_K_sent_var: Annotated[bool, Form()] = False,
    End_K_sent_var: Annotated[bool, Form()] = False,
    openOutputFiles: Annotated[bool, Form()] = False,
    compute_sentence_table: Annotated[bool, Form()] = False,
    search_token_word_checkbox: Annotated[bool, Form()] = False, 
    repetition_finder: Annotated[bool, Form()] = False, 
    clause_noun_verb_function: Annotated[bool, Form()] = False, 
    clause_noun_verb_function_options: Annotated[str, Form()] = False 

):
    inputFilename = ""
    inputDirectory = os.path.expanduser(inputDirectory)
    outputDirectory = os.path.join(os.path.expanduser("~"), "nlp-suite", "output")
    thread = Thread(
        target=lambda: run(
            app,
            lambda: run_conll(
                inputFilename=inputFilename,
                inputDir=inputDirectory,
                outputDir=outputDirectory,
                openOutputFiles=openOutputFiles, 
                chartPackage=chart_packages, 
                dataTransformation=transformation,
                searchedCoNLLField=conll_search_field,
                searchField_kw=search_kw,
                postag=postag,
                deprel=deprel,
                co_postag=postag_b,
                co_deprel=deprel_b,
                Begin_K_sent_var=Begin_K_sent_var,
                End_K_sent_var=End_K_sent_var,
                compute_sentence_var = compute_sentence_table,
                search_token_var = search_token_word_checkbox,
                k_sentences_var = repetition_finder,
                all_analyses_vars = clause_noun_verb_function,
                all_analyses = clause_noun_verb_function_options, 
            ),
        )
    )
    thread.start()
    return PlainTextResponse("", status_code=200)


@app.post("/style_analysis")
def style_analysis(
        inputDirectory: Annotated[str, Form()],
        outputDirectory: Annotated[str, Form()],
        analysis_dropdown: Annotated[str, Form()],
        voc_options: Annotated[str, Form()],
        min_rating: Annotated[int, Form()],
        max_rating_sd: Annotated[int, Form()],
        chartPackage: Annotated[str, Form()] = 'Excel',
        transformation: Annotated[str, Form()] = 'no_transformation',
        complexity_analysis: Annotated[bool, Form()] = False,
        vocabulary_analysis: Annotated[bool, Form()] = False,
        gender_guesser: Annotated[bool, Form()] = False, 
):
    inputFilename = ""
    extra_GUIs_var = False
    inputDirectory = os.path.expanduser(inputDirectory)
    outputDirectory = os.path.join(os.path.expanduser("~"), "nlp-suite", "output")
    gender_guesser = False
        
    thread = Thread(
        target=lambda: run(
            app,
            lambda: run_style_analysis(
                inputFilename = inputFilename,
                inputDir = inputDirectory,
                outputDir = outputDirectory,
                chartPackage = chartPackage, 
                dataTransformation = transformation,
                extra_GUIs_var = extra_GUIs_var,
                complexity_readability_analysis_var = complexity_analysis,
                complexity_readability_analysis_menu_var = analysis_dropdown,
                vocabulary_analysis_var = vocabulary_analysis,
                vocabulary_analysis_menu_var = voc_options,
                gender_guesser_var = gender_guesser,
                min_rating = min_rating,
                max_rating_sd = max_rating_sd
            ),
        )
    )
    thread.start()
    return PlainTextResponse("", status_code=200)



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
    inputDirectory = os.path.expanduser(inputDirectory)
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

@app.post("/colormap_chart")
def colormap_chart(
    colormap_file_input: Annotated[str, Form()],
    outputDirectory: Annotated[str, Form()],
    max_number_of_rows: Annotated[int, Form()],
    less_freq_color_picker: Annotated[str, Form()],
    csv_file_categorical_field_list_front: Annotated[str, Form()] = '[]', 
    more_freq_color_picker: Annotated[str, Form()] = False,
    normalize: Annotated[str, Form()] = False,
    file_data: Annotated[str, Form()] = "",

):
    # inputDirectory = os.path.expanduser(inputDirectory)
    outputDirectory = os.path.join(os.path.expanduser("~"), "nlp-suite", "output")
    thread = Thread(
        target=lambda: run(
            app,
            lambda: run_colormap(
                inputFilename=colormap_file_input,
                outputDir=outputDirectory,
                csv_file_categorical_field_list=csv_file_categorical_field_list_front, 
                max_rows_var= max_number_of_rows,
                color_1_style_var=less_freq_color_picker,
                color_2_style_var=more_freq_color_picker,
                normalize_var=normalize,
                inputFileData=file_data,
            ),
        )
    )
    thread.start()
    return PlainTextResponse("", status_code=200)


@app.post("/sankey_flowchart")
def sankey_flowchart(
        inputDirectory: Annotated[str, Form()],
        outputDirectory: Annotated[str, Form()],
        variable_1_max: Annotated[int, Form()], 
        variable_2_max: Annotated[int, Form()], 
        variable_3_max: Annotated[int, Form()], 
        file_data: Annotated[str, Form()] = "",
        selected_pairs_data: Annotated[str, Form()] = "[]",
):
    inputDirectory = os.path.expanduser(inputDirectory)
    outputDirectory = os.path.join(os.path.expanduser("~"), "nlp-suite", "output")
    
    thread = Thread(
        target=lambda: run(
            app,
            lambda: run_sankey(
                data = file_data,
                inputDir = inputDirectory,
                outputDir = outputDirectory,
                csv_file_relational_field_list = selected_pairs_data,
                Sankey_limit1_var = variable_1_max,
                Sankey_limit2_var = variable_2_max,
                Sankey_limit3_var = variable_3_max,
            ),
        )
    )
    thread.start()
    return PlainTextResponse("", status_code=200)



@app.post("/SVO")
def SVO(
    inputDirectory: Annotated[str, Form()],
    outputDirectory: Annotated[str, Form()],
    transformation: Annotated[str, Form()],
    coreferenceResolution: Annotated[bool, Form()] = False,
    manualCoreference: Annotated[bool, Form()] = False,
    package: Annotated[str, Form()] = 'Excel',
    lemmatize_subjects: Annotated[bool, Form()] = False,
    filter_subjects: Annotated[bool, Form()] = False,
    lemmatize_verbs: Annotated[bool, Form()] =  False,
    filter_verbs: Annotated[bool, Form()] = False,
    lemmatize_objects: Annotated[bool, Form()] = False,
    filter_objects: Annotated[bool, Form()] = False,
    so_gender: Annotated[bool, Form()] = False,
    so_quote: Annotated[bool, Form()] = False,
):
    inputFilename = ""
    chartPackage = 'Excel'
    inputDirectory = os.path.expanduser(inputDirectory)
    outputDirectory = os.path.join(os.path.expanduser("~"), "nlp-suite", "output")
    thread = Thread(
        target=lambda: run(
            app,
            lambda: run_svo(
                inputFilename = inputFilename,
                inputDir = inputDirectory, 
                outputDir = outputDirectory, 
                openOutputFiles = False, 
                chartPackage = chartPackage, 
                dataTransformation = transformation,
                coref_var = coreferenceResolution,
                manual_coref_var = manualCoreference,
                normalized_NER_date_extractor_var = False,
                package_var = package,
                gender_var = so_gender,
                quote_var = so_quote,
                subjects_dict_path_var = False,
                verbs_dict_path_var = False,
                objects_dict_path_var = False,
                filter_subjects = filter_subjects,
                filter_verbs = filter_verbs,
                filter_objects = filter_objects,
                lemmatize_subjects = lemmatize_subjects,
                lemmatize_verbs = lemmatize_verbs,
                lemmatize_objects = lemmatize_objects,
                gephi_var = False,
                wordcloud_var = False,
                google_earth_var = False
            ),
        )
    )
    thread.start()
    return PlainTextResponse("", status_code=200)

@app.post("/wordclouds")
def wordcloud(
    inputDirectory: Annotated[str, Form()],
    outputDirectory: Annotated[str, Form()],
    wordcloudservice: Annotated[str, Form()],
    font_name: Annotated[str, Form()], 
    maxNumberOfWords: Annotated[int, Form()],
    horizontal: Annotated[bool, Form()] = False,
    stopwords: Annotated[bool, Form()] = False,
    lemmas: Annotated[bool, Form()] = False,
    punctuation: Annotated[bool, Form()] =  False,
    lowercase_checkbox: Annotated[bool, Form()] = False,
    collocation: Annotated[bool, Form()] = False,
    differentColorsByPOS: Annotated[bool, Form()] = False,
    prepareImage: Annotated[bool, Form()] = False,
    imageContour: Annotated[bool, Form()] = False,
    useColorsForCsvColumns: Annotated[bool, Form()] = False,
    csvField: Annotated[bool, Form()] = False,
    intermediateWordcloudFiles: Annotated[bool, Form()] = False,
):
    inputFilename = ""
    inputDirectory = os.path.expanduser(inputDirectory)
    outputDirectory = os.path.join(os.path.expanduser("~"), "nlp-suite", "output")
    selectedImage = ""
    openOuputfiles = False
    thread = Thread(
        target=lambda: run(
            app,
            lambda: run_wordcloud(
                inputFilename,
                inputDir = inputDirectory, 
                outputDir = outputDirectory, 
                visualization_tools = wordcloudservice, 
                prefer_horizontal = horizontal, 
                font = font_name,
                max_words = maxNumberOfWords, 
                lemmatize = lemmas, 
                exclude_stopwords = stopwords,
                exclude_punctuation = punctuation, 
                lowercase = lowercase_checkbox, 
                collocation = collocation, 
                differentPOS_differentColor = differentColorsByPOS,
                prepare_image_var =prepareImage,
                selectedImage = selectedImage, 
                use_contour_only = imageContour,
                differentColumns_differentColors = useColorsForCsvColumns, 
                csvField_color_list = csvField, 
                openOutputFiles = openOuputfiles , 
                doNotCreateIntermediateFiles = intermediateWordcloudFiles
            ),
        )
    )
    thread.start()
    return PlainTextResponse("", status_code=200)


@app.post("/NGrams_CoOccurrences.html")
def NGrams_CoOccurrences(
        inputDirectory: Annotated[str, Form()],
        outputDirectory: Annotated[str, Form()],
        openOutputFiles: Annotated[bool, Form()], 
        chartPackage: Annotated[str, Form()],
        dataTransformation: Annotated[str, Form()],
        ngrams_options_list: Annotated[str, Form()],
        Ngrams_compute_var: Annotated[bool, Form()],
        ngrams_menu_var: Annotated[str, Form()],
        ngrams_options_menu_var: Annotated[str, Form()],
        ngrams_size: Annotated[int, Form()],
        search_words: Annotated[str, Form()], 
        minus_K_words_var: Annotated[int, Form()],
        plus_K_words_var: Annotated[int, Form()],
        Ngrams_search_var: Annotated[bool, Form()],
        csv_file_var: Annotated[str, Form()],
        ngrams_viewer_var:  Annotated[bool, Form()],
        CoOcc_Viewer_var: Annotated[str, Form()],
        date_options: Annotated[bool, Form()],
        temporal_aggregation_var: Annotated[bool, Form()],
        viewer_options_list: Annotated[str, Form()],
        language_list: Annotated[str, Form()],
        config_input_output_numeric_options: Annotated[str, Form()],
        number_of_years: Annotated[int, Form()],
        
):
    inputFilename = ""
    inputDirectory = os.path.expanduser(inputDirectory)
    outputDirectory = os.path.join(os.path.expanduser("~"), "nlp-suite", "output")
        
    thread = Thread(
        target=lambda: run_ngrams(
            app,
            lambda: run_ngrams(
                    inputFilename=inputFilename,
                    inputDir=inputDirectory,
                    outputDir=outputDirectory,
                    openOutputFiles=openOutputFiles,
                    chartPackage=chartPackage,
                    dataTransformation=dataTransformation,

                    ngrams_options_list=ngrams_options_list,
                    Ngrams_compute_var=Ngrams_compute_var,
                    ngrams_menu_var=ngrams_menu_var,
                    ngrams_options_menu_var=ngrams_options_menu_var,
                    ngrams_size=ngrams_size,
                    search_words=search_words,
                    minus_K_words_var=minus_K_words_var,
                    plus_K_words_var=plus_K_words_var,
                    Ngrams_search_var=Ngrams_search_var,
                    csv_file_var=csv_file_var,
                    ngrams_viewer_var=ngrams_viewer_var,
                    CoOcc_Viewer_var=CoOcc_Viewer_var,
                    # within_sentence_co_occurrence_search_var=within_sentence_co_occurrence_search_var,
                    date_options=date_options,
                    temporal_aggregation_var=temporal_aggregation_var,
                    viewer_options_list=viewer_options_list,
                    language_list=language_list,
                    config_input_output_numeric_options=config_input_output_numeric_options,
                    number_of_years=number_of_years
            ),
        )
    )
    thread.start()
    return PlainTextResponse("", status_code=200)


if __name__ == "__main__":
    uvicorn.run(app, port=3000, host="0.0.0.0")
