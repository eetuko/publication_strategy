import json
import pymongo
import collections
import os
import pandas as pd
import numpy as np


ROOT_PATH = os.path.join(os.getcwd(), 'data')
if not os.path.isdir(ROOT_PATH):
    os.mkdir(ROOT_PATH)

def select_journals_if(low, high):
    allowed_ISSN = []
    # special case : if journals do not have an IF consider it null
    for journal in impactfactors.find():
        try:
            if low <= float(journal['2013/2014']) < high:
                allowed_ISSN.append(journal['ISSN'])
        except:
            if low == 0:
               allowed_ISSN.append(journal['ISSN'])
    return allowed_ISSN

def select_papers(start, end, allowed_ISSN=[]):
    KW = []
    # Counters to evaluate how many do not have correct
    # publication years or keywords list
    i = 0
    j = 0
    # select papers that are not reviews :
    for paper in papers_info.find({'MedlineCitation.Article.PublicationTypeList': {"$nin": ['Review']}}):
        try: 
            if start <= int(paper['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate']['Year']) <= end:
                try:
                    # if list of ISSN provided, assume you want to filter on papers IF
                    if len(allowed_ISSN) > 0: 
                        if paper['MedlineCitation']['Article']['Journal']['ISSN'] in allowed_ISSN:
                            KW.append([str(kw['DescriptorName']) for kw in paper['MedlineCitation']['MeshHeadingList']])
                    else:
                        KW.append([str(kw['DescriptorName']) for kw in paper['MedlineCitation']['MeshHeadingList']])
                except:
                    i += 1
                    pass
        except:
            j += 1
            pass
    return KW, i, j

def save_counter(data, start, end, extra=''):
    '''
    Normalized top 500 keywords counts
    Computed from list of dicts
    Data dumpes to json
    '''
    paper_num = float(len(data))/100000
    KW = []
    for kw_list in data:
        KW.extend(kw_list)
    MostCommon = dict(collections.Counter(KW).most_common(500))
    for key in MostCommon:
         MostCommon[key] /= paper_num
    with open(ROOT_PATH + "/mostcommon_" + str(start) + "_" + str(end) + str(extra) + ".txt", "w") as save:
        json.dump(dict(MostCommon), save)

host_string = "mongodb://localhost"
port = 27017
mongo_client = pymongo.MongoClient(host_string, port)

# get a reference to mongodb 'publishorperish'
mongo_db = mongo_client['publishorperish']

# get a reference to papers collection
papers_info = mongo_db['papers_info']
impactfactors = mongo_db['impactfactors']

## Not optimized, going multiple times over the same data
# Generate top keyword counts by IF and 5 year intervals
for i in range(1985, 2015, 5):
    for low, high in [(0, 5), (5, 15), (15, 100)]:
        allowed_ISSN = select_journals_if(low, high)
        KW, nokeyword, nopubyear = select_papers(i, i + 4, allowed_ISSN)
        save_counter(KW, i, i + 4, extra=str('_IF_' + str(low) + '_' + str(high)))
        print 'no pub year' + str(nopubyear)
        print 'no key word' + str(nokeyword)


# Generate top keyword counts
for i in range(1985, 2015, 5):
    KW, nokeyword, nopubyear = select_papers(i, i + 4)
    save_counter(KW, i, i + 4)
    print 'no pub year' + str(nopubyear)
    print 'no key word' + str(nokeyword)


