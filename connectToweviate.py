import os
import weaviate
from weaviate.classes.init import Auth
import json


# Define API key and URL as strings
WEAVIATE_API_KEY = "VP7sH6xdEs7UleUmTNOr6vn6Igk5fNsKaAZd"
WEAVIATE_URL  = "https://qv0mqyrs4oxagxq9fn5q.c0.us-west3.gcp.weaviate.cloud"

# The rest of your code remains the same
# Use the defined constants instead of environment variables
weaviate_url = WEAVIATE_URL
weaviate_api_key = WEAVIATE_API_KEY


import weaviate
from weaviate.auth import AuthApiKey

WEAVIATE_API_KEY = "VP7sH6xdEs7UleUmTNOr6vn6Igk5fNsKaAZd"
WEAVIATE_URL = "https://b631db80-834a-4a3f-b88f-8e90bf230453.weaviate.network"
OPENAI_API_KEY =  # Replace with your actual OpenAI API key


# Connect to Weaviate Cloud
client = weaviate.Client(
    url=weaviate_url,
    auth_client_secret=Auth.api_key(weaviate_api_key),
        additional_headers={
        "X-OpenAI-Api-Key": OPENAI_API_KEY  # Or "X-Cohere-Api-Key" or "X-HuggingFace-Api-Key" 
    }
)

client.data_object.get()

nearText = {"concepts": ["biology"]}

result = (
    client.query
    .get("Question", ["question", "answer", "category"])
    .with_near_text(nearText)
    .with_limit(2)
    .do()
)

print(json.dumps(result, indent=4))


# Delete existing schema (if necessary - THIS WILL ALSO DELETE ALL OF YOUR DATA)
client.schema.delete_all()

# Fetch & inspect schema (should be empty)
schema = client.schema.get()

print(json.dumps(schema, indent=4))

# ===== add schema ===== 
class_obj = {
    "class": "Question",
    "vectorizer": "text2vec-openai"  # Or "text2vec-cohere" or "text2vec-huggingface"
}

client.schema.create_class(class_obj)

# ===== import data ===== 
# Load data from GitHub
import requests
url = 'https://raw.githubusercontent.com/weaviate/weaviate-examples/main/jeopardy_small_dataset/jeopardy_tiny.json'
resp = requests.get(url)
data = json.loads(resp.text)

# Configure a batch process
with client.batch as batch:
    batch.batch_size=100
    # Batch import all Questions
    for i, d in enumerate(data):
        print(f"importing question: {i+1}")

        properties = {
            "answer": d["Answer"],
            "question": d["Question"],
            "category": d["Category"],
        }

        client.batch.add_data_object(properties, "Question")

#print(client.is_ready())