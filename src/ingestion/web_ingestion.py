import requests
from bs4 import BeautifulSoup

def fetch_from_web_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text()
    return {"content": text, "source": url}
