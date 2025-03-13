from bs4 import BeautifulSoup
from flask import request
from flask import (
    Blueprint, request
)

from . import ai
bp = Blueprint('routes', __name__, url_prefix='/')

@bp.post("/")
def take_html():
    raw_data = request.get_data()
    parsed_text = parse_text(raw_data)
    return { "is_hotel": ai().is_hotel(parsed_text)}

def parse_text(raw_data):
    soup = BeautifulSoup(raw_data, features="html.parser")
    return soup.get_text(separator=" ", strip=True)