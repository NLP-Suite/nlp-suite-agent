# import statements
from WSI_classes import Clusterer, Matcher
import re
import numpy as np
import random
import pickle
from collections import Counter
from tqdm import tqdm
import os
tcache_path = f'{os.getcwd()}/cache'
if not os.path.exists(tcache_path):
    os.makedirs(tcache_path)
os.environ['TRANSFORMERS_CACHE'] = tcache_path

from transformers import BertModel, BertTokenizer
from collections import Counter
import spacy

import IO_files_util


SEED = 0
batch_size = 32
dropout_rate = 0.25
bert_dim = 768

alphabets = "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"
digits = "([0-9])"


def get_vocab(sentences, u_vocab='', top_n=0.01, min_count=50, add_stopwords=['said']):
    
    if u_vocab == '':
        text = ' '.join([tpl[1] for tpl in sentences]).split()
        en = spacy.load('en_core_web_sm')
        stopwords = list(en.Defaults.stop_words) + add_stopwords
        text = [w.strip() for w in text if w.strip() not in stopwords]
        u_vocab = Counter(text)
        u_vocab = [w for w, i in u_vocab.most_common(round(top_n * len(u_vocab))) \
                if u_vocab[w] >= min_count]
    else:
        u_vocab = [w.strip() for w in u_vocab.split(',')]

    return u_vocab


