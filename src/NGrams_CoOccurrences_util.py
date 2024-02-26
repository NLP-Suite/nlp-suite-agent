# written by Rafael Piloto October 2021
# re-written by Roberto Franzosi October 2021
# completed by Austin Cai October 2021

import os
import tkinter.messagebox as mb
import pandas as pd
import csv
import numpy as np
import pprint
# from Stanza_functions_util import word_tokenize_stanza, sent_tokenize_stanza, lemmatize_stanza
import stanza

import GUI_util
import IO_files_util
import IO_csv_util
import IO_user_interface_util
import constants_util

"""
NGramsCoOccurrences implements the ability to generate NGram and CoOccurrences data
"""
import hashfile
from Stanza_functions_util import stanzaPipeLine, word_tokenize_stanza, sent_tokenize_stanza, lemmatize_stanza
def is_subset(A, B):
    A = ' '.join(A).split(' ')
    return all(element in B for element in A)

def one_text_res(sentences, targets, doc_index, doc_name):
    results = []
    for sent in sentences:
        if is_subset(targets, word_tokenize_stanza(stanzaPipeLine(sent))):
            results.append((sent, sentences.index(sent), doc_index, doc_name))
    return pd.DataFrame(results, columns=['Sentence', 'Sentence ID',
                                          'Document ID', 'Document'])

def readfile(doc):
    with open(doc, "r", encoding="utf-8", errors="ignore") as f:
        fullText = f.read()
        fullText = fullText.replace('\n', ' ')
    return fullText
def get_all_dataframe_for_sentence_cooccur(inputFilename, inputDir, targets,
                                           configFileName, outputDir):
    outputFilename = IO_files_util.generate_output_file_name(inputFilename, inputDir, outputDir, '.csv', 'Stanza',
                                                             'Co-occurrence_within_sentence')
    files = IO_files_util.getFileList(inputFilename, inputDir,
                                      '.txt', silent=False, configFileName=configFileName)
    o2 = os.path.dirname(outputDir+"Sentence")
    hashmap = hashfile.getcache(o2) if hashfile.checkOut(o2) else {}
    all_results = pd.DataFrame() # Initialize an empty DataFrame to store all results
    for index, file in enumerate(files):
        checksum = hashfile.calculate_checksum(file)
        head, tail = os.path.split(file)
        if checksum in hashmap:
            sentences = hashmap[checksum]
            print(f" cache auto:  Processing file {index + 1}/{len(files)} {tail}")
        else:
            print(f" producing cache:  Processing file {index + 1}/{len(files)} {tail}")
            sentences = sent_tokenize_stanza(stanzaPipeLine(readfile(file)))
            hashfile.storehash(hashmap, checksum, sentences)
            hashfile.writehash(hashmap, o2)
        df = one_text_res(sentences, targets, index, IO_csv_util.dressFilenameForCSVHyperlink(file))
        all_results = pd.concat([all_results, df]) # Append the results to the all_results DataFrame
    all_results.to_csv(outputFilename,index=False)
    # print("Generation complete. Done!")
    return outputFilename

def processSearchWords(inputStr):
    word_list = []
    if inputStr.find("\"") == -1:
        # no quotation mark
        word_list += inputStr.split(",")
    else:
        # contains quotation mark
        curWord = ""
        i = 0
        while i < len(inputStr):
            if inputStr[i] == ",":
                if curWord != "":
                    word_list.append(curWord)
                curWord = ""
            elif inputStr[i] == "\"":
                endIndex = inputStr.index("\"", i + 1)
                word_list.append(inputStr[i + 1: endIndex])
                i = endIndex
            else:
                curWord = curWord + inputStr[i]
            i += 1
    return word_list


def process_date(search_wordsLists, temporal_aggregation):
    # it will iterate through i = 0, 1, 2, …., n-1
    # this assumes the data are in this format: temporal_aggregation, frequency of search-word_1, frequency of search-word_2, ...
    i = 0
    j = 0
    columns_to_be_plotted_yAxis = []
    ngram_list = processSearchWords(search_wordsLists)
    ngram_list = ['-checkNGrams'] + ngram_list
    while i < (len(ngram_list) - 1):
        if temporal_aggregation == "quarter" or temporal_aggregation == "month":
            if i == 0:
                j = j + 3
            columns_to_be_plotted_yAxis.append([0, j])
        else:
            columns_to_be_plotted_yAxis.append([0, i + 1])
        i += 1
        j += 1
    return columns_to_be_plotted_yAxis


def aggregate_by_number_of_years(yearList, byNumberOfYears, search_word_list):
    # pprint.pprint(ngram_results)
    curYear = yearList[0]
    newYear = curYear + byNumberOfYears - 1
    newYearStringList = []
    newYearIntList = []
    ngram_results = {}

    while curYear < yearList[-1]:
        yearChunk = str(curYear) + "-" + str(newYear)
        newYearStringList.append(yearChunk)
        newYearIntList.append((curYear, newYear))
        curYear = newYear + 1
        newYear = curYear + byNumberOfYears - 1
    aggregated_ngram_results = {}
    for word in search_word_list:
        aggregated_ngram_results[word] = {}
        for y in newYearStringList:
            aggregated_ngram_results[word][y] = {"Search Word(s)": word,
                                                 "Frequency": 0}
        for year in yearList:
            for i in range(len(newYearIntList)):
                if newYearIntList[i][0] <= year <= newYearIntList[i][1]:
                    aggregated_ngram_results[word][newYearStringList[i]]["Frequency"] += \
                        ngram_results[word][year]["Frequency"]
    ngram_results = aggregated_ngram_results
    return ngram_results


