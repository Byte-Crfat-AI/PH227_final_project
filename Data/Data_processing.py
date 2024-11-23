import google.generativeai as gemini
import json 
import google.generativeai as genai
import re
from bs4 import BeautifulSoup
from Scraping import scrape

# List of URLs to scrape the data from and their corresponding metadata. Purpose of metadata is to categorize the URLs into different types
# so that the prompt can be customized accordingly.
urls = ['https://www.phy.iitb.ac.in/en/employee-profile/aftab-alam', 'https://www.phy.iitb.ac.in/en/employee-profile/m-aslam', 'https://www.phy.iitb.ac.in/en/content/soumya-bera', 'https://www.phy.iitb.ac.in/en/content/varun-bhalerao', 'https://www.phy.iitb.ac.in/en/content/sayantika-bhowal', 'https://www.phy.iitb.ac.in/en/employee-profile/raghunath-chelakkot', 'https://www.phy.iitb.ac.in/en/employee-profile/pragya-das', 'https://www.phy.iitb.ac.in/en/employee-profile/dibyendu-das', 'https://www.phy.iitb.ac.in/en/employee-profile/sadhana-dash', 'https://www.phy.iitb.ac.in/en/content/himadri-shekhar-dhar', 'https://www.phy.iitb.ac.in/en/employee-profile/subhabrata-dhar', 'https://www.phy.iitb.ac.in/en/content/gopal-dixit', 'https://www.phy.iitb.ac.in/en/employee-profile/kantimay-das-gupta', 'https://www.phy.iitb.ac.in/en/employee-profile/dinesh-kabra', 'https://www.phy.iitb.ac.in/en/content/rahul-kashyap', 'https://www.phy.iitb.ac.in/en/content/prashant-kumar', 'https://www.phy.iitb.ac.in/en/content/pramod-kumar', 'https://www.phy.iitb.ac.in/en/content/nitin-kumar', 'https://www.phy.iitb.ac.in/en/content/anshuman-kumar-0', 'https://www.phy.iitb.ac.in/en/employee-profile/tapanendu-kundu', 'https://www.phy.iitb.ac.in/en/employee-profile/avinash-v-mahajan', 'https://www.phy.iitb.ac.in/en/content/maniraj-mahalingam', 'https://www.phy.iitb.ac.in/en/employee-profile/dr-suddhasatta-mahapatra-1', 'https://www.phy.iitb.ac.in/en/faculty/mithun', 'https://www.phy.iitb.ac.in/en/employee-profile/asmita-mukherjee', 'https://www.phy.iitb.ac.in/en/content/uditendu-mukhopadhyay', 'https://www.phy.iitb.ac.in/en/employee-profile/basanta-kumar-nandi', 'https://www.phy.iitb.ac.in/en/employee-profile/amitabha-nandi', 'https://www.phy.iitb.ac.in/en/content/archana-pai', 'https://www.phy.iitb.ac.in/en/content/hridis-kumar-pal', 'https://www.phy.iitb.ac.in/en/employee-profile/punit-parmananda', 'https://www.phy.iitb.ac.in/en/content/sumiran-pujari', 'https://www.phy.iitb.ac.in/en/employee-profile/p-ramadevi', 'https://www.phy.iitb.ac.in/en/employee-profile/kumar-rao', 'https://www.phy.iitb.ac.in/en/employee-profile/vikram-rentala', 'https://www.phy.iitb.ac.in/en/content/shankaranarayanan-s', 'https://www.phy.iitb.ac.in/en/employee-profile/anirban-sain', 'https://www.phy.iitb.ac.in/en/content/siddhartha-santra', 'https://www.phy.iitb.ac.in/en/employee-profile/pradeep-sarin', 'https://www.phy.iitb.ac.in/en/content/manibrata-sen', 'https://www.phy.iitb.ac.in/en/employee-profile/m-senthil-kumar', 'https://www.phy.iitb.ac.in/en/employee-profile/alok-shukla', 'https://www.phy.iitb.ac.in/en/employee-profile/p-p-singh', 'https://www.phy.iitb.ac.in/en/content/sunita-srivastava', 'https://www.phy.iitb.ac.in/en/employee-profile/k-g-suresh', 'https://www.phy.iitb.ac.in/en/employee-profile/s-umasankar', 'https://www.phy.iitb.ac.in/en/employee-profile/raghava-varma', 'https://www.phy.iitb.ac.in/en/employee-profile/parinda-vasa', 'https://www.phy.iitb.ac.in/en/content/sai-vinjanampathy', 'https://www.phy.iitb.ac.in/en/research/high-energy-theory', 'https://www.phy.iitb.ac.in/en/research/high-energy-experiments', 'https://www.phy.iitb.ac.in/en/research/condensed-matter-theory', 'https://www.phy.iitb.ac.in/en/research/condensed-matter-experiments', 'https://www.phy.iitb.ac.in/en/research/soft-matter-biophysics-and-nonlinear-dynamics', 'https://www.phy.iitb.ac.in/en/research/optics-and-photonics', 'https://www.phy.iitb.ac.in/en/research/astronomy-cosmology-gravity', 'https://www.phy.iitb.ac.in/en/research/quantum-information-theory', 'https://www.phy.iitb.ac.in/en/staff', 'https://www.phy.iitb.ac.in/en/staff?field_employee_type_tid=2', 'https://www.phy.iitb.ac.in/en/research-facilities', 'https://www.phy.iitb.ac.in/en/curriculum-courses', 'https://www.iitb.ac.in/newacadhome/GuidelinesPhDSynopsispreparation07Jan2016.pdf', 'https://www.iitb.ac.in/newacadhome/mscphd201509Julylatest.pdf', 'https://www.phy.iitb.ac.in/en/undergraduate', 'https://www.phy.iitb.ac.in/en/postgraduate', 'https://www.phy.iitb.ac.in/en/phd', 'https://www.phy.iitb.ac.in/en/jobs/faculty-recruitment', 'https://www.phy.iitb.ac.in/en/jobs/post-doctoral-fellowship', 'https://www.phy.iitb.ac.in/en/jobs/research-associate']
metadata = ['faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'faculty', 'research', 'research', 'research', 'research', 'research', 'research', 'research', 'research', 'staff', 'staff', 'facilities', 'others', 'others', 'others', 'others', 'others', 'others', 'others', 'others', 'others']

# Set the API key for the GenAI library
gemini.configure(api_key="AIzaSyBkXXtG5XeopoPisjR0LGqFdNcy3F_a8eo")

# Function to process the URL and extract the relevant sections(data) based on the category
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

# Function to clean the JSON string by removing comments and extra commas
def clean_json_string(json_string):
    json_string = re.sub(r'//.*', '', json_string)
    json_string = re.sub(r',\s*}', '}', json_string)
    json_string = re.sub(r',\s*]', ']', json_string)
    return json_string

# Function to extract the text between triple quotes, which will be the generated JSON conent
def extract_between_triple_quotes(input_string):
    matches = re.findall(r"```(.*?)```", input_string, re.DOTALL)
    return matches

# Function to generate the structured and meaningful JSON content from the extracted HTML content using Gemini 1.5 pro model
def generate_json_from_text(prompt):
    try:
            model = genai.GenerativeModel("gemini-1.5-pro")
            response = model.generate_content(prompt)
            #print(response)
            return (response)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        

# Function to extract the data from the URLs and save it to a JSON file     
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
        response_ = clean_json_string(extract_between_triple_quotes(response._result.candidates[0].content.parts[0].text)[0][4:])
        print(response_)
        data = json.loads(response_)
        print("data loaded successfully")
        if response:
            if metadata[i] not in major_json:
                major_json[metadata[i]] = []
            major_json[metadata[i]].append(data)
        with open('physics_department_data.json', 'w') as f:
            json.dump(major_json, f, indent=2)
    print("Data successfully saved to 'physics_department_data.json'.")
    
# Call the function to extract the data from the URLs and save it to a JSON file
extract_data(urls,metadata)