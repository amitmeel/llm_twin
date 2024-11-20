import os
from dotenv import load_dotenv, find_dotenv, dotenv_values

load_dotenv(find_dotenv(), override=True)

# Get the .env file contents
env_vars = dotenv_values(".env")

# Print only the variables that are in your .env file
# for key in env_vars:
#     print(f"{key}: {os.getenv(key)}")
# all_env_vars = dict(os.environ)
# print(all_env_vars)
##### TEST AZURE OPENAI ENDPOINT

# import openai
# from openai import AzureOpenAI

# def get_azure_openai_response(prompt, model_name, api_key, endpoint):
#     """
#     Get completion from Azure OpenAI service.

#     Args:
#         prompt (str): The input prompt for the model
#         model_name (str): The deployment name of your model
#         api_key (str): Your Azure OpenAI API key
#         endpoint (str): Your Azure OpenAI endpoint URL

#     Returns:
#         str: The model's response
#     """
#     # Initialize the Azure OpenAI client
#     client = AzureOpenAI(
#         api_key=api_key, api_version="2024-08-01-preview", azure_endpoint=endpoint
#     )

#     try:
#         # Make the API call
#         response = client.chat.completions.create(
#             model=model_name,  # This should be your deployment name
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.7,
#             max_tokens=800,
#         )

#         # Extract and return the response text
#         return response.choices[0].message.content

#     except Exception as e:
#         return f"An error occurred: {str(e)}"


# # Example usage
# if __name__ == "__main__":
#     # Replace these with your actual values
#     MODEL_NAME = os.getenv("AZURE_OPENAI_MODEL_ID")
#     API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
#     ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")

#     # Example prompt
#     prompt = "What is artificial intelligence?"

#     # Get response
#     response = get_azure_openai_response(prompt, MODEL_NAME, API_KEY, ENDPOINT)
#     print("Response:", response)


####### TEST MONGODB CONNECTION

# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi

# uri = os.getenv("DATABASE_HOST")

# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))

# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

####### TEST QDRANT VECTOR DB CONNECTION

from qdrant_client import QdrantClient
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_CLOUD_URL"), 
    api_key=os.getenv("QDRANT_APIKEY"),
)

print(qdrant_client.get_collections())