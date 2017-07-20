'''
    DAO for remote Sparql
'''
from SPARQLWrapper import SPARQLWrapper, JSON

class SparqlDao:
    '''
       class contains wrapper methods for the Sparql queries
    '''
    def run_remote_sparql(self,endpoint, query):
        '''
           Method to run remote Sparql queries
        '''
        data = []

        sparql = SPARQLWrapper(endpoint)

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        data = [(r["s"]["value"], r["p"]["value"], r["o"]["value"]) for r in results["results"]["bindings"]]

        return data

    def autocomplete_sparql(self,endpoint, query):
        '''
           Method for autocomplete sparql
        '''
        data = []

        sparql = SPARQLWrapper(endpoint)

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        data = [(r["s"]["value"], r["o"]["value"]) for r in results["results"]["bindings"]]

        return data