def process_n_grams(search_word, ngram_results, quarter_ngram_results, year, month,
                    byNumberOfYears, byYear, byMonth, byQuarter, yearList):
    if byNumberOfYears > 1:
        ngram_results = aggregate_by_number_of_years(yearList, byNumberOfYears, search_word)
    if byYear:
        ngram_results[search_word][year]["Frequency"] += 1
    if byMonth:
        ngram_results[search_word][str(year)][str(month).zfill(2)]["Frequency"] += 1
    if byQuarter:
        for word, yearDict in ngram_results.items():
            for year_template, monthDict in yearDict.items():
                q1Sum, q2Sum, q3Sum, q4Sum = 0, 0, 0, 0
                for month_template, freqDict in monthDict.items():
                    if 1 <= int(month_template) <= 3 and month == int(month_template):
                        q1Sum += 1  # freqDict["Frequency"]
                    if 4 <= int(month_template) <= 6 and month == int(month_template):
                        q2Sum += 1  # freqDict["Frequency"]
                    if 7 <= int(month_template) <= 9 and month == int(month_template):
                        q3Sum += 1  # freqDict["Frequency"]
                    if 10 <= int(month_template) <= 12 and month == int(month_template):
                        q4Sum += 1  # freqDict["Frequency"]
                quarter_ngram_results[word][year]["quarter 1"] = {"Search Word(s)": word,
                                                                  "Frequency": q1Sum}
                quarter_ngram_results[word][year]["quarter 2"] = {"Search Word(s)": word,
                                                                  "Frequency": q2Sum}
                quarter_ngram_results[word][year]["quarter 3"] = {"Search Word(s)": word,
                                                                  "Frequency": q3Sum}
                quarter_ngram_results[word][year]["quarter 4"] = {"Search Word(s)": word,
                                                                  "Frequency": q4Sum}
    return ngram_results, quarter_ngram_results


# def process_coOcc(file, search_word, search_word_list, coOcc_results):
#     return
   # co_occurrence_checker = True
   # co_occurrence_checker = True
   # for word in search_word_list:
   #     if word not in list(coOcc_results.items())[0][1]['Search Word(s)']:  # list(coOcc_results.items())[1]:
   #         co_occurrence_checker = False
    #        break
   # if co_occurrence_checker:
   #     coOcc_results[search_word] = 1
   #     co_occurrence_checker = True
   #     coOcc_results[file]["Co-Occurrence"] = "YES"

    # return coOcc_results, co_occurrence_checker


def process_word_search(file, n_grams_viewer, CoOcc_Viewer, tokens_, search_word_list,
                        ngram_results, quarter_ngram_results, coOcc_results, year, month,
                        byNumberOfYears, byYear, byMonth, byQuarter, yearList):
    for collocationIndex in range(len(tokens_)):
        token = tokens_[collocationIndex]
        for search_word in search_word_list:
            # splitting searched multi-word expressions, such as Hong Kong, Australian author, beautiful young princess

            iterations = search_word.count(' ')
            split_search_word = search_word.split(' ')
            length_of_search_list = len(split_search_word)
            checker = False
            if iterations > 0:
                for i in range(length_of_search_list):
                    if i == 0:
                        if split_search_word[i] == token:
                            checker = True
                    else:
                        if checker and (collocationIndex + i) < len(tokens_):
                            if split_search_word[i] == tokens_[collocationIndex + i]:
                                checker = True
                            else:
                                checker = False
                                break
                if checker and CoOcc_Viewer:
                    coOcc_results[file]['Co-Occurrence'][search_word] += 1
                if n_grams_viewer and checker:
                    ngram_results, quarter_ngram_results = process_n_grams(search_word, ngram_results,
                                                                           quarter_ngram_results, year, month,
                                                                           byNumberOfYears, byYear, byMonth, byQuarter,
                                                                           yearList)

            else:
                if search_word == token:
                    # for now the date option only applies to n-grams but there is no reason to exclude co-occurrences
                    # if dateOption:
                    if n_grams_viewer:
                        ngram_results, quarter_ngram_results = process_n_grams(search_word, ngram_results,
                                                                               quarter_ngram_results, year, month,
                                                                               byNumberOfYears, byYear, byMonth,
                                                                               byQuarter, yearList)

                    if CoOcc_Viewer:
                        coOcc_results[file]['Co-Occurrence'][search_word]+=1
                        #coOcc_results, co_occurrence_checker = process_coOcc(file, search_word, search_word_list,
                        #                                                     coOcc_results)
                        # do not skip the next record when running both n-grams and coOcc
                        #if co_occurrence_checker and not n_grams_viewer:
                        #    break
    if CoOcc_Viewer: #failed to consider this fact.... let's first make it work...
        valuescheck = coOcc_results[file]['Co-Occurrence'].values()
        if 0 in valuescheck:
            coOcc_results[file]['Co-Occurrence-bool']="NO"
        else:
            coOcc_results[file]['Co-Occurrence-bool'] = "YES"
    return ngram_results, quarter_ngram_results, coOcc_results


