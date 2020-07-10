"""
Time complexity: 

BEST CASE SCENARIO: O(n^2)
WORST CASE SCENARIO: O(n^m)
"""

import re
import os
import io
import json
import pandas as pd
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
from bs4 import BeautifulSoup

DetectorFactory.seed = 0

file = input("Enter CSV path: ")
CSV = pd.read_csv(file, skiprows=0, header=None)

tekstovi = []
automatskePoruke = []


""" ----------------------------------------- FUNCTIONS ----------------------------------------- """
def detectLanguage(text):
    try:
        return detect(text)
    except LangDetectException:
        return "UNKNOWN"


def tierischer(traveller):
    if re.search(r"(?<=Nachricht).*?(?=Mit)", traveller, re.S) is None:
        return None
    else:
        text = re.search(r"(?<=Nachricht).*?(?=Mit)", traveller, re.S).group(0)

    text = re.sub(r"(?:<[^<>]*>|\s)+", " ", text)
    text = text.strip()
    
    if text == "":
        return None

    language = detectLanguage(text)

    tekstovi.append({
        "text": text,
        "language": language,
        "category": 1
    })


def avtokampi1(traveller):
    if re.search(r"(?<=Sporočilo:).*?(?=S prijaznimi)",  traveller,  re.S) is None:
        return None
    else:
        text = re.search(r"(?<=Sporočilo:).*?(?=S prijaznimi)", traveller, re.S).group(0)

    text = re.sub(r"<[^<]+?>", " ", text)
    text = " ".join(text.split())
    text = text.strip()
    
    if text == "":
        return None

    language = detectLanguage(text)

    tekstovi.append({
        "text": text,
        "language": language,
        "category": 2
    })


def avtokampi2(traveller):
    if re.search(r'(?<=charset=utf-8">).*?(?=Pošiljatelj:)', traveller, re.S) is None:
        return None
    else:
        text = re.search(r'(?<=charset=utf-8">).*?(?=Pošiljatelj:)', traveller, re.S).group(0)

    text = re.sub(r"<[^<]+?>", " ", text)
    text = " ".join(text.split())
    text = text.strip()
    
    if text == "":
        return None

    language = detectLanguage(text)

    tekstovi.append({
        "text": text,
        "language": language,
        "category": 2
    })


def kinderhotel(traveller):
    soup = BeautifulSoup(traveller, "html.parser")

    text = soup("table")[2]
    text = " ".join(text("td")[8].find_all(string=True)[2:])
    text = " ".join(text.split())
    text = text.strip()
    
    if text == "":
        return None

    language = detectLanguage(text)

    tekstovi.append({
        "text": text,
        "language": language,
        "category": 3
    })


def autoBooking(traveller):
    soup = BeautifulSoup(traveller, "html.parser")

    text = " ".join(soup("strong")[0].find_all(string=True))
    text = text.replace('\xa0', "")
    
    if text == "":
        return None

    language = detectLanguage(text)

    automatskePoruke.append({
        "text": text,
        "language": language,
        "category": 4
    })


def booking1(traveller):
    soup = BeautifulSoup(traveller, "html.parser")

    check = " ".join(soup("span")[0].find_all(string=True))

    if re.search(r"Vanjski pošiljatelj", check) is None:
        return None
    else:
        if re.search(r"Vanjski pošiljatelj", check):
            text = " ".join(soup("span")[1].find_all(string=True))
            text = text.replace('\xa0', "")
        else:
            text = " ".join(soup("span")[0].find_all(string=True))
            text = text.replace('\xa0', "")

    if text == "":
        return None

    language = detectLanguage(text)

    tekstovi.append({
        "text": text,
        "language": language,
        "category": 4
    })


def booking2(traveller):
    soup = BeautifulSoup(traveller, "html.parser")

    counter: int = 0

    aa = soup("td")[7]

    while True:
        try:
            bb = aa("td")[5 + counter]
            text = " ".join(bb("td")[1].find_all(string=True))
            text = text.replace('\xa0', "")

            language = detectLanguage(text)
            
            if text == "":
                return None

            tekstovi.append({
                "text": text,
                "language": language,
                "category": 4
            })

        except IndexError:
            break

        counter += 8


def booking3(traveller):
    soup = BeautifulSoup(traveller, "html.parser")

    check = " ".join(soup("div")[0].find_all(string=True))
    
    if re.search(r"Vanjski pošiljatelj / External sender", check) is None:
        return None
    else:
        if re.search(r"Vanjski pošiljatelj / External sender", check):
            text = check[45:]
            text = text.strip()
            text = text.replace('\xa0', "")

        else:
            text = check.strip()
            text = text.replace('\xa0', "")

    if text == "":
        return None

    language = detectLanguage(text)

    tekstovi.append({
        "text": text,
        "language": language,
        "category": 4
    })


def booking4(traveller):
    soup = BeautifulSoup(traveller, "html.parser")

    text = " ".join(soup("b")[0].find_all(string=True))
    text = text.replace('\xa0', "")
    text = text.strip()
    
    if text == "":
        return None

    language = detectLanguage(text)

    tekstovi.append({
        "text": text,
        "language": language,
        "category": 4
    })
    
    
def otochorwacja1(traveller):
    soup = BeautifulSoup(traveller, "html.parser")
    
    text = soup("body")[3].find_all(string=True)[0]
    text = text.replace('\xa0', "")
    text = text.strip()
    
    language = detectLanguage(text)
    
    if text == "":
        return None
    
    tekstovi.append({
        "text": text, 
        "language": language, 
        "category": 5
    })
    
    
