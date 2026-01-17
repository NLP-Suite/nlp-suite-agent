from statistics_txt_main import run_statistics
inputDir = '/Users/aidenamaya/nlp-suite/input'
outputDir = '/Users/aidenamaya/nlp-suite/output'
inputFilename = ""

corpus_statistics_options_menu_var = "*"
corpus_text_options_menu_var = "*"
openOutputFiles = False
chartPackage = "Excel"
dataTransformation = "No transformation"
corpus_statistics_var = True
corpus_statistics_byPOS_var = True


run_statistics(inputFilename = inputFilename, inputDir = inputDir, outputDir = outputDir,
        corpus_statistics_options_menu_var = corpus_statistics_options_menu_var,
        corpus_text_options_menu_var = corpus_text_options_menu_var ,
        openOutputFiles = openOutputFiles,
        chartPackage = chartPackage,
        dataTransformation = dataTransformation,
        corpus_statistics_var = corpus_statistics_var,
        corpus_statistics_byPOS_var =corpus_statistics_byPOS_var)