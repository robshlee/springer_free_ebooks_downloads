import os
import requests
import pandas as pd
import re
from tqdm import tqdm
import time


def download_books(): 
    # grab content table from url
    site_path = 'https://resource-cms.springernature.com/springer-cms/rest/v1/content/17858272/data/v4'
    books = pd.read_excel(site_path)

    # filter for only columns needed 
    df = books[['Book Title', 'DOI URL', 'OpenURL']]
    df.columns = ['title', 'doi_url', 'open_url']

    # progress bar for sanity
    t = tqdm(total=df.shape[0], desc='Epoch', position=0)

    # loop through each title to download
    for book in df.itertuples():
        # rename title to use as file name
        title = book.title.replace(' ', '_')

        # regex magic to generate url to pdf path
        url = re.search('.*\/', book.open_url)
        url = url[0] + 'content/pdf/10.'
        url = url + re.search('10\.(.*)\/', df.iloc[0].doi_url)[1] + '%2F'
        url = url + re.search('([^\/]+)$', book.doi_url)[0] + '.pdf'

        # grab the content
        content = requests.get(url).content
        download_path = os.getcwd() + f'/downloads/{title}.pdf'
        
        # download!
        # open(os.getcwd() + f'/downloads/{title}', 'wb').write(content)
        open(download_path.encode('utf-8'), 'wb').write(content)

        # add count for tqdm progress bar
        t.update(1)

        print(f'Downloaded {title}')

def main():
    download_books()


if __name__ == '__main__':
    # execute only if run as a script
    main()

