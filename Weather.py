#!/usr/bin/env python3

import sys
import subprocess
import requests


def weather(city):
    try:
        from bs4 import BeautifulSoup
    except:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'bs4'])
    finally:
        from bs4 import BeautifulSoup
        url = f"https://www.google.com/search?q=Weather in {city}"
        r = requests.get(url)
        s = BeautifulSoup(r.text, "html.parser")
        update = s.find("div", class_="BNeawe").text
        return update+"elcius"


if __name__ == "__main__":
    weather(city=input("Search the city you want to check weather in: "))
