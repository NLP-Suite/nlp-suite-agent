import os
import subprocess
from sys import platform


def run_MALLET(inputDir, outputDir, numTopics, chartPackage='Excel', dataTransformation='', OptimizeInterval=False):
    # Ensure MALLET is installed and environment variables are set
    MALLETDir = os.getenv('MALLET_HOME')
    if not MALLETDir:
        print('The MALLET_HOME environment variable is not set. Please set it before running the application.')
        raise EnvironmentError('MALLET_HOME environment variable not set.')

    MALLETBinDir = os.path.join(MALLETDir, 'bin')

    # Validate input and output directories
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

    # Count the number of .txt files in inputDir
    numFiles = len([f for f in os.listdir(inputDir) if f.endswith('.txt')])
    if numFiles == 0:
        print('The input directory does not contain any .txt files.')
        raise ValueError('No .txt files found in input directory.')
    elif numFiles < 50:
        print(f'The input directory contains only {numFiles} .txt files. Topic modeling may not produce valid results with so few files.')

    # Define output filenames
    TXTFiles_MALLETFormatted_FileName = os.path.join(outputDir, "MALLETFormatted_TXTFiles.mallet")
    Composition_FileName = os.path.join(outputDir, "NLP-MALLET_Output_Composition.tsv")
    Keys_FileName = os.path.join(outputDir, "NLP-MALLET_Output_Keys.tsv")
    Compressed_FileName = os.path.join(outputDir, "NLP-MALLET_Output_Compressed.gz")

    # List to store files generated for further processing or opening
    filesToOpen = []

    print('Started running MALLET Topic modeling.')

    # First Step: Import Corpus
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

    # Second Step: Train Topics
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

    # Convert TSV files to CSV if necessary (this requires a file conversion utility, not shown here)
    # If you have a conversion function, you would call it here, for example:
    # header_keys = ['Topic #', 'Weight', 'Keywords']
    # Keys_FileName_csv = file_converter_util.tsv_converter(Keys_FileName, outputDir, header_keys)
    # filesToOpen.append(Keys_FileName_csv)

    # header_composition = ['Document ID', 'Document'] + [f"Topic #{i} Weight in Document" for i in range(numTopics)]
    # Composition_FileName_csv = file_converter_util.tsv_converter(Composition_FileName, outputDir, header_composition)
    # filesToOpen.append(Composition_FileName_csv)

    # For now, append the original files
    filesToOpen.append(Keys_FileName)
    filesToOpen.append(Composition_FileName)
    filesToOpen.append(Compressed_FileName)

    # Generate charts if needed
    if chartPackage != 'No charts':
        # Implement chart generation logic here, if needed
        pass

    # Return the list of files generated
    return filesToOpen
