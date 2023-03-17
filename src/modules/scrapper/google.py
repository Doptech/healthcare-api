import requests
from bs4 import BeautifulSoup

def google_search(query):
    url = "https://www.google.com/search?q=" + query.replace(" ", "+")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = []
    for i in soup.find_all('div', class_='hgKElc'):
        results.append(i.text)
    return results

