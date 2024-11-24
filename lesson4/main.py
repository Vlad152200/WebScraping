import requests
import re
import hashlib
import json

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

def use_re(url):
    content = get_content(url)
    title_pattern = r'<h3 class="jobCard_title m-0">(.+?)<\/h3>'
    url_pattern = r'<a href="(https://www\.lejobadequat\.com/emplois/[^"]+)"'

    titles = [re.sub(r'/<wbr>', '/', vacancy) for vacancy in re.findall(title_pattern, content)]
    urls = re.findall(url_pattern, content)

    vacancies = [{"title": title, "url": url} for title, url in zip(titles, urls)]

    result = json.dumps(vacancies, indent=4, ensure_ascii=False)
    print(result)

if __name__ == '__main__':
    use_re('https://www.lejobadequat.com/emplois')
