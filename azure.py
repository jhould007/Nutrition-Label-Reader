import os  
from openai import AzureOpenAI  
import ocr

def openai_init():
    endpoint = os.getenv("ENDPOINT_URL", "https://mywestusregion.openai.azure.com/openai/deployments/gpt-35-turbo/chat/completions?api-version=2024-08-01-preview")
    deployment = os.getenv("DEPLOYMENT_NAME", "gpt-35-turbo")
    subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "f13de0a9e7e14570958e7fece7338171")
    
    # Initialize Azure OpenAI client with key-based authentication
    client = AzureOpenAI(  
        azure_endpoint=endpoint,  
        api_key=subscription_key,  
        api_version="2024-05-01-preview",  
    )  
    
def get_openai_insights(file_path):
    # Extract text from nutrition label
    label_text = ocr.read_label(file_path)  

    # Construct dynamic user content
    user_content = f"""Here is the ingredient list for a food item: [{label_text}]. 
    Can you analyze these ingredients, identify those that are unhealthy when consumed regularly, and only provide brief explanations for those? Explanations for healthy or neutral ingredients are not necessary."""
  
    # Prepare the chat prompt  
    chat_prompt = [
    {
        "role": "system",
        "content": "You are a nutrition expert who provides accurate and concise analyses of food ingredients, focusing on their health implications. Wherever possible, include credible sources or references to support your claims."
    },
    {
        "role": "user",
        "content": user_content
    }
    ]
    
    # Include speech result if speech is enabled  
    speech_result = chat_prompt  
    
    # Generate the completion  
    completion = client.chat.completions.create(  
        model=deployment,  
        messages=speech_result,   
        max_tokens=800,  
        temperature=0.7,  
        top_p=0.95,  
        frequency_penalty=0,  
        presence_penalty=0,  
        stop=None,  
        stream=False  
    )

    # Get and print response  
    response = completion.choices[0].message.content
    return response

#____________________________________________________________________________________________________________________________________
 
# Set up Azure OpenAI info   
endpoint = os.getenv("ENDPOINT_URL", "https://mywestusregion.openai.azure.com/openai/deployments/gpt-35-turbo/chat/completions?api-version=2024-08-01-preview")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-35-turbo")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "f13de0a9e7e14570958e7fece7338171")
    
# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(  
    azure_endpoint=endpoint,  
    api_key=subscription_key,  
    api_version="2024-05-01-preview",  
)  
    
# Extract text from nutrition label
label_text = ocr.read_label("Images/SkittleIngredientList.png")  

# Construct dynamic user content
user_content = f"""Here is the ingredient list for a food item: [{label_text}]. 
Can you analyze these ingredients and let me know if there are any that may not be healthy when consumed regularly? 
Please provide a brief explanation for any concerns."""
  
# Prepare the chat prompt  
chat_prompt = [
{
    "role": "system",
    "content": "You are a nutrition expert who provides accurate and concise analyses of food ingredients, focusing on their health implications. Wherever possible, include credible sources or references to support your claims."
},
{
    "role": "user",
    "content": user_content
}
]
    
# Include speech result if speech is enabled  
speech_result = chat_prompt  
    
# Generate the completion  
completion = client.chat.completions.create(  
    model=deployment,  
    messages=speech_result,   
    max_tokens=800,  
    temperature=0.7,  
    top_p=0.95,  
    frequency_penalty=0,  
    presence_penalty=0,  
    stop=None,  
    stream=False  
)

# Get and print response  
#response = completion.choices[0].message.content
#print(f"Response: {response}")