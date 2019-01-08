from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

# TODO cache ?
PLOSH_URL = "http://graphdb.dev.innovation.insee.eu/repositories/plosh"
SCOTT_URL = "https://statistics.gov.scot/sparql"

def get_endpoints_list():
    return [
        {"label": "PLOSH data sets", "value": PLOSH_URL},
        {"label": "Scotland's official statistics", "value": SCOTT_URL}
        ]

def query_datasets(target_url):
    QUERY = """
    PREFIX qb: <http://purl.org/linked-data/cube#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 

    SELECT ?label ?comment ?dataset_uri where {           
        ?dataset_uri a qb:DataSet ; rdfs:label ?label  .
		OPTIONAL {
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
    
    return list({v['value']:v for v in [{'label': label_modif(result), 'value': result["dataset_uri"]['value']} for result in results]}.values())

def queryToDataFrame(results):
    results_value=results['results']['bindings']
    table=pd.DataFrame([[x[name]['value'] for x in results_value]  for name in list(results_value[0].keys())]).T
    table.columns=list(results_value[0].keys())
    return table

def query_dimensions(target_url, dataset_uri):
    
    sparql = SPARQLWrapper(target_url)
    sparql.setReturnFormat(JSON)
    
    query = f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
    PREFIX qb: <http://purl.org/linked-data/cube#>

    SELECT ?concept ?dim where {{           
        <{dataset_uri}> qb:structure ?dsd .
        ?dsd qb:component/qb:dimension ?dim .
        ?dim rdfs:label ?concept .
        #filter(langMatches(lang(?concept), "en"))
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
    
    query = f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX qb: <http://purl.org/linked-data/cube#>

    SELECT ?measure ?label where {{ 
        <{dataset_uri}> qb:structure ?dsd .
        ?dsd qb:component/qb:measure ?measure .
        ?measure rdfs:label ?label .
		FILTER (STRLEN(?label) > 0)
    }}
    """

    sparql.setQuery(query)
    results = sparql.query().convert()
    results=results["results"]["bindings"]
    
    def label_modif(row):
        if row["label"]["value"]!="":
            return row["label"]["value"]
        else:
            return row["measure"]["value"]

    def index(row):
        if row["label"]["value"]!="":
            return 1
        else:
            return 2

    df=pd.DataFrame([{'label': label_modif(result), 'value': result['measure']['value'], 'index':index(result)} 
                     for result in results]).sort_values(['value','index'])
    df=df.groupby('value').first().reset_index()[['value','label']]
    
    return [{'label': result[1], 'value': result[0]} for result in df.to_dict('split')['data']]

def query_data(target_url, dataset_uri, dimension1, dimension2, measures_info):
    
    sparql = SPARQLWrapper(target_url)
    sparql.setReturnFormat(JSON)
    
    query = f"""
	PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX qb: <http://purl.org/linked-data/cube#>

    SELECT ?concept1 ?concept2 (SUM(?value) as ?total) where {
        ?obs qb:dataSet <{dataset_uri}> .
        ?obs <{dimension1}> ?dim1 .
        ?obs <{dimension2}> ?dim2 .
        ?obs <{measures_info}> ?value .

        ?dim1 rdfs:label ?concept1 .
        ?dim2 rdfs:label ?concept2 .
    }
    GROUP BY ?concept1 ?concept2
    """

    print(query)

    sparql.setQuery(query)
    results = sparql.query().convert()
    
    df=queryToDataFrame(results)

    return df.pivot(index='concept1', columns='concept2', values='value').reset_index()


