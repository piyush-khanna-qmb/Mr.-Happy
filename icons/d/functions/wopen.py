import requests
from bs4 import BeautifulSoup

def wopen(app):
    sess = requests.Session()
    def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a', {'jsname': 'UWckNb'})
            return [link.get('href') for link in links]

    def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}
            response = sess.get(url, headers=headers)

            if response.status_code == 200:
                return response.text
            
            else:
                print("Failed to retrieve search results.")
            return None

    html = search_google(app)

    if html:
        link = extract_links(html)[0]
        return link
if __name__ == "__main__":
    print(wopen("google"))