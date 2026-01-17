# written by Roberto Franzosi November 2019
# rewritten by Roberto Franzosi January 2023

import IO_files_util
import charts_util 
import json
import pandas as pd 
import io 
from get_first_csv import first_csv


def run_sankey(inputDir, outputDir,
        csv_file_relational_field_list, # = "a, b, c"
        Sankey_limit1_var, Sankey_limit2_var, Sankey_limit3_var,
        ):
    
        file = first_csv(inputDir)

        
        # data = json.loads(data)
        
        
        # data = pd.DataFrame(data) 
        # # @@@ nan values will break the code
        # data = data.fillna("Blank/missing value")
        
        # # csv_file_relational_field_list = json.loads(csv_file_relational_field_list)
        output_label = 'Sankey'
        
        outputFilename = IO_files_util.generate_output_file_name(file, inputDir, outputDir,
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
            
        outputFiles = charts_util.Sankey(file, outputFilename,
                                    csv_file_relational_field_list[0], Sankey_limit1_var, csv_file_relational_field_list[1],
                                            Sankey_limit2_var, three_way_Sankey, var3, Sankey_limit3_var)
            
        if outputFiles != None:
            if isinstance(outputFiles, str):
                filesToOpen.append(outputFiles)
            else:
                filesToOpen.extend(outputFiles)


        return outputFiles


def main(): 
    data ='''Obs,Name,Gender,Fixed,Color,Heritage,Age,Weight,Size
        1,Max,Male,Yes,Dark brown,"Designer/deliberate mix (e.g., labradoodles)",7,70,Large
        2,Isla,Female,Yes,Black,Single breed,8,13,Small
        3,Tyson,Male,No,Black,Mixed breed/unknown,0.33,24,Large
        4,Lexi,Female,Yes,Light brown,"Designer/deliberate mix (e.g., labradoodles)",6,24,Small
        5,,Male,Yes,Light brown,Mixed breed/unknown,6,45,Large
        6,Lola,Female,Yes,Black,Mixed breed/unknown,14,85,Large
        7,Lady,Female,Yes,Black,Single breed,11,22,Small
        8,Leo,Male,Yes,Reddish,Single breed,15,14,Small''' #csv file 

    rows = [row.split(",") for row in data.split("\n")]
    headers = rows[0]
    data_list = [dict(zip(headers, row)) for row in rows[1:]]

    data = json.dumps(data_list)

    
    
    inputDir = "/Users/aidenamaya/nlp-suite/csvInput"
    outputDir = "/Users/aidenamaya/nlp-suite/output"
    csv_file_relational_field_list = "Name, Gender"
    Sankey_limit1_var = 10
    Sankey_limit2_var = 15
    Sankey_limit3_var = 20

    run_sankey(
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
