import os
import time
import json
import IO_libraries_util
import IO_files_util
import pandas as pd
from pycorenlp import StanfordCoreNLP
import logging
import reminders_util

# Set up logger for error and process tracking
logger = logging.getLogger(__name__)

def CoreNLP_annotate(config_filename, inputFilename, inputDir, outputDir, openOutputFiles, chartPackage, dataTransformation, annotator_params, DoCleanXML, language, export_json_var=0, memory_var=6, document_length=90000, sentence_length=1000, silent=False, filter_subjects=False, **kwargs):
    
    # Validate memory and length defaults
    if memory_var < 4:
        memory_var = 4
    if document_length < 50000:
        document_length = 90000
    if sentence_length < 50:
        sentence_length = 100

    filesToOpen = []
    start_time = time.time()

    # Check if the selected language is supported by CoreNLP
    available_language = check_CoreNLP_available_languages(language)
    if not available_language:
        logger.error(f"Language {language} is not supported.")
        return filesToOpen

    # Check if the selected annotator is available for the given language
    annotator_available = check_CoreNLP_annotator_availability(config_filename, annotator_params, language)
    if not annotator_available:
        logger.error(f"Annotator {annotator_params} is not available for {language}.")
        return filesToOpen

    # Set up CoreNLP directory
    CoreNLPdir, _, errorFound = IO_libraries_util.external_software_install('Stanford_CoreNLP_util', 'Stanford CoreNLP', '', silent=silent, errorFound=False)
    if not CoreNLPdir:
        logger.error("Stanford CoreNLP installation not found.")
        return filesToOpen

    # Check for Java installation
    errorFound, _, _, java_version = IO_libraries_util.check_java_installation('Stanford CoreNLP')
    if errorFound:
        logger.error("Java installation not found or incompatible.")
        return filesToOpen

    # Check available memory
    IO_libraries_util.check_avaialable_memory('Stanford CoreNLP')

    # Process input files
    inputDocs = IO_files_util.getFileList(inputFilename, inputDir, fileType='.txt', silent=False, configFileName=config_filename)
    nDocs = len(inputDocs)
    if nDocs == 0:
        logger.error("No input files found.")
        return filesToOpen

    logger.info(f"Starting CoreNLP annotation for {nDocs} files.")

    # Setup CoreNLP server
    nlp = StanfordCoreNLP('http://localhost:9000')
    
    # Iterate over input files
    for doc in inputDocs:
        docID = inputDocs.index(doc) + 1
        head, tail = os.path.split(doc)
        logger.info(f"Processing file {docID}/{nDocs}: {tail}")

        # Read the file
        try:
            with open(doc, 'r', encoding='utf-8') as file:
                text = file.read().replace("\n", " ")
        except Exception as e:
            logger.error(f"Error reading file {doc}: {e}")
            continue

        # Handle percent signs (optional reminder)
        if "%" in text:
            logger.warning("Found '%' in the text, replacing it with 'percent'.")
            text = text.replace("%", "percent")

        # Prepare CoreNLP parameters
        params = {
            'annotators': ','.join(annotator_params),
            'outputFormat': 'json',
            'timeout': '999999',
            'parse.maxlen': str(sentence_length),
            'ner.maxlen': str(sentence_length),
            'pos.maxlen': str(sentence_length),
            'memory': f'{memory_var}g'
        }

        if language.lower() != 'english':
            params['props'] = language.lower()

        if DoCleanXML:
            params['annotators'] += ',cleanXML'

        # Annotate text using CoreNLP
        try:
            annotator_start_time = time.time()
            CoreNLP_output = nlp.annotate(text, properties=params)
            logger.info(f"Annotation completed for {tail} in {time.time() - annotator_start_time:.2f} seconds.")
        except Exception as e:
            logger.error(f"Error during CoreNLP annotation for {tail}: {e}")
            continue

        # Process CoreNLP output and save results
        try:
            outputFilename = os.path.join(outputDir, f"{os.path.splitext(tail)[0]}_CoreNLP_output.json")
            with open(outputFilename, 'w', encoding='utf-8') as f:
                json.dump(CoreNLP_output, f, ensure_ascii=False, indent=4)
            filesToOpen.append(outputFilename)
            logger.info(f"Saved CoreNLP output to {outputFilename}.")
        except Exception as e:
            logger.error(f"Error saving CoreNLP output for {tail}: {e}")

        # Optionally generate CSV outputs or visualizations
        if openOutputFiles:
            generate_csv_output(CoreNLP_output, outputDir, tail, filesToOpen)

    # End the CoreNLP server process
    nlp.kill()

    # Log completion
    logger.info(f"Completed CoreNLP annotation for all files in {time.time() - start_time:.2f} seconds.")

    return filesToOpen

 
