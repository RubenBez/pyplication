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

def save_html(url, folder):
    try:
        fileName = folder + "/" + url.rsplit('/', 1)[-1]
        if (not os.path.isfile(fileName)):    
            with open(fileName, "x") as f:
                response = requests.get(url, timeout=10)
                f.write(response.text)
    except Exception as e:
        print(f"Failed to extract {url}: {e}")
        return None

def download_pages(link_file, save_dir):
    # Create the save_dir if it doesn't exists
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # Read URLs from file
    with open(link_file) as f:
        urls = [line.strip() for line in f.readlines()]
    total = len(urls)

    # Run in parallel
    with ThreadPoolExecutor(max_workers=20) as executor:  # Adjust max_workers as needed
        futures = {executor.submit(save_html, url, save_dir): url for url in urls}
        
        # Track progress
        for i, future in enumerate(futures):
            future.result()
            printProgressBar(i + 1, total)

current_dir = os.path.dirname(os.path.realpath(__file__))

urls_file_name = current_dir + "/uk-booking-urls.txt"
links_from_booking_com(current_dir + "/booking.com-uk-hotels.mhtml", urls_file_name, "a78ca197d0")  
download_pages(urls_file_name, current_dir + "/raw_hotel")

def get_redirect_url(url):
    try:
        response = requests.get(url, allow_redirects=True, timeout=5)
        print(response.url)
        return response.url
    except requests.RequestException as e:
        return f"Error: {e}"

# Grab random wiki articles
def grab_random_wiki_article():    
    cache_file = current_dir + "/wiki-links.txt"
    # If we don't have a wiki links, make a new one
    if not os.path.isfile(cache_file):
        total = 500
        links = []
        # Get links
        with ThreadPoolExecutor(max_workers=20) as executor:
            future_to_url = {executor.submit(get_redirect_url, url): url for url in ["https://en.wikipedia.org/wiki/Special:Random"] * total}
            for i, future in enumerate(future_to_url):
                final_url = future.result()
                links.append(final_url)
        # Save Links
        with open(cache_file, "w") as f:
            for link in links:
                f.write(link + "\n")
        
    download_pages(cache_file, current_dir + "/raw_not_hotel")

grab_random_wiki_article()