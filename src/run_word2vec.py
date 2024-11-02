import unittest
import os
from word2vec import run_word2vec 
import WSI_util
 

class TestWord2Vec(unittest.TestCase):

    def setUp(self):
        self.inputDir = 'C:/Users/sherry/OneDrive/Desktop/QTM446W/Input'
        self.outputDir = 'C:/Users/sherry/OneDrive/Desktop/QTM446W/Ouput'
        os.makedirs(self.inputDir, exist_ok=True)
        os.makedirs(self.outputDir, exist_ok=True)

        # TODO: need inputFilename?
        self.inputFilename = "" #"Conrad_Lord Jim_01.txt"
        
    def test_run_word2vec_basic(self):
        # Test with minimal settings
        filesToOpen = run_word2vec(
            inputFilename=self.inputFilename,
            inputDir=self.inputDir,
            outputDir=self.outputDir,
            openOutputFiles=False,
            chartPackage="Excel",
            dataTransformation="No transformation",
            remove_stopwords_var=False,
            lemmatize_var=False,
            WSI_var=True,
            BERT_var=False,
            Gensim_var=True,
            sg_menu_var="Skip-Gram",
            vector_size_var=100,
            window_var=5,
            min_count_var=5,
            vis_menu_var="Do not plot",
            dim_menu_var="2D",
            compute_distances_var=False,
            top_words_var=50,
            keywords_var="sea, ship, hero",
            keywordInput="sea",
            range4=2,
            range6=3,
            range20 = 5,
            ngramsDropDown="1-gram"
        )
        
        self.assertTrue(len(filesToOpen) > 0, "No output files were generated.")
        for file in filesToOpen:
            self.assertTrue(os.path.exists(file), f"Output file {file} does not exist.")



    # def tearDown(self):
    #     if os.path.exists(os.path.join(self.inputDir, self.inputFilename)):
    #         os.remove(os.path.join(self.inputDir, self.inputFilename))
    #     if os.path.exists(self.inputDir):
    #         os.rmdir(self.inputDir)
    #     if os.path.exists(self.outputDir):
    #         for root, dirs, files in os.walk(self.outputDir, topdown=False):
    #             for name in files:
    #                 os.remove(os.path.join(root, name))
    #             for name in dirs:
    #                 os.rmdir(os.path.join(root, name))
    #         os.rmdir(self.outputDir)

if __name__ == "__main__":
    unittest.main()
    #WSI_util.get_cluster_sentences("C:/Users/sherry/OneDrive/Desktop/QTM446W/Ouput/Word2Vec_Gensim_Input")
