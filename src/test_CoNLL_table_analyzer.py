# test_topic_modeling.py
import os
from CoNLL_table_analyzer_main import run

# Replace with your input and output directories
inputDir = '/Users/is2ac/nlp-suite/input'
inputFilename = '/Users/is2ac/nlp-suite/input/NLP_CoreNLP_Dir_English_nn_CoNLL.csv'
outputDir = '/Users/is2ac/nlp-suite/output'

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
    inputFilename=inputFilename,
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
