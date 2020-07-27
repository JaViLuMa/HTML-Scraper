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
        text = text.capitalize()
        return detect(text)
    
    except LangDetectException:
        return None


def removeUnnecessaryStuff(text):
    text = re.sub(r'\s+([?.!"])', r"\1", text)
    text = re.sub(r"[\n]+| {2,}", " ", text)
    text = text.strip()
    
    return text


def possiblyRemoveRepliesAndOtherStuff(text):
    text = re.sub(r"\b[Vv]on:.*|\b[Ff]rom:.*|\b[Oo]d:.*|\b[Dd]a:.*|\b[Ee].[Mm][Aa][Ii][Ll]|CMS.*",  "",  text)
    text = re.sub(r"[<>\[\]]|^[-]+|[-]+$",  "",  text)
    text = re.sub(r"[*]+|[=]+.*?",  "",  text)
    text = re.sub(r'((http|https)\:\/\/)?[A-z0-9\.\/\?\:@\-_=#]+\.([A-z]){2,6}([A-z0-9\.\&\/\?\:@\-_=#])*', "", text)
    text = re.sub(r"[Ss]ent from my .*|[Vv]on meinem .*|[Tt]rimis de pe .*|[Ii]nviato da .*|[Ss]endt fra min .*|[Vv]erstuurd vanaf mijn .*|[Oo]doslané z .*",  "",  text)
    text = text.strip()
    
    return text


def textChecker(text):
    if len(text.split()) < 5:
        return None
    else:
        return text


def textAppender(text, language, category):
    tekstovi.append({
        "text": text,
        "language": language,
        "intent": "NADODATI",
        "category": category
    })


def automatedTextAppender(text, language, category):
    automatskePoruke.append({
        "text": text,
        "language": language,
        "intent": "NADODATI",
        "category": category
    })


def tierischer(traveller):
    if re.search(r"(?<=Nachricht).*?(?=Mit)", traveller, re.S) is None:
        return None
    else:
        text = re.search(r"(?<=Nachricht).*?(?=Mit)", traveller, re.S).group(0)
    
    text = re.sub(r"(?:<[^<>]*>|\s)+", " ", text)
    
    if text == "" or "Interessen:":
        return None
    
    text = removeUnnecessaryStuff(text)
    language = detectLanguage(text)
    text = textChecker(text)
    category = 1
    
    if text is None:
        return None
    
    if language is None:
        return None

    textAppender(text=text, language=language, category=category)


def avtokampi1(traveller):
    if re.search(r"(?<=Sporočilo:).*?(?=S prijaznimi)",  traveller,  re.S) is None:
        return None
    else:
        text = re.search(r"(?<=Sporočilo:).*?(?=S prijaznimi)", traveller, re.S).group(0)
    
    text = re.sub(r"<[^<]+?>", " ", text)
    text = " ".join(text.split())
    text = text.replace("*** Vanjski pošiljatelj / External sender ***",  "")
    
    if text == "":
        return None
    
    text = removeUnnecessaryStuff(text)
    language = detectLanguage(text)
    text = textChecker(text)
    category = 2
    
    if text is None:
        return None
    
    if language is None:
        return None
    
    textAppender(text=text, language=language, category=category)


def avtokampi2(traveller):
    if re.search(r'(?<=charset=utf-8">).*?(?=Pošiljatelj:)', traveller, re.S) is None:
        return None
    else:
        text = re.search(r'(?<=charset=utf-8">).*?(?=Pošiljatelj:)', traveller, re.S).group(0)
    
    text = re.sub(r"<[^<]+?>", " ", text)
    text = " ".join(text.split())
    text = text.replace("*** Vanjski pošiljatelj / External sender ***",  "")
    
    if text == "":
        return None
    
    text = removeUnnecessaryStuff(text)
    language = detectLanguage(text)
    text = textChecker(text)
    category = 2
    
    if text is None:
        return None

    if language is None:
        return None
    
    textAppender(text=text, language=language, category=category)


def kinderhotel(traveller):
    soup = BeautifulSoup(traveller, "html.parser")
    
    try:
        text = soup("table")[2]
        text = " ".join(text("td")[8].find_all(string=True)[2:])
    except IndexError:
        return None
    
    text = " ".join(text.split())
    
    if text == "":
        return None
    
    text = removeUnnecessaryStuff(text)
    language = detectLanguage(text)
    text = textChecker(text)
    category = 3
    
    if text is None:
        return None
    
    if language is None:
        return None
    
    textAppender(text=text, language=language, category=category)


def autoBooking(traveller):
    soup = BeautifulSoup(traveller, "html.parser")
    
    try:
        text = " ".join(soup("strong")[0].find_all(string=True))
    except IndexError:
        return None
    
    text = text.replace('\xa0', "")
    
    if text == "":
        return None
    
    text = removeUnnecessaryStuff(text)
    language = detectLanguage(text)
    text = textChecker(text)
    category = 4
    
    if text is None:
        return None
    
    if language is None:
        return None
    
    automatedTextAppender(text=text, language=language, category=category)


