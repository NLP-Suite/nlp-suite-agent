from shape_of_stories_main import run
    
def main():
    # inputFilename = '/Users/is2ac/nlp-suite/input/example.txt'
    inputFilename = ''
    # inputDir = '/Users/is2ac/nlp-suite/input'
    inputDir = '/Users/is2ac/Documents/QTM_190/English'
    outputDir= '/Users/is2ac/nlp-suite/output'
    openOutputFiles = False
    chartPackage = "Excel"
    dataTransformation = ''
    sentimentAnalysis=True
    sentimentAnalysisMethod="Stanford CoreNLP"
    memory_var=6
    corpus_analysis=False
    hierarchical_clustering=True
    SVD=True
    NMF=True
    best_topic_estimation=False
    run(inputFilename, inputDir, outputDir, openOutputFiles, chartPackage, dataTransformation, sentimentAnalysis, sentimentAnalysisMethod, memory_var, corpus_analysis,
        hierarchical_clustering, SVD, NMF, best_topic_estimation)
    
if __name__ == '__main__':
    main()