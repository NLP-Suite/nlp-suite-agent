import os
import Gephi_util

def run_gephi_graph(inputFilename, outputDir, 
        csv_file_relational_field_list,
        dynamic_network_field_var,
        inputFileData=None
        ):
        if len(csv_file_relational_field_list)!=3:
                print("Warning",
                               "You must select three csv fields to be used in the computation of the network graph, in the order of node, edge, node (e.g., Subject, Verb, Object).\n\nIf you wish to create a dynamic network graph you can select a fourth field to be used as the dynamic index (e.g., Sentence ID or Date).")
                return
            
        fileBase = "network_graph" if inputFileData else os.path.basename(inputFilename)[0:-4]
        
        # csv_file_relational_field_list contains the column header of node1, edge, node2 (e.g., SVO), and, possibly, the field for dynamic network
        return Gephi_util.create_gexf(fileBase, outputDir, inputFilename,
                                    csv_file_relational_field_list[0], csv_file_relational_field_list[1],
                                    csv_file_relational_field_list[2], dynamic_network_field_var, 'abnormal',
                                    inputFileData=inputFileData)

def main():
    input_data = """Name,Heritage,Color,Date
Max,Designer/deliberate mix,Dark brown,01-15-2022
Isla,Single breed,Black,02-10-2022
Tyson,Mixed breed/unknown,Black,03-05-2022
Lexi,Designer,Light brown,04-20-2022
Lola,Mixed breed/unknown,Black,05-25-2022
Lady,Single breed,Black,06-30-2022
Leo,Single breed,Reddish,07-15-2022"""

    input_filename = 'sample.csv'  
    output_directory =  "C:/Users/sherry/OneDrive/Desktop/QTM446W/Ouput" 
    csv_fields = ["Name", "Heritage", "Color"]
    # NEEDS TO BE A DATE STRING: MM-DD-YYYY
    dynamic_field = "Date" 

    output_file = run_gephi_graph(
        inputFilename=input_filename,
        outputDir=output_directory,
        csv_file_relational_field_list=csv_fields,
        dynamic_network_field_var=dynamic_field,
        inputFileData=input_data  
    )

    print(f"GEXF file created at: {output_file}")

if __name__ == '__main__':
    main()