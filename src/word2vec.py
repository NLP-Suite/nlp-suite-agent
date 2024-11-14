import reminders_util
import IO_files_util

# RUN section ______________________________________________________________________________________________________________________________________________________

def run_word2vec(inputFilename, inputDir, outputDir, chartPackage, dataTransformation,
                 remove_stopwords_var, lemmatize_var, WSI_var,
                 BERT_var, Gensim_var,
                 sg_menu_var, vector_size_var, window_var, min_count_var,
                 vis_menu_var, dim_menu_var, compute_distances_var, top_words_var, keywords_var,
                 keywordInput, range4, range6, range20, ngramsDropDown):

    config_filename = "NLP_default_IO_config.csv"
    scriptName = "word2vec.py"

    if not BERT_var and not Gensim_var and not WSI_var and not compute_distances_var:
        print('No option has been selected.\n\nPlease select the Word2Vec package you wish to use (BERT and/or Gensim) and try again.')
        return

    filesToOpen = []

    if not 'Do not' in vis_menu_var:
        result = print('Visualization via t-SNE: You have selected to run Word2Vec with the t-SNE visualization option ("Plot word vectors"). Depending upon the total number of words in your corpus, this option is computationally VERY demanding.')
        if not result:
            return

    label = ''
    if BERT_var:
        label = 'Word2Vec_BERT'
    elif Gensim_var:
        label = 'Word2Vec_Gensim'
    elif WSI_var:
        label = 'WSI'
    
    Word2Vec_Dir = IO_files_util.make_output_subdirectory(inputFilename, inputDir, outputDir, label=label, silent=True)
    print("Word2vec directory")
    print(Word2Vec_Dir)
    if Word2Vec_Dir == '':
        return

    # Word Sense Induction
    if WSI_var:
        
        # WSI_keywords_var = tk.StringVar()
        # WSI_keywords_var.set('')
        # WSI_keywords_lb = tk.Label(window, text='Keywords (WSI)')
        # y_multiplier_integer=GUI_IO_util.placeWidget(window,GUI_IO_util.labels_x_indented_coordinate,y_multiplier_integer,WSI_keywords_lb,True)

        # WSIdictionary_file_var=tk.StringVar() # dictionary file used to annotate
        # def get_dictionary_file(window,title,fileType):
        #     #WSIdictionary_var.set('')
        #     filePath = tk.filedialog.askopenfilename(title = title, initialdir =GUI_IO_util.namesGender_libPath, filetypes = fileType)
        #     if len(filePath)>0:
        #         # WSIdictionary_file.config(state='normal')
        #         WSI_keywords_var.set(filePath)
        
        # TODO: file upload functionality
        WSI_keywords_var = keywordInput  
        if WSI_keywords_var == '':
            print('The "Word sense induction" algorithm requires a comma-separated list of case-sensitive keywords taken from the corpus in order to run.\n\nPlease, enter the keywords and try again.')
            return

        import WSI_util, WSI_viz, WSI_keyterms

        # Load WSI data with the specified keyword list and k-means range
        all_sent, all_vocab, Word2Vec_Dir, docs, paths = WSI_util.get_data(
            inputFilename, inputDir, Word2Vec_Dir, u_vocab=WSI_keywords_var, fileType='.txt', configFileName=config_filename
        )

        # k-means range from web sliders (range4 and range6)
    
        # k_means_min_var = tk.Scale(window, from_=2, to=9, orient=tk.HORIZONTAL)
        # k_means_min_var.pack()
        # k_means_min_var.set(4)
        # TODO: add a label for K means
        k_means_min_var = int(range4) # TODO: range(2, 9)
        k_means_max_var = int(range6) # TODO: range(3, 15)
        k_range = (k_means_min_var, k_means_max_var)
        
        WSI_util.get_centroids(all_sent, all_vocab, Word2Vec_Dir, k_range)
        WSI_util.match_embeddings(all_sent, all_vocab, Word2Vec_Dir)
        s_paths = WSI_util.get_cluster_sentences(Word2Vec_Dir)
        v_paths = WSI_viz.sense_bar_chart(Word2Vec_Dir)

        # ngrams_menu_var = tk.StringVar()
        # ngrams_menu_var.set('1-grams')
        # ngrams_menu = tk.OptionMenu(window,ngrams_menu_var, '1-grams (unigrams)','2-grams (bigrams)','3-grams (trigrams)','4-grams (quadgrams)')
        ngrams_menu_var = int(ngramsDropDown.split("-")[0]) # TODO: needs to be between 1 and 4
        top_keywords_var = int(range20)  # TODO: change to between 5 to 20
        k_paths = WSI_keyterms.get_keyterms(Word2Vec_Dir, topn=top_keywords_var, ngram_range=(1, ngrams_menu_var))
        
        filesToOpen = s_paths + v_paths + k_paths

    if BERT_var:
        reminders_util.checkReminder(scriptName,
                                     reminders_util.title_options_BERT_Word2Vec_timing,
                                     reminders_util.message_BERT_Word2Vec_timing,
                                     True)
        import BERT_util
        BERT_output = BERT_util.word_embeddings_BERT(inputFilename, inputDir, Word2Vec_Dir, False, 
                                                     chartPackage, dataTransformation, vis_menu_var, dim_menu_var, compute_distances_var,
                                                     top_words_var, keywords_var, lemmatize_var, remove_stopwords_var, config_filename)
        filesToOpen.append(BERT_output)

    if Gensim_var:
        # reminders_util.checkReminder(scriptName,
        #                              reminders_util.title_options_Gensim_Word2Vec_timing,
        #                              reminders_util.message_Gensim_Word2Vec_timing,
        #                              True)
        import word2vec_Gensim_util
        Gensim_output = word2vec_Gensim_util.run_Gensim_word2vec(inputFilename, inputDir, Word2Vec_Dir, config_filename, chartPackage, dataTransformation,
                                 remove_stopwords_var, lemmatize_var,
                                 keywords_var,
                                 compute_distances_var, top_words_var,
                                 sg_menu_var, vector_size_var, window_var, min_count_var,
                                 vis_menu_var, dim_menu_var)
        filesToOpen.append(Gensim_output)


    return filesToOpen


