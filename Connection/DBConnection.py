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
            {'item': wikidata_uri})
        return entity_found


    @classmethod
    def update_person(cls, person_name):
        db = Mongodb.db_connect()
        wikidata_collection = db['person']
        print('Inside Update')
        filter = {'arabic_name': person_name}
        wikidata_match = {"$set": {'wikidata_match': True}}
        wikidata_collection.update_one(filter, wikidata_match)
        print('Updated Successfully !!!!')

        
    @classmethod
    def is_saved_to_person(cls,Person_collection, arabic_name):
        person_found = Person_collection.find_one(
            {'arabic_name': arabic_name})
        return person_found
        
    @classmethod
    def insert_wikidata(cls, results):
        wikidata_collection = Mongodb.get_wikidata_collection()
        for item in results:
            found = Mongodb.is_saved_to(wikidata_collection, item['item'])
            if found is None:
                wikidata_collection.insert(item)
                Mongodb.update_person(item['itemLabel'])
                print('enitiy: [' +
                        item['itemLabel'] + '] has been inserted successfully')
            else:
                print('enitiy: [' +
                        item['itemLabel'] + '] Alreday there')

    @classmethod
    def insert_person(cls, person):
        db = Mongodb.db_connect()
        collection = db['person']
        person_found = Mongodb.is_saved_to_person(collection,
                                            person['arabic_name'])
        if person_found is None:
            collection.insert_one(person)
            print('Person: [' +
                person['english_name'] + '] has been inserted successfully')
        else:
            print('Person: [' +
                person['english_name'] + '] Alreday there')
        return person_found
    @classmethod
    def find_by(cls, uri, wikidata_collection):
        all_entities = wikidata_collection.find(
            {'entity_uri': uri}, sort=[('_id', -1)]).limit(10)
        data = []
        for x in all_entities:
            datum = {}
            datum['item'] = x['item']
            datum['itemLabel'] = x['itemLabel']
            datum['entity_descrption'] = x['entity_descrption']
            datum['entity_type'] = x['entity_type']
            datum['entity_main_category'] = x['entity_main_category']
            datum['entity_alias'] = x["entity_aliase"]
            data.append(datum)
        return data
        

