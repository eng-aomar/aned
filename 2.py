from SPARQLWrapper import SPARQLWrapper, JSON, XML, N3, RDF
print('Enter your name:')
x = input()
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("\n"
                "    PREFIX dbpedia: <http://dbpedia.org/resource/>"
                " PREFIX dbo: <http://dbpedia.org/ontology/>"
                "PREFIX dbp: <http://dbpedia.org/property/>\n"
                "PREFIX foaf: <http://xmlns.com/foaf/0.1/>\n"
                "PREFIX rdfs:   <http://www.w3.org/2000/01/rdf-schema#>\n"
                "PREFIX dct:    <http://purl.org/dc/terms/>\n"
                "SELECT DISTINCT ?name  ?birthDate   WHERE {\n"
                "dbpedia:"+x+" foaf:name ?name\n"
                "}\n"
                "                   ")
print('\n\n*** JSON Example')
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
for result in results["results"]["bindings"]:
    a = result["name"]["value"]
print(a)
