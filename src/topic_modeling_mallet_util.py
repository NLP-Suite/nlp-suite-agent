import os
import subprocess
from sys import platform
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import charts_matplotlib_seaborn_util 
import charts_util 

def run_MALLET(inputDir, outputDir, numTopics, chartPackage='Excel', dataTransformation='', OptimizeInterval=False):
    MALLETDir = os.getenv('MALLET_HOME')
    if not MALLETDir:
        print('The MALLET_HOME environment variable is not set. Please set it before running the application.')
        raise EnvironmentError('MALLET_HOME environment variable not set.')

    MALLETBinDir = os.path.join(MALLETDir, 'bin')

    if ' ' in inputDir:
        print('The selected INPUT directory contains a space, which is not allowed.')
        raise ValueError('Input directory contains spaces.')

    if ' ' in outputDir:
        print('The selected OUTPUT directory contains a space, which is not allowed.')
        raise ValueError('Output directory contains spaces.')

    if not os.path.isdir(inputDir):
        print('The selected input directory does not exist.')
        raise FileNotFoundError('Input directory does not exist.')

    if not os.path.isdir(outputDir):
        print('The selected output directory does not exist.')
        raise FileNotFoundError('Output directory does not exist.')

    numFiles = len([f for f in os.listdir(inputDir) if f.endswith('.txt')])
    if numFiles == 0:
        print('The input directory does not contain any .txt files.')
        raise ValueError('No .txt files found in input directory.')
    elif numFiles < 50:
        print(f'The input directory contains only {numFiles} .txt files. Topic modeling may not produce valid results with so few files.')

    TXTFiles_MALLETFormatted_FileName = os.path.join(outputDir, "MALLETFormatted_TXTFiles.mallet")
    Composition_FileName = os.path.join(outputDir, "NLP-MALLET_Output_Composition.txt")
    Keys_FileName = os.path.join(outputDir, "NLP-MALLET_Output_Keys.txt")
    Compressed_FileName = os.path.join(outputDir, "NLP-MALLET_Output_Compressed.gz")

    filesToOpen = []

    print('Started running MALLET Topic modeling.')

    import_command = [
        os.path.join(MALLETBinDir, 'mallet'),
        'import-dir',
        '--input', inputDir,
        '--output', TXTFiles_MALLETFormatted_FileName,
        '--keep-sequence',
        '--remove-stopwords'
    ]

    shell_flag = platform == "win32"
    subprocess.call(import_command, shell=shell_flag)

    train_command = [
        os.path.join(MALLETBinDir, 'mallet'),
        'train-topics',
        '--input', TXTFiles_MALLETFormatted_FileName,
        '--num-topics', str(numTopics),
        '--output-state', Compressed_FileName,
        '--output-topic-keys', Keys_FileName,
        '--output-doc-topics', Composition_FileName
    ]

    if OptimizeInterval:
        train_command.extend(['--optimize-interval', str(numTopics)])

    subprocess.call(train_command, shell=shell_flag)

    print('Finished running MALLET Topic modeling.')

    if not os.path.isfile(Keys_FileName) or not os.path.isfile(Composition_FileName):
        print('MALLET did not produce the expected output files.')
        raise FileNotFoundError('MALLET output files not found.')

    keys_df = pd.read_csv(Keys_FileName, sep='\t', header=None, names=['Topic #', 'Weight', 'Keywords'])
    keys_csv_file = os.path.join(outputDir, 'NLP-MALLET_Output_Keys.csv')
    keys_df.to_csv(keys_csv_file, index=False)
    filesToOpen.append(keys_csv_file)

    composition_df = pd.read_csv(Composition_FileName, sep='\t', header=None)
    num_columns = composition_df.shape[1]
    topic_columns = [f'Topic {i} Proportion' if i % 2 == 1 else f'Topic {i // 2}' for i in range(2, num_columns)]
    composition_df.columns = ['Document ID', 'Document'] + topic_columns
    composition_csv_file = os.path.join(outputDir, 'NLP-MALLET_Output_Composition.csv')
    composition_df.to_csv(composition_csv_file, index=False)
    filesToOpen.append(composition_csv_file)


    if chartPackage != 'No charts':
        # Generate heatmap using custom function
        heatmap_file = charts_matplotlib_seaborn_util.MALLET_heatmap(composition_csv_file, keys_csv_file, outputDir)
        filesToOpen.append(heatmap_file)

        # Optionally run additional charts using charts_util
        additional_charts = charts_util.run_all(
            columns_to_be_plotted=[(2, num_columns - 1)],
            inputFilename=composition_csv_file,
            outputDir=outputDir,
            outputFileLabel='MALLET_TM',
            chartPackage=chartPackage,
            dataTransformation=dataTransformation,
            chart_type_list=["bar"],
            chart_title='MALLET Topics',
            column_xAxis_label_var='Document',
            hover_info_column_list=[],
            column_yAxis_label_var='Topic weight'
        )
        if additional_charts:
            filesToOpen.append(additional_charts)

    return filesToOpen


# if __name__ == '__main__':
#     inputDir = 'C:/Users/sherry/OneDrive/Desktop/QTM446W/Input'
#     outputDir = 'C:/Users/sherry/OneDrive/Desktop/QTM446W/Output'
#     numTopics = 20
#     run_MALLET(inputDir, outputDir, numTopics)
