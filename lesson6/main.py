import requests
from bs4 import BeautifulSoup
import json
import time
import hashlib
import sqlite3

def get_content(url):
    name = hashlib.md5(url.encode('utf-8')).hexdigest()
    try:
        with open(name, 'r', encoding='utf-8') as f:
            content = f.read()
            return content
    except FileNotFoundError:
        try:
            response = requests.get(url)
            print('Request was sent')
            with open(name, 'w', encoding='utf-8') as f:
                f.write(response.text)
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching the URL: {e}")
            return None

def pars_html(url):
    content = get_content(url)

    soup = BeautifulSoup(content, 'lxml')

    urls = []

    sport = soup.find('ul', {'class':'ssrcss-1xxqo5f-Grid e12imr580'})
    cards = sport.find_all('div', {'type': 'article'})
    for card in cards:
        url = card.find('a').get('href')
        url = 'https://www.bbc.com' + url
        urls.append(url)
    result_urls = urls[:5]

    result = []
    for url in result_urls:
        result.append(parse_page(url))

    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

def parse_page(url: str) -> dict:
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    r = requests.get(url, headers={'user-agent': user_agent})

    soup = BeautifulSoup(r.text, 'lxml')

    topics = [topic.text for topic in soup.find_all('a', {'class': 'ssrcss-1ef12hb-StyledLink ed0g1kj0'})]
    return {'Link': url, 'Topics': topics}

def write_sql(data: list) -> None:
    filename = 'result.db'
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()

    sql = """
        CREATE TABLE IF NOT EXISTS sport (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            topics TEXT NOT NULL
        )
    """
    cursor.execute(sql)

    for item in data:
        topics = ', '.join(item['Topics'])
        cursor.execute("""
            INSERT INTO sport (url, topics)
            VALUES (?, ?)
        """, (item['Link'], topics))

    conn.commit()
    conn.close()

def read_json(filename: str) -> list:
    # Чтение данных из JSON-файла
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


if __name__ == '__main__':

    start = time.time()
    pars_html('https://www.bbc.com/sport')
    data = read_json('result.json')
    write_sql(data)
    finish = time.time()
    print('Time',finish - start)