def booking1(traveller):
    soup = BeautifulSoup(traveller, "html.parser")
    
    try:
        check = " ".join(soup("span")[0].find_all(string=True))
    except IndexError:
        return None
    
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
    
    text = removeUnnecessaryStuff(text)
    language = detectLanguage(text)
    text = textChecker(text)
    category = 4
    
    if text is None:
        return None
    
    if language is None:
        return None
    
    textAppender(text=text, language=language, category=category)


def booking2(traveller):
    soup = BeautifulSoup(traveller, "html.parser")
    
    counter: int = 0
    
    try:
        aa = soup("td")[7]
    except IndexError:
        return None
    
    while True:
        try:
            try:
                bb = aa("td")[5 + counter]
                text = " ".join(bb("td")[1].find_all(string=True))
            except IndexError:
                return None
            
            text = text.replace('\xa0', "")
            
            text = removeUnnecessaryStuff(text)
            language = detectLanguage(text)
            text = textChecker(text)
            category = 4
            
            if text is None:
                return None
            
            if language is None:
                return None
            
            if text == "":
                return None
            
            textAppender(text=text, language=language, category=category)
        
        except IndexError:
            break
    
        counter += 8


def booking3(traveller):
    soup = BeautifulSoup(traveller, "html.parser")
    
    try:
        check = " ".join(soup("div")[0].find_all(string=True))
    except IndexError:
        return None
    
    if re.search(r"Vanjski pošiljatelj / External sender", check) is None:
        return None
    else:
        if re.search(r"Vanjski pošiljatelj / External sender", check):
            text = check[45:]
            text = text.replace('\xa0', "")
        
        else:
            text = check.strip()
            text = text.replace('\xa0', "")

    if text == "":
        return None
    
    text = removeUnnecessaryStuff(text)
    language = detectLanguage(text)
    text = textChecker(text)
    category = 4
    
    if text is None:
        return None
    
    if language is None:
        return None
    
    textAppender(text=text, language=language, category=category)


def booking4(traveller):
    soup = BeautifulSoup(traveller, "html.parser")
    
    try:
        text = " ".join(soup("b")[0].find_all(string=True))
    except IndexError:
        return None
    
    text = text.replace('\xa0', "")
    
    if text == "":
        return None
    
    text = removeUnnecessaryStuff(text)
    language = detectLanguage(text)
    text = textChecker(text)
    category = 4
    
    if text is None:
        return None
    
    if language is None:
        return None
    
    textAppender(text=text, language=language, category=category)


def otochorwacja(traveller):
    soup = BeautifulSoup(traveller, "html.parser")
    
    try:
        text = soup("body")[3].find_all(string=True)[0]
    except IndexError:
        return None
    
    text = text.replace('\xa0', "")
    
    if text == "":
        return None
    
    text = removeUnnecessaryStuff(text)
    language = detectLanguage(text)
    text = textChecker(text)
    category = 5
    
    if text is None:
        return None
    
    if language is None:
        return None
    
    textAppender(text=text, language=language, category=category)


def glamping(traveller):
    soup = BeautifulSoup(traveller, "html.parser")
   
    try:
       text = " ".join(soup("div")[0].find_all(string=True))
    except IndexError:
       return None
    
    if re.search(r'Inhalt der Anfrage:[ ]+"(.*?)"',  text) is None:
        return None
    else:
        text = re.search(r'Inhalt der Anfrage:[ ]+"(.*?)"',  text).group(1)
    
    text = text.replace('\xa0', "")
    
    if text == "":
        return None
    
    text = removeUnnecessaryStuff(text)    
    language = detectLanguage(text)
    text = textChecker(text)
    category = 6
    
    if text is None:
        return None
    
    if language is None:
        return None
    
    textAppender(text=text, language=language, category=category)


def tripadvisor1(traveller):
    soup = BeautifulSoup(traveller,  "html.parser")
    
    text = " ".join(soup.find_all(string=True))
    
    if re.search(r"(?<=Message:).*?(?=Reply Now)",  text) is None:
        return None
    else:
        text = re.search(r"(?<=Message:).*?(?=Reply Now)",  text).group(0)
    
    text = re.sub(r"[ ]+",  " ",  text)
    
    if text == "":
        return None
    
    text = removeUnnecessaryStuff(text)    
    language = detectLanguage(text)
    text = textChecker(text)
    category = 7
    
    if text is None:
        return None
    
    if language is None:
        return None
    
    textAppender(text=text, language=language, category=category)


def tripadvisor2(traveller):
    soup = BeautifulSoup(traveller,  "html.parser")
    
    text = " ".join(soup.find_all(string=True))
    
    if re.search(r"(?<=Messaggio:).*?(?=Rispondi ora)",  text) is None:
        return None
    else:
        text = re.search(r"(?<=Messaggio:).*?(?=Rispondi ora)",  text).group(0)
    
    text = re.sub(r"[ ]+",  " ",  text)
    
    if text == "":
        return None
    
    text = removeUnnecessaryStuff(text)    
    language = detectLanguage(text)
    text = textChecker(text)
    category = 7
    
    if text is None:
        return None
    
    if language is None:
        return None
    
    textAppender(text=text, language=language, category=category)


