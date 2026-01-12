import os
from CoNLL_main import run_conll

# Replace with your input and output directories
inputDir = '/Users/aidenamaya/nlp-suite/csvInput'
outputDir = '/Users/aidenamaya/nlp-suite/output'

# Ensure the directories exist
# Set parameters
inputFilename = ''# Will be overridden by inputDir inside run_conll
openOutputFiles = False
chartPackage = "Excel"
dataTransformation = ''
searchedCoNLLField = 'FORM'  # or 'LEMMA'
searchField_kw = ''
postag = ''
deprel = ''
co_postag = ''
co_deprel = ''
Begin_K_sent_var = 0
End_K_sent_var = 0
compute_sentence_var = False
search_token_var = False
k_sentences_var = False
all_analyses_var = False
all_analyses = '*'

# Run the function
run_conll(
    inputFilename,
    inputDir,
    outputDir,
    openOutputFiles,
    chartPackage,
    dataTransformation,
    searchedCoNLLField,
    searchField_kw,
    postag,
    deprel,
    co_postag,
    co_deprel,
    Begin_K_sent_var,
    End_K_sent_var,
    compute_sentence_var,
    search_token_var,
    k_sentences_var,
    all_analyses_var,
    all_analyses
)
