# test_topic_modeling.py
import os
from CoNLL_table_analyzer_main import run

# Replace with your input and output directories
inputDir = "/Users/aidenamaya/nlp-suite/csvInput"
outputDir = '/Users/aidenamaya/nlp-suite/output'
inputFilename = inputDir 
# Ensure the directories exist
os.makedirs(inputDir, exist_ok=True)
os.makedirs(outputDir, exist_ok=True)

# Set parameters
openOutputFiles = 1
chartPackage='Excel'
dataTransformation=''
searchedCoNLLField='FORM' #LEMMA
searchField_kw='e.g.: father'
postag='*'
deprel='*'
co_postag='*'
co_deprel='*'
Begin_K_sent_var=0
End_K_sent_var=0



# Run the topic modeling function
# def run(inputFilename, inputDir, outputDir, openOutputFiles, chartPackage, dataTransformation,
#         searchedCoNLLField, searchField_kw, postag, deprel, co_postag, co_deprel, Begin_K_sent_var, End_K_sent_var):
run(
    inputFilename="",
    inputDir=inputDir,
    outputDir=outputDir,
    openOutputFiles=openOutputFiles,
    chartPackage=chartPackage,
    dataTransformation=dataTransformation,
    searchedCoNLLField='FORM', #LEMMA
    searchField_kw='e.g.: father',
    postag='*',
    deprel='*',
    co_postag='*',
    co_deprel='*',
    Begin_K_sent_var=0,
    End_K_sent_var=0
)
