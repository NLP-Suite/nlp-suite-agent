import logging
import CoNLL_clause_analysis_util
import CoNLL_noun_analysis_util
import CoNLL_verb_analysis_util
import CoNLL_function_words_analysis_util
import CoNLL_table_search_util
import IO_csv_util
import CoNLL_util
    
    
def run(inputFilename, inputDir, outputDir, openOutputFiles, chartPackage, dataTransformation,
        searchedCoNLLField, searchField_kw, postag, deprel, co_postag, co_deprel, Begin_K_sent_var, End_K_sent_var):
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    config_filename = 'NLP_default_IO_config.csv'
    filesToOpen = []

    # Reading CoNLL file data
    data, header = IO_csv_util.get_csv_data(inputFilename, True)
    if len(data) == 0:
        return
    all_CoNLL_records = CoNLL_util.CoNLL_record_division(data)
    if all_CoNLL_records is None or len(all_CoNLL_records) == 0:
        return

    if searchedCoNLLField == 'FORM':
        logger.info("Running FORM-based search")
    else:
        logger.info("Running LEMMA-based search")

    # Clause Analysis
    outputFiles = CoNLL_clause_analysis_util.clause_stats(inputFilename, '', outputDir, data, all_CoNLL_records, openOutputFiles, chartPackage, dataTransformation)
    if outputFiles:
        filesToOpen.extend(outputFiles)
    
    # Noun Analysis
    outputFiles = CoNLL_noun_analysis_util.noun_stats(inputFilename, outputDir, data, all_CoNLL_records, openOutputFiles, chartPackage, dataTransformation)
    if outputFiles:
        filesToOpen.extend(outputFiles)

    # Verb Analysis
    outputFiles = CoNLL_verb_analysis_util.verb_stats(config_filename, inputFilename, outputDir, data, all_CoNLL_records, openOutputFiles, chartPackage, dataTransformation)
    if outputFiles:
        filesToOpen.extend(outputFiles)

    # Function Words (Stop words) Analysis
    outputFiles = CoNLL_function_words_analysis_util.function_words_stats(inputFilename, outputDir, data, all_CoNLL_records, openOutputFiles, chartPackage, dataTransformation)
    if outputFiles:
        filesToOpen.extend(outputFiles)

    if searchField_kw and searchField_kw != 'e.g.: father':
        logger.info("Running token search on: %s", searchField_kw)
        temp_outputDir, outputFiles = CoNLL_table_search_util.search_CoNLL_table(inputFilename, outputDir, config_filename, chartPackage, dataTransformation, all_CoNLL_records, searchField_kw, searchedCoNLLField, postag, deprel, co_postag, co_deprel)
        if outputFiles:
            filesToOpen.extend(outputFiles)

    return filesToOpen