available_languages = [
    "Arabic",
    "Chinese",
    "English",
    "French",
    "German",
    "Hungarian",
    "Italian",
    "Spanish",
    ]

available_coreference = [
    # "Arabic",
    "Chinese",
    "English",
    # "French",
    # "German",
    # "Hungarian",
    # "Italian",
    # "Spanish",
    ]

url = 'https://stanfordnlp.github.io/CoreNLP/human-languages.html'       
CoreNLP_web = '\n\nLanguage and annotator options for Stanford CoreNLP are listed at the Stanford CoreNLP website\n\n' + url

def generate_csv_output(CoreNLP_output, outputDir, tail, filesToOpen):
    """
    Optional function to process CoreNLP JSON output into a CSV.
    """
    try:
        # Example: Extracting Named Entities and saving to CSV
        entities = []
        for sentence in CoreNLP_output['sentences']:
            for entity in sentence['entitymentions']:
                entities.append({
                    'Text': entity['text'],
                    'NER': entity['ner'],
                    'Sentence': sentence['index']
                })

        output_csv = os.path.join(outputDir, f"{os.path.splitext(tail)[0]}_NER.csv")
        df = pd.DataFrame(entities)
        df.to_csv(output_csv, index=False)
        filesToOpen.append(output_csv)
        logger.info(f"Saved NER data to {output_csv}.")
    except Exception as e:
        logger.error(f"Error generating CSV output: {e}")
        


def check_CoreNLP_available_languages(language):
    """
    Check if the given language is supported by Stanford CoreNLP.
    """
    available_language = True
    if language not in available_languages:
        available_language = False
        website_name = 'CoreNLP website'
        message_title = 'CoreNLP Language Availability'
        message = (f"{language} is not available in Stanford CoreNLP.\n\n"
                   f"Available languages are: {', '.join(available_languages)}.\n\n"
                   "You can change the selected language using the Setup dropdown menu "
                   "or visit the CoreNLP website for more information.")
        logger.warning(message)
        IO_libraries_util.open_url(website_name, CoreNLP_web, ask_to_open=True, message_title=message_title, message=message)
    return available_language


def check_CoreNLP_annotator_availability(config_filename, annotator, language):
    """
    Check if the selected annotator is available for the given language in CoreNLP.
    """
    not_available = False

    if "lemma" in annotator and language != 'English':
        not_available = True
    elif "normalized" in annotator and language != 'English':
        not_available = True
    elif "gender" in annotator and language != 'English':
        not_available = True
    elif "quote" in annotator and language != 'English':
        not_available = True
    elif "OpenIE" in annotator and language != 'English':
        not_available = True
    elif "sentiment" in annotator and language not in ['English', 'Chinese']:
        not_available = True
    elif "coreference" in annotator and language not in ['English', 'Chinese']:
        not_available = True
    elif "PCFG" in annotator and language not in ['English', 'German']:
        not_available = True
    elif "neural network" in annotator and language in ['Arabic', 'Hungarian']:
        not_available = True
    elif "SVO" in annotator and language in ['Arabic', 'Hungarian']:
        not_available = True

    if not_available:
        logger.warning(f"{annotator.upper()} annotator is not available for {language}.")
        reminder_status = reminders_util.checkReminder(__file__,
                                                       reminders_util.title_options_CoreNLP_website,
                                                       reminders_util.message_CoreNLP_website,
                                                       True)
        if reminder_status == 'Yes' or reminder_status == 'ON':
            website_name = 'CoreNLP website'
            message_title = 'CoreNLP Annotator Availability'
            message = ("Would you like to open the Stanford CoreNLP website "
                       "for more information about annotator availability?")
            IO_libraries_util.open_url(website_name, CoreNLP_web, ask_to_open=True, message_title=message_title, message=message)

    return not not_available