## One Paper format example :
# {u'MedlineCitation': {u'Article': {u'Abstract': {u'AbstractText': [u'Risk factors associated with LP are frequent in patients older than 60 years old who are hospitalized with pneumonia. The aim of the study was to define the incidence, epidemiological and clinical features of LP in this age group in Northern Israel.',
#      u'The study was prospective and conducted for one year during the period 1.6.1999-31.5.2000. All patients older than 60 years who were hospitalized with community-acquired or nosocomial pneumonia were tested for legionella infection by the urine antigen test (which identifies Legionella pneumophila type I and 14 other Legionella serotype antigens). Data was obtained from each patient regarding risk factors and clinical feature of the disease. The data of patients with LP was compared on a 1:2 ratio to data obtained from a control group of patients with non LP according to age, sex, and week of admission.',
#      u'During the study period 202 patients and 38 patients were hospitalized with community-acquired or nosocomial pneumonia respectively. Overall, 8/240 patients (3.3%) were found to suffer from LP. All patients with LP had community-acquired pneumonia with an incidence of 8/202 (4%). Six of the 8 patients (75%) with LP were hospitalized during June-September. Significant clinical findings in patients with LP as compared to those in the control group, respectively, were: severity score, history of smoking, mental status alteration, respiration rate over 30/minute, respiratory acidosis, hypoxia, and need for mechanical ventilation (P < 0.05 in all). All patients with LP were treated with macrolides, however the death rate was 50% vs 0% in the control group (p < 0.001).',
#      u'In northern Israel, LP is infrequent among patients older than 60 years hospitalized with pneumonia. The disease occurs mostly during the summer in patients with community acquired pneumonia. Patients with LP had unique and more severe clinical features and the death rate was very high inspite of appropriate therapy.']},
#    u'ArticleDate': [],
#    u'ArticleTitle': u'[The epidemiology and clinical features of Legionella pneumonia (LP) in patients older than 60 years old who were hospitalized with pneumonia in northern Israel].',
#    u'AuthorList': [{u'AffiliationInfo': [{u'Affiliation': u'Internal Department of Medicine B, Rappaport School of Medicine, Technion, Haifa.',
#        u'Identifier': []}],
#      u'ForeName': u'G',
#      u'Identifier': [],
#      u'Initials': u'G',
#      u'LastName': u'Ben-Dror'},
#     {u'AffiliationInfo': [],
#      u'ForeName': u'Y',
#      u'Identifier': [],
#      u'Initials': u'Y',
#      u'LastName': u'Mizerizky'},
#     {u'AffiliationInfo': [],
#      u'ForeName': u'G',
#      u'Identifier': [],
#      u'Initials': u'G',
#      u'LastName': u'Viar'},
#     {u'AffiliationInfo': [],
#      u'ForeName': u'M',
#      u'Identifier': [],
#      u'Initials': u'M',
#      u'LastName': u'Zuker'},
#     {u'AffiliationInfo': [],
#      u'ForeName': u'D',
#      u'Identifier': [],
#      u'Initials': u'D',
#      u'LastName': u'Miron'}],
#    u'ELocationID': [],
#    u'Journal': {u'ISOAbbreviation': u'Harefuah',
#     u'ISSN': u'0017-7768',
#     u'JournalIssue': {u'Issue': u'8',
#      u'PubDate': {u'Month': u'Aug', u'Year': u'2002'},
#      u'Volume': u'141'},
#     u'Title': u'Harefuah'},
#    u'Language': [u'HEB'],
#    u'Pagination': {u'MedlinePgn': u'680-2, 763'},
#    u'PublicationTypeList': [u'English Abstract', u'Journal Article']},
#   u'CitationSubset': [u'IM'],
#   u'DateCompleted': {u'Day': u'11', u'Month': u'10', u'Year': u'2002'},
#   u'DateCreated': {u'Day': u'11', u'Month': u'9', u'Year': u'2002'},
#   u'DateRevised': {u'Day': u'15', u'Month': u'11', u'Year': u'2006'},
#   u'GeneralNote': [],
#   u'KeywordList': [],
#   u'MedlineJournalInfo': {u'Country': u'Israel',
#    u'ISSNLinking': u'0017-7768',
#    u'MedlineTA': u'Harefuah',
#    u'NlmUniqueID': u'0034351'},
#   u'MeshHeadingList': [{u'DescriptorName': u'Aged', u'QualifierName': []},
#    {u'DescriptorName': u'Aged, 80 and over', u'QualifierName': []},
#    {u'DescriptorName': u'Community-Acquired Infections',
#     u'QualifierName': [u'epidemiology', u'microbiology']},
#    {u'DescriptorName': u'Cross Infection',
#     u'QualifierName': [u'epidemiology', u'microbiology']},
#    {u'DescriptorName': u'Female', u'QualifierName': []},
#    {u'DescriptorName': u'Humans', u'QualifierName': []},
#    {u'DescriptorName': u'Inpatients',
#     u'QualifierName': [u'statistics & numerical data']},
#    {u'DescriptorName': u'Israel', u'QualifierName': [u'epidemiology']},
#    {u'DescriptorName': u'Legionella pneumophila',
#     u'QualifierName': [u'classification', u'isolation & purification']},
#    {u'DescriptorName': u'Legionellosis',
#     u'QualifierName': [u'epidemiology', u'therapy']},
#    {u'DescriptorName': u"Legionnaires' Disease",
#     u'QualifierName': [u'epidemiology', u'therapy']},
#    {u'DescriptorName': u'Male', u'QualifierName': []},
#    {u'DescriptorName': u'Middle Aged', u'QualifierName': []},
#    {u'DescriptorName': u'Retrospective Studies', u'QualifierName': []},
#    {u'DescriptorName': u'Serotyping', u'QualifierName': []},
#    {u'DescriptorName': u'Treatment Outcome', u'QualifierName': []}],
#   u'OtherAbstract': [],
#   u'OtherID': [],
#   u'PMID': u'12222127',
#   u'SpaceFlightMission': []},
#  u'PubmedData': {u'ArticleIdList': [u'12222127'],
#   u'History': [{u'Day': u'12',
#     u'Hour': u'10',
#     u'Minute': u'0',
#     u'Month': u'9',
#     u'Year': u'2002'},
#    {u'Day': u'12',
#     u'Hour': u'4',
#     u'Minute': u'0',
#     u'Month': u'10',
#     u'Year': u'2002'},
#    {u'Day': u'12',
#     u'Hour': u'10',
#     u'Minute': u'0',
#     u'Month': u'9',
#     u'Year': u'2002'}],
#   u'PublicationStatus': u'ppublish'},
#  u'_id': ObjectId('581500730c1cde65451de755')}
