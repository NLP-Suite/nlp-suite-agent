# test_topic_modeling.py
import os
from sentence_analysis import run_sentence_analysis

# Replace with your input and output directories
inputDir = '/Users/aidenamaya/nlp-suite/input'
outputDir = '/Users/aidenamaya/nlp-suite/output'

inputFilename = ''

# Ensure the directories exist
os.makedirs(inputDir, exist_ok=True)
os.makedirs(outputDir, exist_ok=True)

# Set parameters
chartPackage='Excel'
dataTransformation=''

compute_sentence_length_var = True
sentence_complexity_var = True
text_readability_var = True
visualize_sentence_structure_var = True


#These variables aren't in the gui?
visualize_bySentenceIndex_var = False
visualize_bySentenceIndex_options_var = ''
IO_values = ''
script_to_run = ''

# Run the topic modeling function
run_sentence_analysis(
    inputFilename = '',
    inputDir = inputDir,
    outputDir = outputDir,
    openOutputFiles = False,
    chartPackage = "Excel",
    dataTransformation = "No transformation",
    compute_sentence_length_var = compute_sentence_length_var,
    visualize_bySentenceIndex_var = visualize_bySentenceIndex_var,
    visualize_bySentenceIndex_options_var = visualize_bySentenceIndex_options_var,
    script_to_run = script_to_run,
    IO_values = script_to_run,
    sentence_complexity_var = sentence_complexity_var,
    text_readability_var = text_readability_var,
    visualize_sentence_structure_var = visualize_sentence_structure_var,
    num_sentences = 1
)
    

                        