def NGrams_search_VIEWER(inputDir="relative_path_here",
        outputDir="relative_path_here",
        configFileName='',
         chartPackage='Excel', dataTransformation='No transformation',
        n_grams_viewer=False,
        CoOcc_Viewer=True,
        search_wordsLists=None,
        minus_K_words_var=0,
        plus_K_words_var=0,
        language_list=['English'],
        useLemma=False,
        dateOption=False,
        temporal_aggregation='year',
        number_of_years=0,
        dateFormat="mm-dd-yyyy",
        itemsDelimiter="_",
        datePos=2,
        viewer_options_list=[],ngrams_size=1,Ngrams_search_var=False,csv_file_var=None):

    if n_grams_viewer or CoOcc_Viewer:
        # create a subdirectory of the output directory
        outputDir = IO_files_util.make_output_subdirectory('', inputDir, outputDir, label='N-grams VIEWER',
                                                           silent=False)
        if outputDir == '':
            return
    else:
        # create a subdirectory of the output directory
        outputDir = IO_files_util.make_output_subdirectory(csv_file_var, inputDir, outputDir, label='search_N-grams',
                                                           silent=False)
        if outputDir == '':
            return


    startTime = IO_user_interface_util.timed_alert(GUI_util.window, 3000, 'N-Grams start',
                                                   'Started running Words/Characters N-Grams at',
                                                   True, '', True, '', False)

    from Stanza_functions_util import word_tokenize_stanza, sent_tokenize_stanza, lemmatize_stanza

    if search_wordsLists is None:
        search_wordsLists = []
    checkCoOccList = False

    lang_dict = dict(constants_util.languages)
    lang = ''
    lang_list = []
    for k, v in lang_dict.items():
        if v == language_list[0]:
            lang = k
            lang_list.append(lang)
            break
    try:
        if useLemma:
            stanzaPipeLine = stanza.Pipeline(lang=lang, processors='tokenize, lemma')
        else:
            stanzaPipeLine = stanza.Pipeline(lang=lang, processors='tokenize')
    except:
        mb.showwarning(title='Warning',
                       message='You must enter an integer value. The value ' + str(result[0]) + ' is not an integer.')
        return
    case_sensitive = False
    normalize = False
    scaleData = False
    useLemma = False
    fullInfo = False
    # print(str(viewer_options_list))
    if 'sensitive' in str(viewer_options_list):
        case_sensitive = True
    if 'insensitive' in str(viewer_options_list):
        case_sensitive = False
    if 'Normalize' in str(viewer_options_list):
        normalize = True
    if 'Scale' in str(viewer_options_list):
        scaleData = True
    if 'Lemmatize' in str(viewer_options_list):
        useLemma = True

    byNumberOfYears = 0
    byYear = False
    byQuarter = False
    byMonth = False

    if dateOption:
        if temporal_aggregation == 'group of years':
            byNumberOfYears = number_of_years  # number of years in one aggregated chunk
            byYear = True  # set to True if aggregating by years
            aggregateBy = 'year'
        elif temporal_aggregation == 'year':
            byYear = True  # set to True if aggregating by years
            aggregateBy = 'year'
        elif temporal_aggregation == 'quarter':
            byQuarter = True  # set to True if aggregating by years
            aggregateBy = 'quarter'
        elif temporal_aggregation == 'month':
            byMonth = True  # set to True if aggregating by years
            aggregateBy = 'month'
    else:
        aggregateBy = ''
        temporal_aggregation = ''

    inputDocs = IO_files_util.getFileList('', inputDir, ".txt", silent=False,
                                      configFileName=configFileName)  # get all input files
    nDocs=len(inputDocs)
    if nDocs==0:
        return


    import IO_string_util
    search_keywords_str, search_keywords_list = IO_string_util.process_comma_separated_string_list(search_wordsLists,
                                                                                                   case_sensitive)

    original_search_word = search_keywords_str
    _results = {}
    yearList = []
    docIndex = 1

    # collect date info
    if dateOption:
        print("\nProcessing files collecting date information\n")
        for file in inputDocs:  # iterate over each file
            head, tail = os.path.split(file)
            print("Processing file " + str(docIndex) + "/" + str(nDocs) + ' ' + tail)
            docIndex += 1
            date, dateStr, month, day, year = IO_files_util.getDateFromFileName(file, dateFormat, itemsDelimiter,
                                                                                datePos)
            yearList.append(year)
            yearList = sorted(np.unique(yearList))

    # coOcc_results are initialized below because this dictionary needs the filename
    ngram_results = {}
    quarter_ngram_results = {}
    coOcc_results = {}


    # iterate over each file, searching for words
    print("\nProcessing files for search words\n")
    docIndex = 0

    #########NEW FILE##########
    import hashfile
    if hashfile.checkOut(outputDir):
        hashmap = hashfile.getcache(outputDir)
    else:
        hashmap = {}

    def transform(ngram):
        return ' '.join(ngram.split(' ')[:-1])

    def extract_context(ngram_str, target_phrase, minus_K_words_var, plus_K_words_var):
        words = ngram_str.split(' ')
        # Create a list of words in the target_phrase
        target_words = target_phrase.split(' ')
        target_length = len(target_words)

        # Find the start index of the phrase
        for i in range(len(words) - target_length + 1):
            if words[i:i + target_length] == target_words:
                target_index = i
                break
        else:
            # The target_phrase is not found in the ngram_str
            return None, None

        # Calculate context indices
        start_index = max(target_index - minus_K_words_var, 0)  # Ensure the start index isn't negative.
        end_index = min(target_index + target_length + plus_K_words_var,
                        len(words))  # Ensure the end index doesn't exceed the length of the list.

        # Get words before and after the target phrase
        words_before = words[start_index:target_index]
        words_after = words[target_index + target_length:end_index]

        # Join the context words back into strings
        context_before = ' '.join(words_before)
        context_after = ' '.join(words_after)

        return context_before, context_after

    def is_word_in_custom_range(ngram, word, minus_K_words_var, plus_K_words_var):
        words = ngram.split(' ')
        start_index = minus_K_words_var # you need abs() if the minus is a negative value, i don't know the design, yet
        end_index = len(words) - plus_K_words_var
        subrange = words[start_index:end_index]  # Extract the subrange
        return word in ' '.join(subrange) # Check if the word is within the subrange.

    def process_ngrams(data, word, minus_K_words_var, plus_K_words_var):
        column_name = data.columns[0]
        ngram_size = int(column_name.split('-')[0])  # Extracting the size of the n-gram from the column name
        filtered_data = data[data[column_name].apply(lambda x: is_word_in_custom_range(x, word, minus_K_words_var, plus_K_words_var))].copy()
        initial_filter_data = filtered_data.copy()
        if filtered_data.empty:
            print("No data rows with the specified conditions.")
            return None  # or handle it as appropriate for your use case
        if ngram_size in [1, 2]:
            filtered_data['Search word'] = filtered_data[column_name].apply(transform)
            filtered_data['Co-Occurring word'] = word
        else:
            filtered_data['Words to the left'], filtered_data['Words to the right'] = zip(
                *filtered_data[column_name].apply(
                    lambda x: extract_context(x, word, minus_K_words_var, plus_K_words_var)))
            filtered_data['Search word'] = word
        return initial_filter_data,filtered_data

    # search n-gram file --------------------------------------------------------------------

    search_words = []
    if Ngrams_search_var:
        filesToOpen=[]
        if csv_file_var is None:
            print("empty csv file, do again, this ought not to happen?!")
            return
        data = pd.read_csv(csv_file_var)
        if 'gram' not in data.columns[0]:
            mb.showwarning(title='Input file error',
                           message='The selected csv file is not the expected csv N-grams file.\n\nThis file should contain a header with the word "gram".\n\nPlease, select the expected csv file and try again.')
            return

        # Check the input parameters, i comment it out for now because we don't know the design
        if minus_K_words_var < 0 or plus_K_words_var < 0 or (minus_K_words_var + plus_K_words_var) > int(data.columns[0][0]) - 1:
            mb.showwarning(title='Warning',
                           message='The sum of -K and +K values should be < than the n-grams value (so, a 4-ngrams can only have a combination of -K + K values less or equal to 3).\n\nThe n-grams value in your input csv file is ' + str(data.columns[0][0]) + '.')
            return

        words = search_keywords_list
        l = []
        l_sankey = []
        for word in words:
            try:
                b, df2 = process_ngrams(data, word, minus_K_words_var, plus_K_words_var)
            except:
                mb.showwarning(title='Warning',message='The selected input file does not contain the word "' + word +'".')
                return
            expanded_rows = []
            for _, row in df2.iterrows():
                new_row = row.copy()
                num_repetitions = int(row['Frequency in Document'])
                for _ in range(num_repetitions):
                    expanded_rows.append(new_row)
            expanded_df = pd.DataFrame(expanded_rows)
            l_sankey.append(expanded_df)
            pivot_df = b.pivot_table(
                values='Frequency in Document',  # fill with frequencies
                index='Document ID',  # rows are documents
                columns=data.columns[0],  # columns are 2-grams
                fill_value=0,  # fill missing values with 0
                aggfunc='sum')  # use sum to aggregate entries
            all_document_ids = range(min(data['Document ID']), max(
                data['Document ID']) + 1)  # Replace with the actual range or list of your document IDs
            pivot_df = pivot_df.reindex(all_document_ids, fill_value=0)
            l.append(pivot_df)
        combined_pivot_df = pd.concat(l, axis=1)
        combined_saneky_df = pd.concat(l_sankey)
        a_to_b_mapping = data.drop_duplicates(subset='Document ID').set_index('Document ID')['Document'].to_dict()
        combined_pivot_df['Document ID'] = combined_pivot_df.index
        combined_pivot_df['Document'] = combined_pivot_df.index.map(a_to_b_mapping)
        # combined_pivot_df.insert(len(combined_pivot_df.columns)-1, 'Document ID', combined_pivot_df['Document ID'])
        NgramsSearchFileName = IO_files_util.generate_output_file_name('', inputDir, outputDir, '.csv',
                                                                 'N-grams_search')

        # Check if the combined DataFrame is empty
        if l_sankey[0].empty:
            mb.showwarning(title='Warning',
                           message='There are no instances of your search word(s) in the selected input file')
            return
        combined_pivot_df.to_csv(NgramsSearchFileName, index=False)

        if chartPackage!='No charts':
            inputFilename = NgramsSearchFileName
            ngram_size = int(data.columns[0].split('-')[0])
            if ngram_size==1:
                # inputFilename=outputFilename_byDocument
                # these variables are used in charts_util.visualize_chart
                headers = IO_csv_util.get_csvfile_headers(inputFilename)
                groupBy = []
                X_axis_label = ''
                if 'Date' in headers:
                    X_axis_label = 'Date'
                    groupBy = ['Date']
                else:
                    if 'Document' in headers:
                        X_axis_label = 'Document'
                        groupBy = ['Document']
                doc_pos = IO_csv_util.get_columnNumber_from_headerValue(headers, X_axis_label, inputFilename)

                columns_to_be_plotted_yAxis=[]
                title_string=''
                for word in words:
                    title_string = title_string + word + ', '
                    word_pos = IO_csv_util.get_columnNumber_from_headerValue(headers, word, inputFilename)
                    columns_to_be_plotted_yAxis.append([doc_pos, word_pos])
                # remove last ,
                title_string=title_string.rstrip()[:-1]
                import charts_util
                outputFiles = charts_util.run_all(columns_to_be_plotted_yAxis, inputFilename, outputDir,
                                                  outputFileLabel='search',
                                                  chartPackage=chartPackage,
                                                  dataTransformation=dataTransformation,
                                                  chart_type_list=['line'],
                                                  chart_title='Frequency Distribution of Search Word(s) by ' + X_axis_label + '\n' + title_string,
                                                  hover_info_column_list=[],
                                                  column_xAxis_label_var=X_axis_label,
                                                  count_var=0)

                if outputFiles != None:
                    if isinstance(outputFiles, str):
                        filesToOpen.append(outputFiles)
                    else:
                        filesToOpen.extend(outputFiles)

                return filesToOpen

            else:
                NgramsSearchFileName_Sankey = IO_files_util.generate_output_file_name('', inputDir, outputDir,
                                                                                      '_Sankey.csv',
                                                                                      'N-grams_search')
                NgramsSearchFileName_txt = IO_files_util.generate_output_file_name('', inputDir, outputDir,
                                                                                      '_frequencies.txt',
                                                                                      'N-grams_search')
                combined_saneky_df.to_csv(NgramsSearchFileName_Sankey, index=False)
                combined_saneky_df[combined_saneky_df.columns[0]].to_csv(NgramsSearchFileName_txt,index = False)

                with open(NgramsSearchFileName_txt, 'r', encoding='utf-8', errors='ignore') as f:
                    q = f.read()
                for word in search_keywords_list:
                    q = q.replace(word, '')
                    print(q, word)
                with open(NgramsSearchFileName_txt, 'w', encoding='utf-8') as f:
                    f.write(q)

                use_contour_only = False
                max_words = 100
                font = 'Default'
                prefer_horizontal = .9
                lemmatize = False
                exclude_stopwords = True
                exclude_punctuation = True
                lowercase = False
                differentPOS_differentColors = False
                differentColumns_differentColors = False
                csvField_color_list = []
                doNotListIndividualFiles = True
                collocation = False
                import wordclouds_util
                outputFiles2 = wordclouds_util.python_wordCloud(NgramsSearchFileName_txt, '', outputDir, configFileName,
                                                                selectedImage="",
                                                                use_contour_only=use_contour_only,
                                                                prefer_horizontal=prefer_horizontal, font=font,
                                                                max_words=max_words,
                                                                lemmatize=lemmatize,
                                                                exclude_stopwords=exclude_stopwords,
                                                                exclude_punctuation=exclude_punctuation,
                                                                lowercase=lowercase,
                                                                differentPOS_differentColors=differentPOS_differentColors,
                                                                differentColumns_differentColors=differentColumns_differentColors,
                                                                csvField_color_list=csvField_color_list,
                                                                doNotListIndividualFiles=doNotListIndividualFiles,
                                                                openOutputFiles=False, collocation=collocation)
                filesToOpen.extend(outputFiles2)
                import charts_util
                headers=IO_csv_util.get_csvfile_headers(NgramsSearchFileName_Sankey)
                Sankey_limit1_var=30
                Sankey_limit2_var=30
                Sankey_limit3_var=30
                output_label = ''

                outputFilename = IO_files_util.generate_output_file_name(NgramsSearchFileName_Sankey, inputDir, outputDir,
                                                                         '.html', output_label)
                if ngram_size==2:
                    three_way_Sankey = False
                    var3 = None
                    Sankey_limit3_var = None
                    Sankey_chart = charts_util.Sankey(NgramsSearchFileName_Sankey, outputFilename,
                                                      'Search word', Sankey_limit1_var, 'Co-Occurring word',
                                                      Sankey_limit2_var, three_way_Sankey, var3, Sankey_limit3_var)
                    filesToOpen.extend([NgramsSearchFileName, NgramsSearchFileName_Sankey, Sankey_chart])
                elif plus_K_words_var==0:
                    three_way_Sankey = False
                    var3 = None
                    Sankey_limit3_var = None
                    Sankey_chart = charts_util.Sankey(NgramsSearchFileName_Sankey, outputFilename,
                                                      'Search word', Sankey_limit1_var, 'Words to the left',
                                                      Sankey_limit2_var, three_way_Sankey, var3, Sankey_limit3_var)
                    filesToOpen.extend([NgramsSearchFileName, NgramsSearchFileName_Sankey, Sankey_chart])
                elif minus_K_words_var==0:
                    three_way_Sankey = False
                    var3 = None
                    Sankey_limit3_var = None
                    Sankey_chart = charts_util.Sankey(NgramsSearchFileName_Sankey, outputFilename,
                                                      'Search word', Sankey_limit1_var, 'Words to the right',
                                                      Sankey_limit2_var, three_way_Sankey, var3, Sankey_limit3_var)
                    filesToOpen.extend([NgramsSearchFileName, NgramsSearchFileName_Sankey, Sankey_chart])
                else:
                    three_way_Sankey = True
                    Sankey_chart=charts_util.Sankey(NgramsSearchFileName_Sankey, outputFilename,
                                       'Words to the left', Sankey_limit1_var, 'Words to the right',
                                       Sankey_limit2_var, 0, "Search word", Sankey_limit3_var)
                    filesToOpen.extend([NgramsSearchFileName, NgramsSearchFileName_Sankey, Sankey_chart])
                    pass

        return filesToOpen

    if n_grams_viewer:
        # initialize the ngram_results dictionary ------------------------------------------------------
        quarter_ngram_results = {}
        for word in search_keywords_list:
            ngram_results[word] = {}
            quarter_ngram_results[word] = {}
            for y in yearList:
                if byYear:
                    ngram_results[word][y] = {"Search Word(s)": word,
                                              "Frequency": 0}
                if byQuarter:
                    quarter_ngram_results[word][y] = {}
                    q1Sum, q2Sum, q3Sum, q4Sum = 0, 0, 0, 0
                    quarter_ngram_results[word][y]["quarter 1"] = {"Search Word(s)": word,
                                                                   "Frequency": 0}
                    quarter_ngram_results[word][y]["quarter 2"] = {"Search Word(s)": word,
                                                                   "Frequency": 0}
                    quarter_ngram_results[word][y]["quarter 3"] = {"Search Word(s)": word,
                                                                   "Frequency": 0}
                    quarter_ngram_results[word][y]["quarter 4"] = {"Search Word(s)": word,
                                                                   "Frequency": 0}

                if byMonth or byQuarter:
                    monthList = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
                    ngram_results[word][str(y)] = {}
                    for m in monthList:
                        ngram_results[word][str(y)][m] = {"Search Word(s)": word,
                                                          "Frequency": 0}



    for file in inputDocs:
        docIndex += 1
        # initialize the CoOcc_results dictionary
        if CoOcc_Viewer:
            mps = {}
            for x in search_keywords_list:
                mps[x] = 0
            coOcc_results[file] = {"Search Word(s)": original_search_word, "Co-Occurrence-bool": "", "Co-Occurrence": mps,
                                   "Document ID": docIndex,
                                   "Document": IO_csv_util.undressFilenameForCSVHyperlink(file)}
        head, tail = os.path.split(file)
        print("Processing file " + str(docIndex) + "/" + str(nDocs) + ' ' + tail)
        # extract the date from the file name
        date, dateStr, month, day, year = IO_files_util.getDateFromFileName(file, dateFormat, itemsDelimiter, datePos)
        if date == '':
            pass# TODO: getDate warns user is this file has a bad date

