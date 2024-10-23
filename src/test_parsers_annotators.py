import os

from parsers_annotators import run

def test_parsers_annotators():
    inputFilename = 'C:/Users/sherry/OneDrive/Desktop/QTM446W/Input/Steinbeck_Grapes of wrath_14.txt'
    inputDir = os.path.join(os.path.expanduser("~"), "nlp-suite", "input")
    outputDir = os.path.join(os.path.expanduser("~"), "nlp-suite", "output")
    openOutputFiles = False
    chartPackage = "Excel"
    dataTransformation = ''
    manual_Coref = False
    parser_var = True  # Set to True to test the parser
    parser_menu_var = 'Neural Network'  # Example parser option
    single_quote = False
    CoNLL_table_analyzer_var = False
    annotators_var = True  # Set to True to test annotators
    annotators_menu_var = 'NER annotator'  

    try:
        output_files = run(
            inputFilename=inputFilename,
            inputDir = 'C:/Users/sherry/OneDrive/Desktop/QTM446W/Input', #inputDir=inputDir, 
            outputDir = 'C:/Users/sherry/OneDrive/Desktop/QTM446W/Output', #outputDir=outputDir,
            openOutputFiles=openOutputFiles,
            chartPackage=chartPackage,
            dataTransformation=dataTransformation,
            manual_Coref=manual_Coref,
            parser_var=parser_var,
            parser_menu_var=parser_menu_var,
            single_quote=single_quote,
            CoNLL_table_analyzer_var=CoNLL_table_analyzer_var,
            annotators_var=annotators_var,
            annotators_menu_var=annotators_menu_var,
        )

        # Check if output files are generated
        if output_files:
            print("Test passed. Output files generated:")
            for file in output_files:
                print(f"- {file}")
        else:
            print("Test failed. No output files generated.")

    except Exception as e:
        print(f"Test failed with exception: {e}")
        
if __name__ == "__main__":
    test_parsers_annotators()
