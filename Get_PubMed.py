from Bio import Entrez
import json
import pymongo

def number_of_entries(query):
    Entrez.email = 'mikael@koutero.name'
    handle = Entrez.egquery(term=query)
    record = Entrez.read(handle)
    for row in record["eGQueryResult"]:
        if row["DbName"]=="pubmed":
            entries_num = row["Count"]
    return int(entries_num)

# https://marcobonzanini.com/2015/01/12/searching-pubmed-with-python/
def search(query, retstart):
    Entrez.email = 'mikael@koutero.name'
    handle = Entrez.esearch(db='pubmed', 
                            sort='relevance', 
                            retmode='xml',
                            retstart=retstart,
                            retmax=100000, 
                            term=query)
    results = Entrez.read(handle)
    return results

def fetch_details(id_list,retstart):
    ids = ','.join(id_list)
    Entrez.email = 'mikael@koutero.name'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           retstart=retstart,
                           retmax=10000,
                           id=ids)
    results = Entrez.read(handle)
    return results

if __name__ == '__main__':
    entries_num = number_of_entries('bacteria')

    host_string = "mongodb://localhost"
    port = 27017
    mongo_client = pymongo.MongoClient(host_string, port)

    # get a reference to mongodb 'publishorperish'
    mongo_db = mongo_client['publishorperish']

    # get a reference to papers collection
    papers_info = mongo_db['papers_info']

    # number of entries :1929202
    for x in range(0, entries_num, 100000):
        results = search(query='bacteria',retstart=x)
        id_list = results['IdList']
        for y in range(0, len(id_list), 10000):
            papers = fetch_details(id_list=id_list,retstart=y)
            for i, paper in enumerate(papers):
                papers_info.insert_one(papers[i])

# mongodb fiddling, just in case any duplicate
# db.papers_info.createIndex( {"MedlineCitation.PMID": 1}, {unique: true, dropDups: true} )
