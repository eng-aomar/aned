from SPARQLWrapper import SPARQLWrapper, JSON
#from pandas import json_normalize
import pandas as pd



def search_wikidata(item):      
  sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
  sparql.setQuery("""
          SELECT DISTINCT ?item ?itemLabel ?itemDescription WHERE {
            ?item ?label "ياسر عرفات"@ar.
            ?article schema:about ?item;
              schema:isPartOf <https://en.wikipedia.org/>.
            SERVICE wikibase:label { bd:serviceParam wikibase:language "ar". }
          }
      """)
  sparql.setReturnFormat(JSON)
  return sparql.query().convert()
  

named_entities = ('ياسر عرفات')

for item in named_entities:
  results = search_wikidata(item)
  for result in results['results']['bindings']:
    print(result["item"]["value"])
    print(result["itemLabel"]["value"])
    print(result["itemDescription"]["value"])

def print_data(results):
  results_df = pd.json_normalize(results['results']['bindings'])
  results_df[['item.value', 'itemLabel.value', 'itemDescription.value']]

