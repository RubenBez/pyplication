from bs4 import BeautifulSoup
from flask import request
from pyplication import app

@app.post("/")
def take_html():
    raw_data = request.get_data()
    result = parse_text(raw_data)
    return result

def parse_text(raw_data):
    soup = BeautifulSoup(raw_data, features="html.parser")
    return soup.get_text(strip=True, separator="\n")