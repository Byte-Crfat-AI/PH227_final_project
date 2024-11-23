import requests
from bs4 import BeautifulSoup

def scrape(url):
    try:
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            pretty_html = soup.prettify()
            print("HTML content has been fetched successfully.")
        else:
            print(f"Failed to fetch the page. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the page: {e}")
    return pretty_html
