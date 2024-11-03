import requests
from bs4 import BeautifulSoup
import re
import time
import json

url = 'https://www.phy.iitb.ac.in/en/faculty'
reqs = requests.get(url, verify=False)
soup = BeautifulSoup(reqs.text, 'html.parser')

#List of all the URLs on the page
urls = []
for link in soup.find_all('a', href=True):
    href = link.get('href')
    full_url = href if href.startswith('http') else url + href
    urls.append(full_url)
print(urls)
#Function to scrape data from a URL
def scrape_data(url):
    try:
        response = requests.get(url, verify=False)
        page_content = BeautifulSoup(response.text, 'html.parser')
        title = page_content.title.string if page_content.title else 'No title'
        paragraphs = page_content.find_all(['p', 'h1', 'h2', 'h3', 'li'])
        text_content = '\n'.join([para.get_text() for para in paragraphs])
        clean_text = re.sub(r'\s+', ' ', text_content).strip()
        return {'url': url, 'title': title, 'content': clean_text}
    except requests.exceptions.RequestException as e:
        return None

scraped_data = []
for url in urls:
    if len(scraped_data) >= 5:
        break
    scraped_content = scrape_data(url)
    if scraped_content:
        scraped_data.append(scraped_content)
    time.sleep(1)

with open('faculty_scraped_data.json', 'w') as f:
    json.dump(scraped_data, f, indent=2)