def tripadvisor3(traveller):
    soup = BeautifulSoup(traveller,  "html.parser")
    
    try:
        text = " ".join(soup("div")[1].find_all(string=True))
    except IndexError:
        return None
    
    if re.search(r"(.*?)(?=SUPER TOURS)",  text) is None:
        return None
    else:
        text = re.search(r"(.*?)(?=SUPER TOURS)",  text).group(0)
    
    text = text.replace('\xa0', "")
    
    if text == "":
        return None
    
    text = removeUnnecessaryStuff(text)    
    language = detectLanguage(text)
    text = textChecker(text)
    category = 7
    
    if text is None:
        return None
    
    if language is None:
        return None
    
    textAppender(text=text, language=language, category=category)


def others1(traveller):
    soup = BeautifulSoup(traveller,  "html.parser")
    
    text = " ".join(soup.find_all(string=True))
    text = re.sub(r".*?-->",  "",  text)
    text = text.replace('\xa0', "")
    text = re.sub(r"[-]+Original.*",  "",  text)
    text = re.sub(r"\S*@\S*\s?",  "",  text)
    text = text.replace("*** Vanjski pošiljatelj / External sender ***",  "")
    text = text.replace("Vanjski pošiljatelj / External sender",  "")
    
    text = possiblyRemoveRepliesAndOtherStuff(text)
    text = removeUnnecessaryStuff(text)
    language = detectLanguage(text)
    text = textChecker(text)
    category = 0
    
    if text is None:
        return None
    
    if language is None:
        return None
    
    textAppender(text=text, language=language, category=category)


def others2(traveller):
    soup = BeautifulSoup(traveller,  "html.parser")
    
    try:
        aa = soup("span")[1].find_all(string=True)
    except IndexError:
        return None
    
    for x in range(len(aa)):
        if re.search(r"SUBJECT",  aa[x]):
            bb = x
        else:
            return None
    
    del aa[:bb + 1]
    
    text = " ".join(aa)
    text = text.replace('\xa0', "")
    text = re.sub(r"[-]+Original.*",  "",  text)
    text = re.sub(r"\S*@\S*\s?",  "",  text)
    text = text.replace("*** Vanjski pošiljatelj / External sender ***",  "")
    text = text.replace("Vanjski pošiljatelj / External sender",  "")
    
    text = possiblyRemoveRepliesAndOtherStuff(text)
    text = removeUnnecessaryStuff(text)
    language = detectLanguage(text)
    text = textChecker(text)
    category = 0
    
    if text is None:
        return None
    
    if language is None:
        return None
    
    textAppender(text=text, language=language, category=category)
""" --------------------------------------------------------------------------------------------- """


""" ------------------------------------------ PARSING ------------------------------------------ """
for x in range(len(CSV)):
    traveller = CSV.iloc[x, 0]
    
    total = x + 1
    
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
        if re.search(r"[-]+ Proslijeđena poruka [-]+",  traveller) is None:
            otochorwacja(traveller)
    
    elif re.search(r"glamping\.info",  traveller):
        glamping(traveller)
    
    elif re.search(r"tripadvisor",  traveller):
        if re.search(r"reservations@valamar\.com",  traveller):
            tripadvisor1(traveller)
        elif re.search(r"camping@valamar\.com",  traveller):
            tripadvisor2(traveller)
        elif re.search(r"SUPER TOURS",  traveller):
            tripadvisor3(traveller)
    
    elif re.search(r"Microsoft Exchange Server",  traveller):
        if re.search(r"[_]+", traveller) or re.search(r"This notification is only to inform",  traveller) or re.search(r"camping.info",  traveller):
            continue
        elif re.search(r"MOLIM PREUZMITE MAIL", traveller) is None:
            others1(traveller)
        elif re.search(r"MOLIM PREUZMITE MAIL",  traveller):
            others2(traveller)
        else:
            continue
    
    else:
        continue
""" --------------------------------------------------------------------------------------------- """

""" ----------------------------- CREATE FILES FOR STORING STUFF ----------------------------- """
if not tekstovi:
    pass
else:
    tekstovi = [dict(t) for t in {tuple(d.items()) for d in tekstovi}]
    
    dataText = open("dataText.json",  "w")
    
    dt = open("dataText.json")
    dtPath = os.path.realpath(dt.name)
    
    with io.open(dtPath,  "w",  encoding="utf8") as f:
        json.dump(tekstovi,  f,  indent=4,  ensure_ascii=False)

if not automatskePoruke:
    pass
else:
    automatskePoruke = [dict(t) for t in {tuple(d.items()) for d in automatskePoruke}]
    
    dataAutomated = open("dataAutomated.json",  "w")
    
    da = open("dataAutomated.json")
    daPath = os.path.realpath(da.name)
    
    with io.open(daPath,  "w",  encoding="utf8") as f:
        json.dump(automatskePoruke,  f,  indent=4,  ensure_ascii=False)
""" --------------------------------------------------------------------------------------------- """
