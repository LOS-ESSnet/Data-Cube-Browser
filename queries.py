from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

# TODO cache ?
#URL = "http://hackathon2018.ontotext.com/repositories/plosh"
URL = "https://statistics.gov.scot/sparql"

def query_datasets():

    QUERY = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX qb: <http://purl.org/linked-data/cube#>
    PREFIX mes: <http://id.insee.fr/meta/mesure/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 

    SELECT ?dataset_uri ?label  where {           
        ?dataset_uri a qb:DataSet .
        OPTIONAL{ 
            ?dataset_uri rdfs:label ?label 
            filter(langMatches(lang(?label),"fr"))
            
        }
    }
    """

    wrapper = SPARQLWrapper(URL)
    wrapper.setQuery(QUERY)
    wrapper.setReturnFormat(JSON)
    json = wrapper.query().convert()

    def label_modif(row):
        if "label" in row.keys():
            return row["label"]["value"] 
        else:
            return row["dataset_uri"]["value"]

    return [ {"label": label_modif(row), "value": label_modif(row)} for row in json["results"]["bindings"] ] 

def queryToDataFrame(results):
    results_value=results['results']['bindings']
    table=pd.DataFrame([[x[name]['value'] for x in results_value]  for name in list(results_value[0].keys())]).T
    table.columns=list(results_value[0].keys())
    return table

def query_dimensions():
    
    sparql = SPARQLWrapper(URL)
    sparql.setReturnFormat(JSON)
    
    query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX qb: <http://purl.org/linked-data/cube#>
    PREFIX mes: <http://id.insee.fr/meta/mesure/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 

    SELECT ?label ?dim where {           
        ?s a qb:DataSet.
        ?s qb:structure ?dsd.
        ?dsd qb:component/qb:dimension ?dim.
        ?dim rdfs:label ?labelfr.

        filter(langMatches(lang(?labelfr),"en"))
        BIND(IF(BOUND(?labelfr), ?labelfr,?dim) AS ?label)
    } 
    """

    sparql.setQuery(query)
    results = sparql.query().convert()
    results=results["results"]["bindings"]
    keys=list(results[0].keys())
    
    return [{'label': result[keys[0]]['value'],'value': result[keys[1]]['value']} for result in results]
    
def query_measures():
    
    sparql = SPARQLWrapper(URL)
    sparql.setReturnFormat(JSON)
    
    query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX qb: <http://purl.org/linked-data/cube#>
    PREFIX mes: <http://id.insee.fr/meta/mesure/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 

    SELECT ?label ?measure where {           
        ?s a qb:DataSet.
        ?s qb:structure ?dsd.
        ?dsd qb:component/qb:measure ?measure .
        ?measure rdfs:label ?labelfr.

        BIND(IF(BOUND(?labelfr), ?labelfr,"NO LABEL !!!"@fr) AS ?label)
    } LIMIT 100
    """

    sparql.setQuery(query)
    results = sparql.query().convert()
    results=results["results"]["bindings"]
    keys=list(results[0].keys())

    return [{'label': result[keys[0]]['value'],'value': result[keys[1]]['value']} for result in results]