def split_into_sentences(text, docID):
    
    text = text.replace('--', '')
    text = " " + text + "  "
    text = text.replace("\n", " ")
    text = text.replace(",", "")
    text = text.replace(";", "")
    text = text.replace(":", "")
    text = text.replace("\"", "")
    text = re.sub(prefixes, "\\1<prd>", text)
    text = re.sub(websites, "<prd>\\1", text)
    text = re.sub(digits + "[.]" + digits, "\\1<prd>\\2", text)
    if "..." in text: text = text.replace("...", "<prd><prd><prd>")
    if "Ph.D" in text: text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] ", " \\1<prd> ", text)
    text = re.sub(acronyms + " " + starters, "\\1<stop> \\2", text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>", text)
    text = re.sub(" " + suffixes + "[.] " + starters, " \\1<stop> \\2", text)
    text = re.sub(" " + suffixes + "[.]", " \\1<prd>", text)
    text = re.sub(" " + alphabets + "[.]", " \\1<prd>", text)
    if "”" in text: text = text.replace(".”", "”.")
    if "\"" in text: text = text.replace(".\"", "\".")
    if "!" in text: text = text.replace("!\"", "\"!")
    if "?" in text: text = text.replace("?\"", "\"?")
    text = text.replace(".", "<stop>")
    text = text.replace("?", "<stop>")
    text = text.replace("!", "<stop>")
    text = text.replace("<prd>", " ")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [(i, re.sub('[^A-Za-z ]+', '', s.strip()), docID) for i, s in enumerate(sentences)]

    return sentences


def get_sent(doc, o_path):

    with open(doc, 'r', encoding='utf-8', errors='ignore') as f:
        fullText = f.read().lower()
    fullText.replace('\n', ' ')
    docID = doc.split('/')[-1]
    sentences = split_into_sentences(fullText, docID)
    with open(f'{o_path}/sentences.pickle', 'wb') as f_name:
        pickle.dump(sentences, f_name)

    return sentences, fullText


def get_data(inputFilename, inputDir, Word2Vec_Dir, u_vocab=[], fileType='.txt', configFileName=''):

    docs = {}
    vocabs = {}
    o_paths = {}
    inputDocs = IO_files_util.getFileList(inputFilename, inputDir, fileType=fileType,silent=False,configFileName=configFileName)
    all_sent = []
    all_vocab = []
    for doc in inputDocs:
        head, tail = os.path.split(doc)
        o_path = f'{Word2Vec_Dir}{os.sep}output{os.sep}{tail[:-4]}'
        if not os.path.exists(o_path):
            os.makedirs(o_path)
        sentences, fullText = get_sent(doc, o_path)
        vocab = get_vocab(sentences, u_vocab=u_vocab)
        all_sent += sentences
        all_vocab += vocab
        docs[doc] = sentences
        o_paths[doc] = o_path
    all_vocab = list(set(all_vocab))

    return all_sent, all_vocab, Word2Vec_Dir, docs, o_paths


def get_centroids(all_sent, all_vocab, Word2Vec_Dir, k_range, sample=None):

    #load model
    print('\nStarted word sense induction...\n')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
    model_name = BertModel.from_pretrained('bert-base-uncased', output_hidden_states=True)
    model = Clusterer(tokenizer, model_name)
    c_path = f'{Word2Vec_Dir}/output/centroids'
    if not os.path.exists(c_path):
        os.makedirs(c_path)
    #get centroids
    for w in tqdm(all_vocab, total=len(all_vocab), desc=f'Generating sense centroids...'):
        if sample is None:
            seq = [tpl for tpl in all_sent if w in tpl[1].split()]
        else:
            seq = random.sample([tpl for tpl in all_sent if w in tpl[1].split()], sample)
    
        if len(seq) == 0:
            print(f':-( There are no occurrences of "{w}" in the dataset. Check for misspellings and/or input other forms of the word, e.g., plural/singular forms, different tenses, etc.')
            raise ValueError(f':-( There are no occurrences of "{w}" in the dataset. Check for misspellings and/or input other forms of the word, e.g., plural/singular forms, different tenses, etc.') 
        
        batched_data, batched_words, batched_masks, batched_users = model.get_batches(seq, batch_size)
        embeddings, do_wordpiece = model.get_embeddings(batched_data, batched_words, batched_masks, batched_users, w)
        data = model.group_wordpiece(embeddings, w, do_wordpiece)
        centroids = model.cluster_embeddings(data, k_range, w, lamb=10000)
        np.save(f'{c_path}/{w}.npy', centroids)


def match_embeddings(all_sent, all_vocab, Word2Vec_Dir):

    #load model
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
    model_name = BertModel.from_pretrained('bert-base-uncased', output_hidden_states=True)
    model = Matcher(tokenizer, model_name)
    c_path = f'{Word2Vec_Dir}/output/centroids'
    #load centroids
    centroids_d = model.load_centroids(all_vocab, f'{Word2Vec_Dir}/output')
    seq = [tpl for tpl in all_sent if any(w in tpl[1].split() for w in all_vocab)]
    o_path = f'{Word2Vec_Dir}/output'
    if not os.path.exists(o_path):
        os.makedirs(o_path)
    batched_data, batched_words, batched_masks, batched_users = model.get_batches(seq, batch_size)
    model.get_embeddings_and_match(batched_data, batched_words, batched_masks, batched_users, centroids_d, o_path)
    print('\nWord sense induction finished. Producing output files...\n')


def get_cluster_sentences(Word2Vec_Dir):

    s_paths = []
    with open(f'{Word2Vec_Dir}/output/senses', 'r') as f:
        tokens = f.read().split('\n')[:-1]
    vocab = list(set([tok.split('\t')[1] for tok in tokens]))
    tokens = [tok.split('\t') for tok in tokens]
    d = {}
    for w in vocab:
        w_path = f'{Word2Vec_Dir}/results/{w}'
        if not os.path.exists(w_path):
            os.makedirs(w_path)
        occs = [tok for tok in tokens if tok[1] == w]
        senses = sorted(list(set([occ[-1] for occ in occs])))
        results = open(f'{w_path}/{w}_clusters.txt', 'w')
        s_paths.append(f'{w_path}/{w}_clusters.txt')
        d[w] = {s: [] for s in senses}
        for s in senses:
            results.write(f'\n\nSENSE {s}:\n')
            s_occs = [tok for tok in occs if tok[-1] == s]
            sents = []
            for i, tok in enumerate(s_occs):
                idx = int(tok[0].split('<sep>')[0])
                f_name = tok[0].split('<sep>')[1]
                head, tail = os.path.split(f_name)
                f_name_no_ext = os.path.splitext(tail)[0]
                pickle_path = os.path.join(Word2Vec_Dir, 'output', f_name_no_ext, 'sentences.pickle')

                with open(pickle_path, 'rb') as f: # TODO: remove redundant path
                    sentences = pickle.load(f)
                sents.append(sentences[idx])
            d[w][s] = [sent[1] for sent in sents]
            for sent in sents:
                results.write('\n')
                results.write(f'FILE: {sent[-1]} SEQUENCE: {sent[1]}')
    with open(f'{Word2Vec_Dir}/output/d.pickle', 'wb') as f:
        pickle.dump(d, f)

    return s_paths


def main():

    with open('/home/gog/work/NLP-Suite/lib/sampleData/Bunin - Gentle breath.txt', 'r') as f:
        text = f.read().lower()
    vocab =  get_vocab(text, vocab=['olia'])
    print(vocab)


if __name__ == '__main__':
    main()

