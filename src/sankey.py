# written by Roberto Franzosi November 2019
# rewritten by Roberto Franzosi January 2023

import IO_files_util
import charts_util 

def run_sankey(inputFilename, inputDir, outputDir,
        csv_file_relational_field_list, # = "a, b, c"
        Sankey_limit1_var, Sankey_limit2_var, Sankey_limit3_var,
        ):

        output_label = 'Sankey'

        outputFilename = IO_files_util.generate_output_file_name(inputFilename, inputDir, outputDir,
                                                             '.html', output_label) 
        filesToOpen = []
        print(f"Original input: {csv_file_relational_field_list}") #
        csv_file_relational_field_list = [word.strip() for word in csv_file_relational_field_list.split(',')  if word.strip()] # added a ' ' before 
        print(f"Processed list: {csv_file_relational_field_list}")
        print(f"Length of the list: {len(csv_file_relational_field_list)}")

        if len(csv_file_relational_field_list)!=2 and len(csv_file_relational_field_list)!=3:
            print("Warning",
                "You must select 2 or 3 csv fields to be used in the computation of a Sankey chart (e.g., Subject, Verb, Object or Subject, Object).\n\nMAKE SURE TO CLICK ON THE + BUTTON AFTER THE LAST SELECTION. CLICK ON THE SHOW BUTTON TO SEE THE CURRENT SELECTION.")
            return
        
        if len(csv_file_relational_field_list)==3:
            three_way_Sankey=True
            var3=csv_file_relational_field_list[2]
        else: # if len(csv_file_relational_field_list) == 2
            three_way_Sankey = False
            var3=None
            Sankey_limit3_var=None
        outputFiles = charts_util.Sankey(inputFilename, outputFilename,
                                    csv_file_relational_field_list[0], Sankey_limit1_var, csv_file_relational_field_list[1],
                                            Sankey_limit2_var, three_way_Sankey, var3, Sankey_limit3_var)
            
        if outputFiles != None:
            if isinstance(outputFiles, str):
                filesToOpen.append(outputFiles)
            else:
                filesToOpen.extend(outputFiles)


        return outputFiles


def main(): 
    inputFilename = '/Users/johnlin/Documents/NLPSuite/NLPSuiteInput /NLP_CoreNLP_SVO_Dir_newspaperArticles.csv' #csv file 
    inputDir = "/Users/johnlin/Documents/NLPSuite/NLPSuiteInput "
    outputDir = "/Users/johnlin/Documents/NLPSuite/NLPSuiteOutput"
    csv_file_relational_field_list = "Subject (S),Verb (V),Object (O)"
    Sankey_limit1_var = 10
    Sankey_limit2_var = 15
    Sankey_limit3_var = 20

    run_sankey(inputFilename = inputFilename, 
               inputDir = inputDir, 
               outputDir = outputDir,
               csv_file_relational_field_list = csv_file_relational_field_list, 
               Sankey_limit1_var = Sankey_limit1_var, 
               Sankey_limit2_var = Sankey_limit2_var, 
               Sankey_limit3_var = Sankey_limit3_var,
        ) 
    # (inputFilename, inputDir, outputDir,
    #     csv_file_relational_field_list, # = "a, b, c"
    #     Sankey_limit1_var, Sankey_limit2_var, Sankey_limit3_var,
    #     ):
    
if __name__ == "__main__":
    main()
