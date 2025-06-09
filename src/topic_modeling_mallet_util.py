import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import charts_matplotlib_seaborn_util
import charts_util

def run_MALLET(inputDir, outputDir, numTopics, chartPackage='Excel', dataTransformation='', OptimizeInterval=False):
    # Validate directories 
    if ' ' in inputDir or ' ' in outputDir:
        raise ValueError('Input or output directory contains spaces.')

    if not os.path.isdir(inputDir):
        raise FileNotFoundError('Input directory does not exist.')

    if not os.path.isdir(outputDir):
        raise FileNotFoundError('Output directory does not exist.')

    numFiles = len([f for f in os.listdir(inputDir) if f.endswith('.txt')])
    if numFiles == 0:
        raise ValueError('No .txt files found in input directory.')
    elif numFiles < 50:
        print(f'Warning: Only {numFiles} .txt files. Topic modeling may be weak.')

    # Prepare the API request
    # REPLACE W/ ACTUAL address for server
    api_url = "http://<MALLET_API_CONTAINER_HOST>:5050/run"  

    import_dir = inputDir
    output_dir = outputDir
    command = "import-dir"
    args_import = {
        "input": import_dir,
        "output": os.path.join(output_dir, "MALLETFormatted_TXTFiles.mallet"),
        "keep-sequence": True,
        "remove-stopwords": True
    }

    command2 = "train-topics"
    args_train = {
        "input": args_import["output"],
        "num-topics": numTopics,
        "output-state": os.path.join(output_dir, "NLP-MALLET_Output_Compressed.gz"),
        "output-topic-keys": os.path.join(output_dir, "NLP-MALLET_Output_Keys.txt"),
        "output-doc-topics": os.path.join(output_dir, "NLP-MALLET_Output_Composition.txt"),
    }

    if OptimizeInterval:
        args_train["optimize-interval"] = numTopics

    # Call MALLET import-dir
    res1 = requests.post(api_url, json={"command": command, "args": args_import})
    if res1.status_code != 200:
        raise RuntimeError(f"MALLET import-dir failed: {res1.json()}")

    # Call MALLET train-topics
    res2 = requests.post(api_url, json={"command": command2, "args": args_train})
    if res2.status_code != 200:
        raise RuntimeError(f"MALLET train-topics failed: {res2.json()}")

    print("Finished calling MALLET API.")

    # Reading output files and making charts
    keys_file = args_train["output-topic-keys"]
    composition_file = args_train["output-doc-topics"]

    if not os.path.isfile(keys_file) or not os.path.isfile(composition_file):
        raise FileNotFoundError('Expected MALLET output files not found.')

    keys_df = pd.read_csv(keys_file, sep='\t', header=None, names=['Topic #', 'Weight', 'Keywords'])
    keys_csv_file = os.path.join(output_dir, 'NLP-MALLET_Output_Keys.csv')
    keys_df.to_csv(keys_csv_file, index=False)

    composition_df = pd.read_csv(composition_file, sep='\t', header=None)
    num_columns = composition_df.shape[1]
    topic_columns = [f'Topic {i} Proportion' if i % 2 == 1 else f'Topic {i // 2}' for i in range(2, num_columns)]
    composition_df.columns = ['Document ID', 'Document'] + topic_columns
    composition_csv_file = os.path.join(output_dir, 'NLP-MALLET_Output_Composition.csv')
    composition_df.to_csv(composition_csv_file, index=False)

    filesToOpen = [keys_csv_file, composition_csv_file]

    if chartPackage != 'No charts':
        heatmap_file = charts_matplotlib_seaborn_util.MALLET_heatmap(composition_csv_file, keys_csv_file, output_dir)
        filesToOpen.append(heatmap_file)

        additional_charts = charts_util.run_all(
            columns_to_be_plotted=[(2, num_columns - 1)],
            inputFilename=composition_csv_file,
            outputDir=output_dir,
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