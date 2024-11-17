import IO_files_util
import charts_util


def run_run_burst(inputFilename, inputDir, outputDir,
        case_sensitive_var,
        csv_file_categorical_field_list, # TODO: frontend checks that this is > 2, need to transform into list
        filter_options_var,
        fixed_param_var,
        rate_param_var,
        base_param_var,
        categorical_menu_var, #TODO: add this var to frontend
        pie_char_var, # TODO: Add to frontend
        tree_map_var # TODO: Add to frontend
        ):
        filesToOpen = []
        # categorical
        outputFilename = IO_files_util.generate_output_file_name(inputFilename, inputDir, outputDir,
                                                                '.html', categorical_menu_var)
        
        if filter_options_var=='No filtering':
            fixed_param_var=None
            rate_param_var=None
            base_param_var=None
        if filter_options_var=='Fixed parameter':
            rate_param_var=None
            base_param_var=None
        if filter_options_var=='Propagating parameter':
            fixed_param_var=None

        if pie_char_var:    
            pie_output = charts_util.Sunburst_Treemap(inputFilename, outputFilename, outputDir, csv_file_categorical_field_list, 1, fixed_param_var, rate_param_var, base_param_var, filter_options_var, case_sensitive_var)
            if pie_output: 
                if isinstance(pie_output, str):
                    filesToOpen.append(pie_output)
                else:
                    filesToOpen.extend(pie_output)
        if tree_map_var:
            tree_map_output = charts_util.Sunburst_Treemap(inputFilename, outputFilename, outputDir, csv_file_categorical_field_list, 0, fixed_param_var, rate_param_var, base_param_var, filter_options_var, case_sensitive_var)    
            if tree_map_output:  
                if isinstance(tree_map_output, str):
                    filesToOpen.append(tree_map_output)
                else:
                    filesToOpen.extend(tree_map_output)
        return filesToOpen

