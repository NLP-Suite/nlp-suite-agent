import IO_files_util
import charts_util
import os


def run_sun_burst(inputFilename, inputDir, outputDir,
        filter_options_var,
        csv_file_categorical_field_list,
        piechar_var, 
        treemap_var 
        ):
        case_sensitive_var = True
        csv_file_categorical_field_list = [word.strip() for word in csv_file_categorical_field_list.split(',') if word.strip()]
        filesToOpen = []
        categorical_menu_var = "Sunbursts"
        # categorical
        outputFilename = IO_files_util.generate_output_file_name(inputFilename, inputDir, outputDir,
                                                                '.html', categorical_menu_var)
        
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
        if piechar_var:    
            pie_output = charts_util.Sunburst_Treemap(inputFilename, outputFilename, outputDir, csv_file_categorical_field_list, 1, fixed_param_var, rate_param_var, base_param_var, filter_options_var, case_sensitive_var)
            if pie_output: 
                if isinstance(pie_output, str):
                    filesToOpen.append(pie_output)
                else:
                    filesToOpen.extend(pie_output)
        if treemap_var:
            tree_map_output = charts_util.Sunburst_Treemap(inputFilename, outputFilename, outputDir, csv_file_categorical_field_list, 0, fixed_param_var, rate_param_var, base_param_var, filter_options_var, case_sensitive_var)    
            if tree_map_output:  
                if isinstance(tree_map_output, str):
                    filesToOpen.append(tree_map_output)
                else:
                    filesToOpen.extend(tree_map_output)
        return filesToOpen

