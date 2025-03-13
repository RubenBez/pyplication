from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse
from concurrent.futures import ThreadPoolExecutor
from ai.print_progress import printProgressBar
import requests
import os
import os.path
import csv

current_dir = os.path.dirname(os.path.realpath(__file__))

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
            printProgressBar(i + 1, total, "Downloading HTML - " + link_file)

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

def extract_text(file):
    """Extracts text from a webpage file"""
    try:
        with open(file) as f:
            text = f.read()
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text(separator=" ", strip=True)
    except Exception as e:
        print(f"Failed to extract {file}: {e}")
        return None

def generate_training_data(raw_hotel_dir, raw_non_hotel_dir):
    hotel_files = os.listdir(raw_hotel_dir)
    non_hotel_files = os.listdir(raw_non_hotel_dir)
    
    # Create CSV file
    with open(current_dir + "/training_data.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, lineterminator=";\r\n")
        # Label 1 = Hotel data
        # Label 0 = Not hotel data
        writer.writerow(["file", "text", "label"])  # Header row
        
        # Process hotel pages
        for i, file in enumerate(hotel_files):
            text = extract_text(raw_hotel_dir + "/" + file)
            printProgressBar(i + 1, len(hotel_files), "Hotel Training Data...")
            if text:
                writer.writerow([file, text, 1])

        # Process non-hotel pages
        for i, file in enumerate(non_hotel_files):
            text = extract_text(raw_non_hotel_dir + "/" + file)
            printProgressBar(i + 1, len(non_hotel_files), "Non-Hotel Training Data...")
            if text:
                writer.writerow([file, text, 0])

urls_file_name = current_dir + "/uk-booking-urls.txt"
links_from_booking_com(current_dir + "/booking.com-uk-hotels.mhtml", urls_file_name, "a78ca197d0")  
download_pages(urls_file_name, current_dir + "/raw_hotel")

grab_random_wiki_article()

# Create training data
generate_training_data(current_dir + "/raw_hotel", current_dir + "/raw_not_hotel")