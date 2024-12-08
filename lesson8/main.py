from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
from time import time

def pars():
    driver = webdriver.Chrome()
    max_page = 2

    wait = WebDriverWait(driver, timeout=10)

    result = []

    for page in range(1, max_page + 1):
        url = f'https://jobs.marksandspencer.com/job-search?page={page}'
        driver.get(url)

        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'border-1')))

        jobs = driver.find_elements(By.CLASS_NAME, 'border-1')
        for job in jobs:
            try:
                title = job.find_element(By.TAG_NAME, 'h3').text
                link_element = job.find_element(By.TAG_NAME, 'a')
                href = link_element.get_attribute('href')

                result.append({
                    'title': title,
                    'url': href
                })
            except Exception as e:
                print(f"Error processing job on page {page}: {e}")
                result.append({
                    'title': title,
                    'url': None
                })

    driver.quit()

    with open('result_hw.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    start = time()
    pars()
    finish = time()
    print('Time:', finish - start)
