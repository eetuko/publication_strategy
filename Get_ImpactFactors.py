import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import pymongo
import string

def htmltable_to_df(table):
    records = []
    for tr in table.findAll("tr"):
        record = []
        for td in tr.findAll("td"):
            record.append(str(td.text))
        records.append(record)
    return pd.DataFrame(data=records[1:], columns=records[0])    


# https://www.snip2code.com/Snippet/712624/Convert-a-pandas-dataframe-to-a-json-blo/
def to_json(df):
    d = [ 
        dict([
            (colname, row[i]) 
            for i,colname in enumerate(df.columns)
        ])
        for row in df.values
    ]
    return d


if __name__ == '__main__':
    listofletters = ['']
    listofletters.extend(['_' + x for x in list(string.ascii_uppercase)[1:]])
    for letter in listofletters:
        url = "http://www.citefactor.org/journal-impact-factor-list-2014" + str(letter) + ".html"
        r = requests.get(url)

        soup = BeautifulSoup(r.text, "lxml")
        impactfactorsource = soup.find("caption", text="Impact Factor 2014").find_parent("table")
        json_data = to_json(htmltable_to_df(impactfactorsource))

        host_string = "mongodb://localhost"
        port = 27017
        mongo_client = pymongo.MongoClient(host_string, port)

        # get a reference to mongodb 'publishorperish'
        mongo_db = mongo_client['publishorperish']
        # get a reference to impactfactors
        impactfactors = mongo_db['impactfactors']
        impactfactors.insert_many(json_data)


