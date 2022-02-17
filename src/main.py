# -*- coding: utf-8 -*-
import csv
from bs4 import BeautifulSoup
import requests
import re
import random
import time


def demo_scrap(query: str, page_start: int,
               page_end: int, output_filename: str) -> None:
    """ scraping google scholar author1 (first & last name), year, title"""

    user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    ]

    papers = []

    for i in range(page_start, page_end):
        idx = 10 * i
        url = f'https://scholar.google.com/scholar?q={query}&start={idx}'

        print(f'Page: {str(i)}')
        print(f'URL: {url}')

        headers = {'User-Agent': random.choice(user_agent_list)}

        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.content, 'lxml')

        if soup:

            for item in soup.select('[data-lid]'):
                try:
                    title = item.select('h3')[0].get_text()
                    elements = item.select('.gs_a')[0].get_text()
                    author1 = elements.replace('-', ',').split(',')[0]
                    year = re.search(r'(\d{4})', elements).group(1)

                    print('---------------------------------------')
                    print(f'title: {title}')
                    print(f'author: {author1}')
                    print(f'year: {year}')

                    paper = [author1, year, title]
                    papers.append(paper)

                except Exception as e:
                    print(f'exception: {str(e)}')

        time.sleep(40)

    pathfile = f'{output_filename}-{page_start}-to-{page_end}.csv'
    with open(pathfile, 'w+', newline='\n') as file:
        write = csv.writer(file)
        write.writerows(papers)


if __name__ == "__main__":
    query = 'hmd+headsets+participant+OR+learner+OR+student+OR+teaching+OR+learning+OR+training+OR+education+"immersive+virtual+reality"+-CAVE&as_ylo=2018&as_yhi=2018'
    page_start = 1
    page_end = 25
    output_filename = 'paperdew-y2018-pg'

    demo_scrap(query, page_start, page_end, output_filename)
