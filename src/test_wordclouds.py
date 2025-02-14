from wordcloud_visual import run_wordcloud
import os
inputDir = '/Users/aidenamaya/nlp-suite/input'
outputDir = '/Users/aidenamaya/nlp-suite/output'

# Ensure the directories exist
os.makedirs(inputDir, exist_ok=True)
os.makedirs(outputDir, exist_ok=True)

inputFilename = ""
visualization_tools = "Python WordCloud"
prefer_horizontal = False
font = "Default"
lemmatize = True
exclude_stopwords = True

exclude_punctuation = True
collocation = False
differentPOS_differentColor = False
lowercase = True
prepare_image_var = False
selectedImage = ""
use_contour_only = True
differentColumns_differentColors = False
csvField_color_list = False
openOutputFiles= False
doNotCreateIntermediateFiles = True

max_words = 100

inputFilename = ""

run_wordcloud(inputFilename, inputDir, outputDir, visualization_tools, prefer_horizontal, font,
        max_words, lemmatize, exclude_stopwords, exclude_punctuation, lowercase, collocation, differentPOS_differentColor,
        prepare_image_var,selectedImage, use_contour_only,
        differentColumns_differentColors, csvField_color_list, openOutputFiles, doNotCreateIntermediateFiles)
