import PyPDF2
from openai import OpenAI
import os

from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



def process_pdf(file_stream, style):
    
    # with open(filepath, 'rb') as file:
    #     reader = PyPDF2.PdfReader(file)
    #     text = ""
    #     for page in reader.pages:
    #         text += page.extract_text()

    reader = PyPDF2.PdfReader(file_stream)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    
    
    if style == 'basic':
        style_prompt = "Generate a basic HTML resume."
    elif style == 'college':
        style_prompt = "Generate an HTML resume for a college student."
    elif style == 'modern':
        style_prompt = "Generate a modern, clean HTML resume."
    elif style == 'overleaf':
        style_prompt = "Generate an HTML resume in a style similar to an Overleaf resume."
    else:
        style_prompt = "Generate a default HTML resume."
    
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates meaningful and beautiful HTML resumes from LinkedIn profile information."},
            {"role": "user", "content": f"{style_prompt} Here is the LinkedIn profile information: {text}"}
        ]
    )
    
    prediction = response.choices[0].message.content.strip()
    return prediction