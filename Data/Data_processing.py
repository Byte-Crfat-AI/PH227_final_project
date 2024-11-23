import google.generativeai as gemini
import json 
import google.generativeai as genai
import re
from bs4 import BeautifulSoup
from Scraping import scrape

urls = ['https://www.phy.iitb.ac.in/en/employee-profile/aftab-alam']
metadata = ['faculty']
gemini.configure(api_key="AIzaSyBkXXtG5XeopoPisjR0LGqFdNcy3F_a8eo")

def process_url(url,category):
    soup = BeautifulSoup(scrape(url), "html.parser")
    sections = []
    if category == 'faculty':
        for section in soup.find_all(['div', 'p','h1','h2','li', 'ul', 'ol','h3','h4','h5','h6'], class_=['field-item even',None, None,None,None,None,None,None,None,None,None]):#'h1', 'h2', 'p', 'li', 'ul', 'ol','h3','h4','h5','h6']):
            text = section.get_text(strip=True)
            if text:
                sections.append(text)
    elif category == 'research':
        for section in soup.find_all(['div', 'p','h1','h2','li', 'ul', 'ol','h3','h4','h5','h6'], class_=['field-item even',None, None,None,None,None,None,None,None,None,None]):#'h1', 'h2', 'p', 'li', 'ul', 'ol','h3','h4','h5','h6']):
            text = section.get_text(strip=True)
            if text:
                sections.append(text)
    elif category == 'staff':
        for section in soup.find_all(['table']):
            text = section.get_text(strip=True)
            if text:
                sections.append(text)
    elif category == 'facilities':
        for section in soup.find_all(['div', 'p','h1','h2','li', 'ul', 'ol','h3','h4','h5','h6'], class_=['field-item even',None, None,None,None,None,None,None,None,None,None]):
            text = section.get_text(strip=True)
            if text:
                sections.append(text)
    else:
        for section in soup.find_all(['div', 'p','h1','h2','li', 'ul', 'ol','h3','h4','h5','h6'], class_=['field-item even',None, None,None,None,None,None,None,None,None,None]):
            text = section.get_text(strip=True)
            if text:
                sections.append(text)
    return sections

def clean_gemini_response_dynamic(response: str):
    json_match = re.search(r"{.*}", response, re.DOTALL)
    if not json_match:
        return {"error": "No JSON-like block found in the response."}

    # Extract the JSON-like string
    json_str = json_match.group(0)

    # Step 1: Remove comments (starting with `//`)
    json_str = re.sub(r"//.*", "", json_str)

    # Step 2: Ensure proper escaping of backslashes
    json_str = json_str.replace("\\\\", "\\\\\\\\")  # Escape double backslashes
    json_str = json_str.replace("\\\"", "\\\\\"")   # Escape quotes

    # Step 3: Validate JSON-like format and parse
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        # Try to pinpoint the error
        return {"error": f"JSON decoding failed: {e}"}
        
    cleaned_data = {}
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list):
                cleaned_data[key] = []
                for item in value:
                    if isinstance(item, dict):
                        cleaned_data[key].append({k: v for k, v in item.items()})
                    else:
                        cleaned_data[key].append(item)
            else:
                cleaned_data[key] = value
    
    return cleaned_data

def generate_json_from_text(prompt):
    try:
            model = genai.GenerativeModel("gemini-1.5-pro")
            response = model.generate_content(prompt)
            print(response)
            return clean_gemini_response_dynamic(str(response))
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        

        
def extract_data(urls, metadata):
    major_json = {}
    prompts = {
        'faculty': """Extract structured information from the provided HTML related to the Physics Department of IIT Bombay. The output should be a JSON object formatted for a chatbot RAG Database. Prioritize extracting the following key details:
        Name of the faculty
        Email address
        Phone number
        Office location
        Research interests
        Publications
        Other Details
        Text:
        {sections}""",
        
        'research': """Extract structured information from the provided HTML related to the Physics Department of IIT Bombay. The output should be a JSON object formatted for a chatbot RAG Database. Prioritize extracting the following key details:
        Description of the research
        People researching in that area
        Other Details
        Text:
        {sections}""",
        
        'staff': """Extract structured information from the provided HTML related to the Physics Department of IIT Bombay. The output should be a JSON object formatted for a chatbot RAG Database. Prioritize extracting the following key details:
        Name of the staff
        Designation
        Email address
        Phone number
        Office location
        Other Details
        Text:
        {sections}""",
        
        'facilities': """Extract structured information from the provided HTML related to the Physics Department of IIT Bombay. 
        The output should be a JSON object formatted for a chatbot RAG Database.
        Give me the complete output for this prompt.
        Text:
        {sections}""",
        
        'others': """Extract structured information from the provided HTML related to the Physics Department of IIT Bombay. The output should be a JSON object formatted for a chatbot RAG Database.
        Text:
        {sections}"""
    }

    for i in range(len(urls)):
        sections = process_url(urls[i], metadata[i])
        prompt = prompts.get(metadata[i], prompts['others']).format(sections=sections)
        response = generate_json_from_text(prompt)
        
        if response:
            if metadata[i] not in major_json:
                major_json[metadata[i]] = []
            major_json[metadata[i]].append(response)
    with open('physics_department_data.json', 'w') as f:
        json.dump(major_json, f, indent=2)
    print("Data successfully saved to 'physics_department_data.json'.")

extract_data(urls,metadata)