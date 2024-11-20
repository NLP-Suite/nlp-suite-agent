import IO_files_util
import charts_util
import os
import json

def run_sun_burst(inputFilename, inputDir, outputDir,
        file_data,
        filter_options_var,
        selected_pairs_data,
        piechart_var, 
        treemap_var 
        ):
        try:
            saved_pairs = json.loads(selected_pairs_data)
        except json.JSONDecodeError:
            print("Invalid JSON in selected_pairs_data, status_code=400")
            raise ValueError("Invalid JSON in selected_pairs_data")
            return

        
        csv_file_categorical_field_list = [
            [f"{pair['searchField']}|{', '.join(word.strip() for word in pair['csvFieldList'].split(',') if word.strip())}"]
            for pair in saved_pairs
        ]
        print(csv_file_categorical_field_list)
        filesToOpen = []
        
        # NOTE: set to default values, can allow user input flexibility later 
        fixed_param_var = 50
        rate_param_var = 3
        base_param_var = 40
        
        if filter_options_var=='No filtering':
            fixed_param_var=None
            rate_param_var=None
            base_param_var=None
        if filter_options_var=='Fixed parameter':
            rate_param_var=None
            base_param_var=None
        if filter_options_var=='Propagating parameter':
            fixed_param_var=None

        # TODO: join with input file dir
        inputFilename = os.path.join(inputDir, inputFilename)
        if piechart_var:    
            piechart_outputFilename = IO_files_util.generate_output_file_name(inputFilename, inputDir, outputDir, '.html', "Sunburst")
            pie_output = charts_util.Sunburst_Treemap(file_data, piechart_outputFilename, outputDir, csv_file_categorical_field_list, 1, fixed_param_var, rate_param_var, base_param_var, filter_options_var)
            if pie_output: 
                if isinstance(pie_output, str):
                    filesToOpen.append(pie_output)
                else:
                    filesToOpen.extend(pie_output)
        if treemap_var:
            treemap_outputFilename = IO_files_util.generate_output_file_name(inputFilename, inputDir, outputDir, '.html', "Treemap")
            tree_map_output = charts_util.Sunburst_Treemap(file_data, treemap_outputFilename, outputDir, csv_file_categorical_field_list, 0, fixed_param_var, rate_param_var, base_param_var, filter_options_var)    
            if tree_map_output:  
                if isinstance(tree_map_output, str):
                    filesToOpen.append(tree_map_output)
                else:
                    filesToOpen.extend(tree_map_output)
        return filesToOpen
    

def main():
    inputFilename = "dogs.csv"
    inputDir = "C:/Users/sherry/OneDrive/Desktop/QTM446W/Input"
    outputDir = "C:/Users/sherry/OneDrive/Desktop/QTM446W/Ouput"
    file_data = """Obs,Name,Gender,Fixed,Color,Heritage,Age,Weight,Size
1,Max,Male,Yes,Dark brown,"Designer/deliberate mix (e.g., labradoodles)",7,70,Large
2,Isla,Female,Yes,Black,Single breed,8,13,Small
3,Tyson,Male,No,Black,Mixed breed/unknown,0.33,24,Large
4,Lexi,Female,Yes,Light brown,"Designer/deliberate mix (e.g., labradoodles)",6,24,Small
5,,Male,Yes,Light brown,Mixed breed/unknown,6,45,Large
6,Lola,Female,Yes,Black,Mixed breed/unknown,14,85,Large
7,Lady,Female,Yes,Black,Single breed,11,22,Small
8,Leo,Male,Yes,Reddish,Single breed,15,14,Small"""

    filter_options_var = "No filtering"
    selected_pairs_data = json.dumps([
        {"searchField": "Color", "csvFieldList": "Black,Reddish,Light brown,"},
        {"searchField": "Size", "csvFieldList": "Small, Medium, Large"}
    ])
    piechart_var = True 
    treemap_var = True

    run_sun_burst(
        inputFilename=inputFilename,
        inputDir=inputDir,
        outputDir=outputDir,
        file_data=file_data,
        filter_options_var=filter_options_var,
        selected_pairs_data=selected_pairs_data,
        piechart_var=piechart_var,
        treemap_var=treemap_var
    )

if __name__ == "__main__":
    main()


