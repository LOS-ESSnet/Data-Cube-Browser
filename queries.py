from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

# TODO cache ?
PLOSH_URL = "http://hackathon2018.ontotext.com/repositories/plosh"
SCOTT_URL = "https://statistics.gov.scot/sparql"

def get_endpoints_list():
    return [
        {"label": "PLOSH", "value": PLOSH_URL},
        {"label": "Scotland machin", "value": SCOTT_URL}
        ]

def query_datasets(target_url):
    QUERY = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX qb: <http://purl.org/linked-data/cube#>
    PREFIX mes: <http://id.insee.fr/meta/mesure/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 

    SELECT ?label ?comment ?dataset_uri  where {           
        ?dataset_uri a qb:DataSet .
        OPTIONAL{ 
            ?dataset_uri rdfs:label ?label .
            #filter(langMatches(lang(?label),"fr"))
            ?dataset_uri rdfs:comment ?comment.
            
        }
    }
    """

    wrapper = SPARQLWrapper(target_url)
    wrapper.setQuery(QUERY)
    wrapper.setReturnFormat(JSON)
    json = wrapper.query().convert()

    def label_modif(row):
        if "label" in row.keys():
            if 'comment' in row.keys():
                return row["label"]["value"]+ ' - '+ row["comment"]["value"]
            else :
                return row["label"]["value"]
        else:
            if 'comment' in row.keys():
                return row["dataset_uri"]["value"]+ ' - '+ row["comment"]["value"]
            else:
                return row["dataset_uri"]["value"]

    results=json['results']['bindings']
    keys=list(results[0].keys())
    
    return [{'label': label_modif(result), 'value': result["dataset_uri"]['value']} for result in results]

def queryToDataFrame(results):
    results_value=results['results']['bindings']
    table=pd.DataFrame([[x[name]['value'] for x in results_value]  for name in list(results_value[0].keys())]).T
    table.columns=list(results_value[0].keys())
    return table

def query_dimensions(target_url, dataset_uri):
    
    sparql = SPARQLWrapper(target_url)
    sparql.setReturnFormat(JSON)
    
    query = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX qb: <http://purl.org/linked-data/cube#>
    PREFIX mes: <http://id.insee.fr/meta/mesure/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 

   SELECT DISTINCT ?concept ?dim where {{           
        <{dataset_uri}> qb:structure ?dsd.
        ?dsd qb:component/qb:dimension ?dim.
        ?dim rdfs:label ?labelfr.
        
        ?dim qb:concept ?o.
        ?o rdfs:label ?concept .

        filter(langMatches(lang(?concept),"fr"))
    }} 
    """

    sparql.setQuery(query)
    results = sparql.query().convert()
    results=results["results"]["bindings"]
    keys=list(results[0].keys())
    
    return [keys,[{'label': result[keys[0]]['value'],'value': result[keys[1]]['value']} for result in results]]
    
def query_measures(target_url, dataset_uri):
    
    sparql = SPARQLWrapper(target_url)
    sparql.setReturnFormat(JSON)
    
    query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX qb: <http://purl.org/linked-data/cube#>
    PREFIX mes: <http://id.insee.fr/meta/mesure/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 

    SELECT distinct ?measure ?label where {  
        #?s a qb:DataSet.
        <http://data.insee.fr/dataset/LFS> qb:structure ?dsd.
        ?dsd qb:component/qb:measure ?measure .
        ?measure rdfs:label ?labelen.         
        BIND(IF(BOUND(?labelen), ?labelen,"NO LABEL !!!"@en) AS ?label)
        OPTIONAL{filter(langMatches(lang(?labelen),"en")).}
    }
    """

    sparql.setQuery(query)
    results = sparql.query().convert()
    results=results["results"]["bindings"]
    
    def label_modif(row):
        if row["label"]["value"]!="":
            return row["label"]["value"]
        else:
            return row["measure"]["value"]

    #results=results["results"]["bindings"]
    #keys=list(results[0].keys())

    return [{'label': label_modif(result), 'value': result['measure']['value']} for result in results]
