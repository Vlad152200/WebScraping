import requests
import re
import hashlib
import json
import html
import xml.etree.ElementTree as ET
import sqlite3
import csv

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
    #titles = [re.sub(r'/<wbr>', '/', vacancy) for vacancy in re.findall(title_pattern, content)]
    titles = [html.unescape(vacancy) for vacancy in re.findall(title_pattern, content)]

    urls = re.findall(url_pattern, content)
    vacancies = [{"title": title, "url": url} for title, url in zip(titles, urls)]
    return  vacancies

def write_json(data: list) -> None:
    filename = 'output.json'

    data = [
        {
            'id':idx,
            'title': item['title'],
            'url': item['url'],
        }
        for idx, item in enumerate(data, start=1)
    ]
    with open(filename, mode='w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def write_sql(data: list) -> None:
    filename = 'output.db'

    conn = sqlite3.connect(filename)
    cursor = conn.cursor()

    sql = """
        create table if not exists vacancies (
            id integer primary key,
            vacancies text,
            url text
        )
    """
    cursor.execute(sql)

    for item in data:
        cursor.execute("""
            insert into vacancies (vacancies, url)
            values (?, ?)
        """, (item['title'], item['url']))

    conn.commit()
    conn.close()

def write_csv(data: list) -> None:
    filename = 'output.csv'

    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Id', 'Title', 'Url'])
        for idx, item in enumerate(data, start=1):
            writer.writerow([idx, item['title'], item['url']])

def write_xml(data: list) -> None:
    filename = 'output.xml'

    root = ET.Element('Vacancies')
    for idx, item in enumerate(data, start=1):
        vacancie = ET.SubElement(root, 'Vacancie')
        ET.SubElement(vacancie, 'id').text = str(idx)
        ET.SubElement(vacancie,'title').text = item['title']
        ET.SubElement(vacancie, 'url').text = item['url']

    tree = ET.ElementTree(root)
    tree.write(filename, encoding='utf-8', xml_declaration=True)

if __name__ == '__main__':
    #example = [{'title': 'Couple concierges/gardiens  H/F', 'url': 'https://www.lejobadequat.com/emplois/262116-couple-concierges-gardiens-f-h-fr'}, {'title': 'Assistant(e) qualité  H/F', 'url': 'https://www.lejobadequat.com/emplois/262115-assistante-qualite-h-f-fr'}, {'title': 'Conducteur d’engins –  H/F', 'url': 'https://www.lejobadequat.com/emplois/262114-conducteur-dengins-h-f-fr'}, {'title': 'Peintre-carrossier  H/F', 'url': 'https://www.lejobadequat.com/emplois/262113-peintre-carrossier-h-f-fr'}, {'title': 'Conducteur d’engins chargeuse-  H/F', 'url': 'https://www.lejobadequat.com/emplois/262112-conducteur-dengins-chargeuse-h-f-fr'}, {'title': 'Assistant(e) qualité  H/F', 'url': 'https://www.lejobadequat.com/emplois/262111-assistante-qualite-h-f-fr'}, {'title': 'Coffreur boiseur  H/F', 'url': 'https://www.lejobadequat.com/emplois/262110-coffreur-boiseur-h-f-fr'}, {'title': 'Assistant paie et RH  H/F', 'url': 'https://www.lejobadequat.com/emplois/262109-assistant-paie-et-rh-h-f-fr'}, {'title': 'Agent de pré-fabrication  H/F', 'url': 'https://www.lejobadequat.com/emplois/262108-agent-de-pre-fabrication-f-h-fr'}, {'title': 'Chef de secteur gms  H/F', 'url': 'https://www.lejobadequat.com/emplois/262106-chef-de-secteur-gms-h-f-fr'}, {'title': 'Chef de secteur gms  H/F', 'url': 'https://www.lejobadequat.com/emplois/262103-chef-de-secteur-gms-h-f-fr'}, {'title': 'Technicien de maintenance  H/F', 'url': 'https://www.lejobadequat.com/emplois/262102-technicien-de-maintenance-h-f-fr'}]
    example = use_re('https://www.lejobadequat.com/emplois')
    write_json(example)
    write_sql(example)
    write_csv(example)
    write_xml(example)