def otochorwacja2(traveller):
    pass
""" 
    soup = BeautifulSoup(traveller, "html.parser")
    
    text = soup("p")[0].find_all(string=True)
    
    language = detectLanguage(text)
    
    tekstovi.append({
        "text": text, 
        "language": language, 
        "category": 5
    })
"""


def glamping(traveller):
    soup = BeautifulSoup(traveller, "html.parser")
   
    text = " ".join(soup("div")[0].find_all(string=True))
    
    if re.search(r'Inhalt der Anfrage:[ ]+"(.*?)"',  text) is None:
        return None
    else:
        text = re.search(r'Inhalt der Anfrage:[ ]+"(.*?)"',  text).group(1)

    text = text.replace('\xa0', "")
    text = text.strip()
    
    if text == "":
        return None
    
    language = detectLanguage(text)
    
    tekstovi.append({
        "text": text, 
        "language": language, 
        "category": 6
    })
    
    
def tripadvisor1(traveller):
    soup = BeautifulSoup(traveller,  "html.parser")
    
    text = " ".join(soup.find_all(string=True))
    
    if re.search(r"(?<=Message:).*?(?=Reply Now)",  text) is None:
        return None
    else:
        text = re.search(r"(?<=Message:).*?(?=Reply Now)",  text).group(0)

    text = re.sub(r"[ ]+",  " ",  text)
    text = text.strip()
    
    if text == "":
        return None
    
    language = detectLanguage(text)
    
    tekstovi.append({
        "text": text, 
        "language": language, 
        "category": 7
    })
    
    
def tripadvisor2(traveller):
    soup = BeautifulSoup(traveller,  "html.parser")
    
    text = " ".join(soup.find_all(string=True))
    
    if re.search(r"(?<=Messaggio:).*?(?=Rispondi ora)",  text) is None:
        return None
    else:
        text = re.search(r"(?<=Messaggio:).*?(?=Rispondi ora)",  text).group(0)

    text = re.sub(r"[ ]+",  " ",  text)
    text = text.strip()
    
    if text == "":
        return None
    
    language = detectLanguage(text)
    
    tekstovi.append({
        "text": text, 
        "language": language, 
        "category": 7
    })
    

def tripadvisor3(traveller):
    soup = BeautifulSoup(traveller,  "html.parser")
    
    text = " ".join(soup("div")[1].find_all(string=True))
    
    if re.search(r"(.*?)(?=SUPER TOURS)",  text) is None:
        return None
    else:
        text = re.search(r"(.*?)(?=SUPER TOURS)",  text).group(0)
    
    text = text.replace('\xa0', "")
    text = text.strip()
    
    if text == "":
        return None
    
    language = detectLanguage(text)
    
    tekstovi.append({
        "text": text, 
        "language": language, 
        "category": 7
    })
""" --------------------------------------------------------------------------------------------- """


""" ------------------------------------------ PARSING ------------------------------------------ """
for x in range(len(CSV)):
    total = x # -------------------------------------------------------
    traveller = CSV.iloc[x, 0]

    if re.search(r"tierischer", traveller):
        tierischer(traveller)

    elif re.search(r"avtokampi", traveller):
        if re.search(r"Povpraševanje", traveller):
            avtokampi1(traveller)
        else:
            avtokampi2(traveller)

    elif re.search(r"khotels", traveller):
        kinderhotel(traveller)

    elif re.search(r"booking\.com", traveller):
        if re.search(r"Review proof of charge|Review claim and respond", traveller):
            autoBooking(traveller)
        elif re.search(r"This guest received an automatic reply", traveller):
            booking1(traveller)
        elif re.search(r"Please be aware that the guests are expected to arrive today.", traveller):
            booking2(traveller)
        elif re.search(r"MsoNormal", traveller):
            booking3(traveller)
        elif re.search(r"Guest Q&", traveller):
            booking4(traveller)

    elif re.search(r"otochorwacja",  traveller):
        if re.search(r"[-]+ Proslijeđena poruka [-]+",  traveller):
            otochorwacja2(traveller)
        else:
            otochorwacja1(traveller)
    
    elif re.search(r"glamping\.info",  traveller):
        glamping(traveller)

    elif re.search(r"tripadvisor",  traveller):
        if re.search(r"reservations@valamar\.com",  traveller):
            tripadvisor1(traveller)
        elif re.search(r"camping@valamar\.com",  traveller):
            tripadvisor2(traveller)
        elif re.search(r"SUPER TOURS",  traveller):
            tripadvisor3(traveller)

    else:
        continue
""" --------------------------------------------------------------------------------------------- """

""" ----------------------------- CREATE FILES FOR STORING STUFF ----------------------------- """
dataText = open("dataText.json",  "w")
dataAutomated = open("dataAutomated.json",  "w")

dt = open("dataText.json")
dtPath = os.path.realpath(dt.name)

da = open("dataAutomated.json")
daPath = os.path.realpath(da.name)

with io.open(dtPath,  "w",  encoding="utf8") as f:
    json.dump(tekstovi,  f,  indent=4,  ensure_ascii=False)
    
with io.open(daPath,  "w",  encoding="utf8") as f:
    json.dump(automatskePoruke,  f,  indent=4,  ensure_ascii=False)
""" --------------------------------------------------------------------------------------------- """
