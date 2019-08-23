from bs4 import BeautifulSoup
import requests
import urllib3
import shutil
import os
import json
import time

# Hiding InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Utility function to download files
def downloadFile(url, path, fileName):
    http = urllib3.PoolManager()
    if not os.path.exists(path):
        os.makedirs(path)
    path = path + fileName
    with http.request('GET', url, preload_content=False) as r, open(path, 'wb') as out_file:
        shutil.copyfileobj(r, out_file)

# Generating metaData as json
def createMetaData(pdf, path, fileName):
    metaData = {}
    metaData["url"] = pdf
    metaData["title"] = fileName
    metaData["time"] = time.ctime()

    jsonName = fileName.split('.')[0] + '.json'
    with open(os.path.join(path,jsonName), 'w') as f:
            json.dump(metaData, f, sort_keys=False, indent=4, ensure_ascii=False)

# Scraping url and getting pdfs
def scrape(url):
    baseUrl = url.split('/')[2]
    folder = url.split('/')[-2]

    page = requests.get(url)
    data = page.text
    soup = BeautifulSoup(data, 'html.parser')

    pdfs = []
    for idx, link in enumerate(soup.findAll('a')):
        link = link.get('href')
        try:
            if link.endswith('.pdf'):
                if link.startswith('..'):
                    link = 'https://' + baseUrl + link[2::]
                pdfs.append(link)
        except:
            # If link.get('href') returns None
            pass
    currentDir = os.getcwd()
    sep = os.sep
    for pdf in pdfs:
        fileName = pdf.split('/')[-1]
        path = currentDir + sep + folder + sep
        downloadFile(pdf, path, fileName)
        createMetaData(pdf, path, fileName)

# List of URLs to scrape
urls = [
        "https://www.privacy.gov.ph/data-privacy-act-primer/",
        "https://www.privacy.gov.ph/memorandum-circulars/",
        "https://www.privacy.gov.ph/advisories/",
        "https://www.privacy.gov.ph/advisory-opinions/",
        "https://www.privacy.gov.ph/commission-issued-orders/"
        ]

for url in urls:
    scrape(url)
