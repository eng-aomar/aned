from SPARQLWrapper import JSON, SPARQLWrapper

from Connection.DBConnection import Mongodb
from Excel.excel import Excel
#from pandas import json_normalize
from sparqlwikidata import sparql_wikidata
import json


def search_wikidata_arabic_label(Person_arabic_label):
    sparql_query = (
        ' SELECT DISTINCT ?item ?itemLabel ?itemDescription ?entity_type ?main_category (GROUP_CONCAT(DISTINCT(?altLabel); separator = ", ") AS ?altLabel_list) WHERE {'
                            f'?item ?label "{Person_arabic_label}"@ar.'
                            '?item wdt:P31 ?entity_type .'
                            'MINUS { ?item wdt:P31 wd:Q4167410}'
                            'OPTIONAL{    ?item wdt:P910 ?main_category}'
                            '?article schema:about ?item;'
                            "schema:isPartOf <https://en.wikipedia.org/>;"
                            'OPTIONAL { ?item skos:altLabel ?altLabel . FILTER (lang(?altLabel) = "ar") }'
                            'SERVICE wikibase:label { bd:serviceParam wikibase:language "ar" .}'         
                            '}'
                            'GROUP BY ?item ?itemLabel ?itemDescription ?entity_type ?main_category'
    )
    return sparql_wikidata(sparql_query)


def search_wikidata_arabic_altlabel(Person_arabic_label):
    sparql_query = (
        ' SELECT DISTINCT ?item ?itemLabel ?itemDescription ?entity_type ?main_category (GROUP_CONCAT(DISTINCT(?altLabel); separator = ", ") AS ?altLabel_list) WHERE {'
        f'?item ?altLabel "{Person_arabic_label}"@ar.'
        '?item wdt:P31 ?entity_type .'
        'MINUS { ?item wdt:P31 wd:Q4167410}'
        'OPTIONAL{    ?item wdt:P910 ?main_category}'
        '?article schema:about ?item;'
        "schema:isPartOf <https://en.wikipedia.org/>;"
        'OPTIONAL { ?item skos:altLabel ?altLabel . FILTER (lang(?altLabel) = "ar") }'
        'SERVICE wikibase:label { bd:serviceParam wikibase:language "ar" .}'
        '}'
        'GROUP BY ?item ?itemLabel ?itemDescription ?entity_type ?main_category'
    )
    return sparql_wikidata(sparql_query)
res_list = []

def extract_wikidata(d):
    for k, v in d.items():
        if isinstance(v, dict):
            extract_wikidata(v)
        else :
            print("{0} : {1}".format(k, v))
            if k == 'bindings':
                
                for index in range(len(v)):
                    data = {}
                    for key, val in v[index].items():
                        data[key] = val['value']
                    res_list.append(data)


def extract_Person_Informaton(results, arabic_name):
    extract_wikidata(results)
    if res_list:
        Mongodb.insert_wikidata(res_list)
    else:
        pass

xl_worksheet = Excel.open_excel_file()
person_names = Excel.load_excel_data(xl_worksheet)

for person in person_names:
    try:
        person_found = Mongodb.insert_person(person)
        if person_found is None:
            label_results = search_wikidata_arabic_label(person['arabic_name'])
            extract_Person_Informaton(label_results, person['arabic_name'])
            altlabel_results = search_wikidata_arabic_altlabel(
                person['arabic_name'])
            extract_Person_Informaton(altlabel_results, person['arabic_name'])

    except:
        pass