###########################################################
        if hashfile.calculate_checksum(file) in hashmap:
            tokens_ = hashmap[hashfile.calculate_checksum(file)]
        else:
            f = open(file, "r", encoding='utf-8', errors='ignore')
            docText = f.read()
            f.close()
            if not case_sensitive:
                docText = docText.lower()
            tokens_ = word_tokenize_stanza(stanzaPipeLine(docText))
            hashfile.storehash(hashmap, hashfile.calculate_checksum(file), tokens_)
            hashfile.writehash(hashmap, outputDir)
############################################################
        ngram_results, quarter_ngram_results, coOcc_results = process_word_search(file,
                                                                                  n_grams_viewer, CoOcc_Viewer,
                                                                                  tokens_, search_keywords_list,
                                                                                  ngram_results, quarter_ngram_results,
                                                                                  coOcc_results,
                                                                                  year, month,
                                                                                  byNumberOfYears, byYear, byMonth,
                                                                                  byQuarter, yearList)

    NgramsFileName = ''
    coOccFileName = ''

    if n_grams_viewer:
        if byQuarter:
            ngram_results = quarter_ngram_results

        if 'group' in temporal_aggregation:
            label = 'group_' + str(byNumberOfYears)
        else:
            label = temporal_aggregation
        NgramsFileName = IO_files_util.generate_output_file_name('', inputDir, outputDir, '.csv',
                                                                 'N-grams_' + label)

    if CoOcc_Viewer:
        coOccFileName = IO_files_util.generate_output_file_name('', inputDir, outputDir, '.csv', 'Co-Occ')

    # save the N-grams/Co-occurrence output files
    # pprint.pprint(coOcc_results)
    filesToOpen = save(NgramsFileName, coOccFileName, ngram_results, coOcc_results, aggregateBy, temporal_aggregation)

    # plot Ngrams --------------------------------------------------------------------------

    if n_grams_viewer:
        import charts_util
        if chartPackage!='No charts' and NgramsFileName != '':
            xlsxFilename = NgramsFileName
            xAxis = temporal_aggregation
            chart_title = 'N-Grams Viewer'
            columns_to_be_plotted_xAxis = []
            columns_to_be_plotted_yAxis = []
            # it will iterate through i = 0, 1, 2, …., n-1
            # this assumes the data are in this format: temporal_aggregation, frequency of search-word_1, frequency of search-word_2, ...
            i = 0
            j = 0
            columns_to_be_plotted_yAxis = process_date(search_wordsLists, temporal_aggregation)
            hover_label = []
            outputFiles = charts_util.run_all(columns_to_be_plotted_yAxis, xlsxFilename, outputDir,
                                              'n-grams_viewer',
                                              chartPackage=chartPackage,
                                              dataTransformation=dataTransformation,
                                              chart_type_list=["line"],
                                              chart_title=chart_title, column_xAxis_label_var=xAxis,
                                              hover_info_column_list=hover_label)
            if outputFiles != None:
                if isinstance(outputFiles, str):
                    filesToOpen.append(outputFiles)
                else:
                    filesToOpen.extend(outputFiles)

    # plot co-occurrences -----------------------------------------------------------------------------

    if CoOcc_Viewer:
        if chartPackage!='No charts' and coOccFileName != '':
            import charts_util
            xlsxFilename = coOccFileName
            chart_title = 'Co-Occurring Words: ' + search_wordsLists
            if dateOption == 0:
                xAxis = 'Document'
            else:
                xAxis = temporal_aggregation
            hover_label = []
            columns_to_be_plotted_byDoc = [[1, 2]]
            freq_file = aggregate_YES_NO(xlsxFilename, ["Co-Occurrence"])
            outputFiles = charts_util.run_all(columns_to_be_plotted_byDoc, freq_file, outputDir,
                                              outputFileLabel='byDoc',
                                              # outputFileNameType + 'byDoc', #outputFileLabel,
                                              chartPackage=chartPackage,
                                              dataTransformation=dataTransformation,
                                              chart_type_list=['bar'],
                                              chart_title=chart_title + '\nby Document',
                                              column_xAxis_label_var='',
                                              column_yAxis_label_var='Frequency',
                                              hover_info_column_list=hover_label,
                                              # count_var is set in the calling function
                                              #     0 for numeric fields;
                                              #     1 for non-numeric fields
                                              count_var=0,
                                              remove_hyperlinks=True)
            if outputFiles != None:
                if isinstance(outputFiles, str):
                    filesToOpen.append(outputFiles)
                else:
                    filesToOpen.extend(outputFiles)

            # chart_title = 'Co-occurrence Viewer'
            # columns_to_be_plotted_yAxis = process_date(search_wordsLists, temporal_aggregation)
            # hover_label = []
            # chart_title = 'Frequency Distribution of Co-Occurring Words'
            # outputFiles = charts_util.run_all(columns_to_be_plotted_yAxis, xlsxFilename, outputDir,
            #                                            'co-occ_viewer',
            #                                            chartPackage=chartPackage,
            #                                            dataTransformation=dataTransformation,
            #                                            chart_type_list=["bar"],
            #                                            count_var=1,
            #                                            chart_title=chart_title,
            #                                            column_xAxis_label_var='Word list: ' + search_wordsLists,
            #                                            hover_info_column_list=hover_label)
            # if outputFiles!=None:
            #     if isinstance(outputFiles, str):
            #         filesToOpen.append(outputFiles)
            #     else:
            #         filesToOpen.extend(outputFiles)

    IO_user_interface_util.timed_alert(GUI_util.window, 2000, 'Analysis end',
                                       'Finished running Words/Characters N-Grams at', True, '', True, startTime,
                                       False)

    return filesToOpen


