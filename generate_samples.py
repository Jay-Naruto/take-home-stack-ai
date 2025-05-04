import cohere
from uuid import uuid4
import json
import os
from dotenv import load_dotenv

load_dotenv()

cohere_api_key = os.getenv("COHERE_API_KEY")
co = cohere.Client(cohere_api_key)

def generate_embedding(text: str):
    response = co.embed(
        model='embed-english-light-v3.0',
        texts=[text],
        input_type="search_query",
        embedding_types=["float"],
    )
    return response.embeddings.float[0]

sample_texts = [
    "AI is transforming industries.",
    "Machine learning is crucial for predictive analysis.",
    "Healthcare is benefiting from advancements in technology.",
    "Automation tools help businesses improve productivity.",
    "The global economy is shifting towards data-driven decisions.",
    "E-commerce platforms are changing the way consumers shop.",
    "Recycling technologies are helping reduce waste.",
    "Electric vehicles are becoming more affordable.",
    "The future of work is in remote collaboration tools.",
    "Blockchain technology is revolutionizing financial systems.",
    "Smart cities use IoT to enhance public services.",
    "Healthcare data analytics is helping doctors make informed decisions.",
    "Digital marketing strategies are key to business success.",
    "Cloud computing has changed how businesses store and process data.",
    "Telemedicine is growing as an effective way to provide healthcare.",
    "Renewable energy is crucial for sustainable growth.",
    "Online education is revolutionizing how people learn worldwide.",
    "Augmented reality is improving shopping experiences.",
    "The hospitality industry is adopting new technologies for better service.",
    "Space exploration is making significant strides with private companies."
]



libraries = []

# def generate_json():
#     for i in range(10):
#         library_name = f"Library {i+1}"
#         documents = []
        
#         document = {
#             "name": f"Document {i+1}",
#             "chunks": [],
#             "metadata_config": {
#                     "metadata_info": f"Metadata for Document {i+1}"
#                 }
#         }
        
#         for j in range(2):
#             chunk_text = sample_texts[(i * 2 + j) % len(sample_texts)] 
#             embedding = generate_embedding(chunk_text)
#             chunk = {
#                 "text": chunk_text,
#                 "embedding": embedding,
#                 "metadata_config": {
#                     "metadata_info": f"Metadata for chunk {j+1} in Document {i+1}"
#                 }
#             }
#             document["chunks"].append(chunk)
        
#         libraries.append({
#             "name": library_name,
#             "documents": [document],
#             "metadata_config": {
#                 "metadata_info": f"Metadata for Library {i+1}"
#             }
#         })

#     json_output = json.dumps(libraries[4], indent=2)

#     return json_output
#     # with open("output.json", "w") as json_file:
#     #     json_file.write(json_output)





for i in range(10):
        library_name = f"Library {i+1}"
        documents = []
        
        document = {
            "name": f"Document {i+1}",
            "chunks": [],
            "metadata_config": {
                    "metadata_info": f"Metadata for Document {i+1}"
                                }
        }
        
        for j in range(2):
            chunk_text = sample_texts[(i * 2 + j) % len(sample_texts)] 
            embedding = generate_embedding(chunk_text)
            chunk = {
                "text": chunk_text,
                "embedding": embedding,
                "metadata_config": {
                    "metadata_info": f"Metadata for chunk {j+1} in Document {i+1}"
                    }
            }
            document["chunks"].append(chunk)
        libraries.append({
            "name": library_name,
            "documents": [document],
            "metadata_config": {
                "metadata_info": f"Metadata for Library {i+1}"
                            }
        })

json_output = json.dumps(libraries[0], indent=2)
with open("output.json", "w") as json_file:
    json_file.write(json_output)