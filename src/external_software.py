import requests  

# Start Google Earth Pro
response = requests.post("http://software-container:5000/start-google-earth")
print("Google Earth Output:", response.json())

# Start Gephi
response = requests.post("http://software-container:5000/start-gephi")
print("Gephi Output:", response.json())

# Run MALLET
response = requests.post("http://software-container:5000/run-mallet", json={"command": "import-dir --input sample_data --output topic-input"})
print("MALLET Output:", response.json())

# Query WordNet
response = requests.get("http://software-container:5000/wordnet", params={"word": "computer"})
print("WordNet Output:", response.json())
