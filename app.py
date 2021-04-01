from SPARQLWrapper import SPARQLWrapper, JSON
#from pandas import json_normalize
import pandas as pd
from sparqlwikidata import sparql_wikidata
from Connection.DBConnection import Mongodb
def search_wikidata(awaraq_entity_label):
  sparql_query = (
               'SELECT DISTINCT ?item ?itemLabel ?itemDescription (GROUP_CONCAT(DISTINCT(?altLabel); separator = ", ") AS ?altLabel_list) WHERE {'
                        f'?item ?label "{awaraq_entity_label}"@ar.'
                        '?article schema:about ?item;'
                        "schema:isPartOf <https://en.wikipedia.org/>;"
                        'OPTIONAL { ?item skos:altLabel ?altLabel . FILTER (lang(?altLabel) = "ar") }'
                        'SERVICE wikibase:label { bd:serviceParam wikibase:language "ar" .}'         
                        '}'
                        'GROUP BY ?item ?itemLabel ?itemDescription'
  )
  return sparql_wikidata(sparql_query)


def extract_wikidata(json_results):
  data = []
  for result in results['results']['bindings']:
      datum={}  
      datum['entity_uri'] = result["item"]["value"]
      datum['entity_label'] = result["itemLabel"]["value"]
      datum['entity_descrption'] = result["itemDescription"]["value"]
      datum['entity_alias'] = result["altLabel_list"]["value"]
      data.append(datum)
  return data



def print_data(results):
      pass
    #results_df = pd.json_normalize(results['results']['bindings'])
    #results_df[['item.value', 'itemLabel.value', 'itemDescription.value']]

input_string = """Name,Phone,Address
Mike Smith,15554218841,123 Nice St, Roy, NM, USA
Anita Hernandez,15557789941,425 Sunny St, New York, NY, USA
Guido van Rossum,315558730,Science Park 123, 1098 XG Amsterdam, NL"""


def string_split_ex(unsplit):
    results = []

    # Bonus points for using splitlines() here instead,
    # which will be more readable
    for line in unsplit.split('\n')[1:]:
        results.append(line.split(',', maxsplit=2))
    return results

#print(string_split_ex(input_string))
#print(extract_wikidata(results))

awraq_entitis = ('القدس','ياسر عرفات','عبد السلام فياض',)
for awraq_entity in awraq_entitis:
    try:
        print(awraq_entity)
        results = search_wikidata(awraq_entity)
        data = extract_wikidata(results)
        Mongodb.insert_wikidata(data)
    except:
        pass
