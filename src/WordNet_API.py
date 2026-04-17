import os 
import requests


AGENT_MOUNT_PATH = "/root/nlp-suite"


def call_wordnet_api(cmd, call_list, args):

    # api_url = f"http://172.16.0.13:7070/{cmd}"
    
    api_url = f"http:localhost:7070/{cmd}"

    
    payload = {"cmd": cmd,
               "call_list": {call_list}}
    
    
    print(f"Calling wordnet cmd: {cmd} with call list: {call_list}")
    
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status() #if http error occurs
        
        
        return response.json()
    
    except Exception as e:
        raise RuntimeError(f"Failed to call WordNet API w/ command {cmd} and call list {call_list}")
    

def wordnet_to_agent_path(path):
    return path.replace("/app", AGENT_MOUNT_PATH)
        
        
    
    