from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse
from concurrent.futures import ThreadPoolExecutor
from ai.print_progress import printProgressBar
import requests
import os
import os.path

def links_from_booking_com(file, output, cssClass):
    with open(file) as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    urls = []
    for link in soup.find_all(class_=cssClass):
        urlString = link.get('href')
        parsed_url = urlparse(urlString)
        clean_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))
        urls.append(clean_url)
    
    with open(output, "w", encoding="utf-8") as f:
        for url in urls:
            f.write(url + "\n")

def save_html(url):
    try:
        fileName = dir_path + "/raw_hotel/" + url.rsplit('/', 1)[-1]
        if (not os.path.isfile(fileName)):    
            with open(fileName, "x") as f:
                response = requests.get(url, timeout=10)
                f.write(response.text)
    except Exception as e:
        print(f"Failed to extract {url}: {e}")
        return None

def download_pages(link_file):
    # Read URLs from file
    with open(link_file) as f:
        urls = [line.strip() for line in f.readlines()]
    total = len(urls)

    # Run in parallel
    with ThreadPoolExecutor(max_workers=20) as executor:  # Adjust max_workers as needed
        futures = {executor.submit(save_html, url): url for url in urls}
        
        # Track progress
        for i, future in enumerate(futures):
            future.result()
            printProgressBar(i + 1, total)

dir_path = os.path.dirname(os.path.realpath(__file__))

urls_file_name = dir_path + "/uk-booking-urls.txt"
links_from_booking_com(dir_path + "/booking.com-uk-hotels.mhtml", urls_file_name, "a78ca197d0")  
download_pages(urls_file_name)

# Grab random wiki articles