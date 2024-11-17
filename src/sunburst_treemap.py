import IO_files_util
import charts_util


def run_run_burst(inputFilename, inputDir, outputDir,
        case_sensitive_var,
        csv_file_categorical_field_list, # TODO: frontend checks that this is > 2
        filter_options_var,
        fixed_param_var,
        rate_param_var,
        base_param_var,
        categorical_menu_var, #TODO: add this var to frontend
        csv_field_categorical_var, #TODO: add this var to frontend, check not empty
        ):
    
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
        if 'Sunburst' in categorical_menu_var.get():
            
            if csv_field_categorical_var=='':
                print("Warning, The sunburst algorithm requires a value for 'csv file field.'\n\nPlease, select a value and try again.")
                return

            outputFiles = charts_util.Sunburst_Treemap(inputFilename, outputFilename, outputDir, csv_file_categorical_field_list, 1,  fixed_param_var, rate_param_var, base_param_var, filter_options_var, case_sensitive_var)
        
        return outputFiles

