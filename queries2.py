from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

def query_endpoint(url,query):
    endpoint = SPARQLWrapper(url)
    endpoint.setQuery(query)
    endpoint.setReturnFormat(JSON)
    return endpoint.query().convert()
	
def load_queries(dir):
    dict={}
    for file in os.listdir(dir):
        with open(os.path.join(dir, file)) as f:
            query=[]
            for line in f:
                query.append(line)
            dict[file]=''.join(query)
    yield dict
	
def pretty_results(results):
    results=results["results"]["bindings"]
    keys=list(results[0].keys())
    return [keys,[{'label': result[keys[0]]['value'],'value': result[keys[1]]['value']} for result in results]]
