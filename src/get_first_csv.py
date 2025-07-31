import os 


def first_csv(path):

    try:
        entries = os.listdir(path)
        
        first = None
        for entry in entries:
            if entry.endswith(".csv"):
                first = os.path.join(path, entry)
                return first 

        return None 
                
        
    except Exception as e:
        
        print("Error", e, " has occurred")
        return None