"""
    Instead of direct aggregation by document, take YES as 1 and NO as 0, and then sum it by document.
"""


def aggregate_YES_NO(inputFilename, column):
    cols = ["Document ID", "Document"] + column
    df = pd.read_csv(inputFilename, encoding='utf-8', on_bad_lines='skip')
    df = df.replace('YES', 1)
    df = df.replace('NO', 0)
    # create a new data frame with Document ID, Document, and the sum of the column
    df = df[cols].groupby(["Document ID", "Document"]).sum()
    # rename 'column' to Frequency
    df = df.rename(columns={column[0]: "Frequency"})
    df = df.reset_index()
    # save the new data frame to a new file, parse the inputfilename and add _frequency to the end
    newFilename = inputFilename.split(".")[0] + "_frequency.csv"
    # save the new data frame to a new file
    df.to_csv(newFilename, index=False)
    _, newFilename = IO_csv_util.remove_hyperlinks(newFilename)
    return newFilename


"""
    Saves the data passed in the expected format of `NGramsCoOccurrences.run()`

    ngrams_results: dict
            The ngram results in the following format: {word : [word, date, file] }
        coOcc_results: dict
            The co-occurrence results in the following format: {combination : [combination, date, file] }
"""


def save(NgramsFileName, coOccFileName, ngram_results, coOcc_results, aggregateBy, temporal_aggregation):
    filesToOpen = []
    if len(ngram_results) > 0:
        dfList = []  # create a list of dataframes: one df for one search word
        if aggregateBy == 'year':
            for word, yearDict in ngram_results.items():
                df = pd.DataFrame(columns=[word, temporal_aggregation])
                for year, freqDict in yearDict.items():
                    df = df.append({word: freqDict["Frequency"], temporal_aggregation: year}, ignore_index=True)
                dfList.append(df)
            newdfCur = dfList[0].copy()  # let newdfCur be the first df in the dfList
            newdf = newdfCur.copy()
            for i in range(1, len(dfList)):  # one by one join next search word's dataframe with the current dataframe
                newdfNext = dfList[i].copy()  # get the next dataframe
                newdf = newdfCur.merge(newdfNext, on=temporal_aggregation, how="left")  # join on year
                newdfCur = newdf.copy()

            # these 3 lines will move the 'year' column to position 0, which is the left most position
            # inserting headers
            newdf.insert(0, 'year_temp', newdf[temporal_aggregation])
            newdf.drop(temporal_aggregation, axis=1, inplace=True)
            newdf.rename(columns={'year_temp': temporal_aggregation}, inplace=True)
        else:
            # aggregating by quarter or month
            for word, yearDict in ngram_results.items():
                df = pd.DataFrame(columns=[word, 'year', temporal_aggregation, "year-" + temporal_aggregation])
                for year, monthDict in yearDict.items():
                    for month, freqDict in monthDict.items():
                        if temporal_aggregation == 'quarter':
                            df = df.append({word: freqDict["Frequency"], "year": year, temporal_aggregation: month,
                                            "year-" + temporal_aggregation: str(year) + "-Q" + month[-1]},
                                           ignore_index=True)
                        else:
                            df = df.append({word: freqDict["Frequency"], "year": year, temporal_aggregation: month,
                                            "year-" + temporal_aggregation: str(year) + "-" + month}, ignore_index=True)
                dfList.append(df)
            newdfCur = dfList[0].copy()
            newdf = newdfCur.copy()
            for i in range(1, len(dfList)):
                newdfNext = dfList[i].copy()
                newdf = newdfCur.merge(newdfNext, on=['year', temporal_aggregation, "year-" + temporal_aggregation],
                                       how="left")
                newdfCur = newdf.copy()
            # these 9 lines will move the 'year', 'month' or 'quarter', and 'year-month' column to the left most position
            newdf.insert(0, 'month_temp', newdf[temporal_aggregation])
            newdf.insert(0, 'year_temp', newdf['year'])
            newdf.insert(0, 'yearMonth_temp', newdf["year-" + temporal_aggregation])
            newdf.drop(temporal_aggregation, axis=1, inplace=True)
            newdf.drop('year', axis=1, inplace=True)
            newdf.drop("year-" + temporal_aggregation, axis=1, inplace=True)
            newdf.rename(columns={'month_temp': temporal_aggregation}, inplace=True)
            newdf.rename(columns={'year_temp': 'year'}, inplace=True)
            newdf.rename(columns={'yearMonth_temp': 'year-' + temporal_aggregation}, inplace=True)

        if NgramsFileName != '':
            newdf.to_csv(NgramsFileName, encoding='utf-8', index=False)
            filesToOpen.append(NgramsFileName)

    if len(coOcc_results) > 0:
        # with open(os.path.join(WCOFileName, outputDir), 'w', encoding='utf-8') as f:
        with open(coOccFileName, 'w', newline='', encoding='utf-8', errors='ignore') as f:
            writer = csv.writer(f)
            line = ["Search Word(s)", "Co-Occurrence"]
            import re
            words = next(iter(coOcc_results.items()))[1]['Search Word(s)']
            line.extend([element + '_Frequency' for element in re.findall(r'[^,]+', words)])
            line.extend(["Document ID", "Document"])
            writer.writerow(line)
            for label, res in coOcc_results.items():
                if isinstance(res, dict):
                    line = [res["Search Word(s)"], res["Co-Occurrence-bool"]]
                    line.extend(list(res['Co-Occurrence'].values()))
                    line.extend([res["Document ID"],IO_csv_util.dressFilenameForCSVHyperlink(res["Document"])])
                    writer.writerow(line)
        filesToOpen.append(coOccFileName)

    return filesToOpen