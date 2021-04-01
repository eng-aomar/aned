from pymongo import MongoClient
import os


class Mongodb:

    @classmethod
    def db_connect(cls):
        DB_URI = os.environ.get('AwraqDB_URI')
        client = MongoClient(DB_URI)
        db = client.awraqdb
        return db

    @classmethod
    def get_uris(cls):
        db = Mongodb.db_connect()
        wikidata_collection = db['wikidata']
        entities = wikidata_collection.find()
        return entities

    @classmethod
    def get_uri_by(cls, wikidata_label):
        db = Mongodb.db_connect()
        wikidata_collection = db['wikidata']
        entities = wikidata_collection.find(wikidata_label)
        return entities

    @classmethod
    def get_wikidata_collection(cls):
        db = Mongodb.db_connect()
        return db['wikidata']

    @classmethod
    def is_saved_to(cls, wikidata_collection, wikidata_uri):
        entity_found = wikidata_collection.find_one(
            {'entity_uri': wikidata_uri})
        return entity_found

    @classmethod
    def insert_wikidata(cls, results):

        wikidata_collection = Mongodb.get_wikidata_collection()
        for result in results:
            entity_found = Mongodb.is_saved_to(wikidata_collection,result['entity_uri'])
            if entity_found is None:
                wikidata_collection.insert_one(result)
                print('entity:' + result['entity_label'] + 'inserted successfully')
            else:
                pass
    @classmethod
    def find_by(cls, uri, wikidata_collection):
        all_entities = wikidata_collection.find(
            {'entity_uri': uri}, sort=[('_id', -1)]).limit(10)
        data = []
        for x in all_entities:
            datum = {}
            datum['entity_uri'] = x['entity_uri']
            datum['entity_label'] = x['entity_label']
            datum['entity_descrption'] = x['entity_descrption']
            datum['entity_alias'] = x["entity_aliase"]
            data.append(datum)
        return data

