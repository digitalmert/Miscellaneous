import requests
import math
from bs4 import BeautifulSoup
from decimal import Decimal
import pandas as pd

##fileUrl: location of your word list
##saveUrl: location to write the final file
fileUrl = "gre_words.txt"
saveUrl = "gre/words_to_study.txt"

with open(fileUrl) as f:
    content = f.readlines()
content = [x.strip() for x in content]
content_len = len(content)

counter = 0
findings ={'Word':[], 'Definition':[], 'Example':[], 'Synonym':[], 'Antonym':[]}

for word in content:
    counter = counter + 1
    example_url = requests.get("https://en.oxforddictionaries.com/thesaurus/" + word)
    definition_url = requests.get("https://en.oxforddictionaries.com/definition/" + word)

    soup_examp = BeautifulSoup(example_url.content, 'html.parser')
    soup_def = BeautifulSoup(definition_url.content, 'html.parser')

    ##Fetching meaning
    try:
        meaning = soup_def.find('span', class_='ind').get_text()
    except:
        meaning = ""
        print("Word: "+word + "Not Found..."),

    ##Fetching example
    try:
        example = soup_examp.find('span', class_='example').get_text()
    except: 
        example = ""
        print("example: " + word + "Not Found..."),

    ##Fetching synonym
    try:
        synonym = soup_examp.find('span', class_='syn').get_text()
    except:
        synonym = ""
        print("synonym: " + word + "Not Found..."),

    ##Fetching antonym
    try:
        antonym = soup_examp.find('span', class_='ant').get_text()
    except:
        antonym = ""
        print("antonym: " + word + "Not Found..."),

    print("Percent Done: " + str(round(Decimal(counter*1.0/content_len),2)) + ", Word: " + word + ", Meaning: "+meaning),

    findings['Word'].append(word)
    findings['Definition'].append(meaning)
    findings['Example'].append(example)
    findings['Synonym'].append(synonym)
    findings['Antonym'].append(antonym)

pd.DataFrame(data=findings).to_csv(saveUrl, columns=['Word','Definition','Example','Synonym','Antonym'], index=False)






