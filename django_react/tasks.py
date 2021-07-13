#from .celery import app
import requests
from bs4 import BeautifulSoup


# app.task()
def count(start, end, postD, commentD):
    url = 'http://localhost:8000/api/lead'
    page = requests.get(url)
    page = page.json() # List[dict()]
    for content in page:
        if content['']
    print(len(page.json()))
