#written by evanamaya
import os
import pandas as pd
from boxplot_chart import run

inputDir = "/Users/aidenamaya/nlp-suite/input"
outputDir = "/Users/aidenamaya/nlp-suite/output"


inputDir = "/Users/evanamaya4/nlp-suite/input"
outputDir = "/Users/evanamaya4/nlp-suite/output"

os.makedirs(inputDir, exist_ok=True)
os.makedirs(outputDir, exist_ok=True)

inputFilename = "/Users/evanamaya4/Desktop/nlp-suite-agent/lib/sentimentLib/EnglishShortenedANEW.csv"


csv_field_visualization_var = "valence"
points_var = "All points"
split_data_byCategory_var = False
csv_field_boxplot_var = ""
csv_field_boxplot_color_var = ""

inputFileData = pd.read_csv(inputFilename, encoding="utf-8-sig", on_bad_lines="skip")

run(
    inputFilename=inputFilename,
    outputDir=outputDir,
    csv_field_visualization_var=csv_field_visualization_var,
    points_var=points_var,
    split_data_byCategory_var=split_data_byCategory_var,
    csv_field_boxplot_var=csv_field_boxplot_var,
    csv_field_boxplot_color_var=csv_field_boxplot_color_var,
    inputFileData=inputFileData,
)
