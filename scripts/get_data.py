from Bio import Entrez
import pandas as pd


def search(query):
    Entrez.email = "lcsmriti@gmail.com"
    handle = Entrez.esearch(db = 'pubmed',
                            sort = 'relevance',
                            retmax = '10000',
                            retmode = 'xml',
                            term = query)
    results = Entrez.read(handle)
    return results

studies = search("Leprosy")

# getting the id list for all the studies
Id_list = studies['IdList']


# fetch the details for all retreived ID lists
def fetch_deets(id_list):
    ids = ",".join(id_list)
    Entrez.email = "lcsmriti@gmail.com"
    handle = Entrez.efetch(db = 'pubmed',
                         retmode = 'xml',
                         id =ids)
    results = Entrez.read(handle)
    return results
papers = fetch_deets(Id_list)

#building the dataframe

title_list=[]
abstract_list =[]
journal_list=[]
language_list =[]
publication_type_list=[]
pubdate_year_list=[]

papers = fetch_deets(Id_list)


for i, paper in enumerate(papers['PubmedArticle']):
    try:
        title_list.append(paper['MedlineCitation']['Article']['ArticleTitle'])
    except:
        title_list.append('No title')
    try:
        abstract_list.append(paper['MedlineCitation']['Article']['Abstract']['AbstractText'][0])
    except:
        abstract_list.append('No Abstract')
    journal_list.append(paper['MedlineCitation']['Article']['Journal']['Title'])
    language_list.append(paper['MedlineCitation']['Article']['Language'][0])
    publication_type_list.append(paper['MedlineCitation']['Article']['PublicationTypeList'][0])
    
    try:
        pubdate_year_list.append(paper['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate']['Year'])
    except:
        pubdate_year_list.append('No Data')
    

tdf = pd.DataFrame(list(zip(title_list,
                            abstract_list,
                            journal_list,
                            publication_type_list,
                            language_list,pubdate_year_list)),
                            columns=['title','abstract','journal','publication_type','language','publication_year'])

tdf.to_csv("total_pm.csv",index=False)





