import os
from openai import AzureOpenAI
import json
from dotenv import load_dotenv

load_dotenv()


def getTime(text):
    # Remove leading whitespaces
    text = text.lstrip()
    ans = 0
    found_digit = False
    for char in text:
        if char.isdigit():
            ans = ans * 10 + int(char)
            found_digit = True
        elif found_digit:  # Stop once we've found a number and hit a non-digit
            break
    return ans


def getDifficulty(text):
    # Remove leading whitespaces
    text = text.lstrip()
    parts = text.split(", ")
    if len(parts) > 1:
        return parts[1].strip()  # Return the second part (difficulty)
    return "Unknown"  # Fallback if the difficulty is missing

# NEED TO CHANGE THIS ACCORDING TO THE FINAL FORMULA

def getCompensation(time, difficulty):
    if(difficulty=="Easy"):
        return time*1
    elif(difficulty=="Medium"):
        return time*3
    elif(difficulty=="Hard"):
        return time*5


# Set the API version for Azure OpenAI
api_version = "2023-07-01-preview"

# Get the Azure API key
azure_api_key = os.getenv("AZURE_API_KEY")  # Ensure the environment variable is set

# Azure endpoint URL (replace with your Azure endpoint)
azure_endpoint = os.getenv("AZURE_ENDPOINT")


# Initialize the AzureOpenAI client with the API key
client = AzureOpenAI(
    api_key=azure_api_key,
    api_version=api_version,
    azure_endpoint=azure_endpoint,
)


print("Enter the prompt: ")
prompt=input()

# Using the babbage-002 model as it is cheapest and sufficient for this task
completion = client.completions.create(
    model="babbage-002-ft-731da07e706f48e0847d4b1164548ea3",  # deployment name of the model
    prompt=prompt,
    max_tokens=4,  # Adjust as needed
    temperature=0.7,  # Adjust temperature for randomness
)


# Print the response in JSON format
response=completion.to_json()
# Access the 'text' field inside the first choice
json_data=json.loads(response)

output=json_data['choices'][0]['text'].strip()
print(output)

time=getTime(output)
difficulty=getDifficulty(output)
print("Time:",time)
print("Difficulty:",difficulty)
compensation=getCompensation(time,difficulty)
print("Compensation:",compensation)