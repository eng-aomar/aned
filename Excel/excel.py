import xlrd
from Connection.DBConnection import Mongodb

class Person(object):

    def __init__(self, id, arabic_name, english_name, wikidata_match):
        self.id = id
        self.arabic_name = arabic_name
        self.english_name = english_name
        self.wikidata_match = wikidata_match

    def __str__(self):
        return("Person object:\n"
                "  Person_id = {0}\n"
                "  arabic_name = {1}\n"
                "  english_name = {2}\n"
                "  wikidata_match = {3}\n"
                .format(self.id, self.arabic_name, self.english_name, self.wikidata_match))

class Excel():
    EXCEL_PATH = 'Excel/AwraqData.xlsx'
    SHEET_NAME = 'Person'
    COULMN_NAME = 'Name_ar1 offical'
    @classmethod
    def open_excel_file(cls):
        xl_workbook = xlrd.open_workbook(Excel.EXCEL_PATH)
        xl_worksheet = xl_workbook.sheet_by_name(Excel.SHEET_NAME)
        return xl_worksheet
    @staticmethod
    def load_excel_data(xl_worksheet):
        number_of_rows = xl_worksheet.nrows
        items = []

        for row in range(1, number_of_rows):
            try:
                arabic_name = (xl_worksheet.cell(row, 4).value)
                english_name = (xl_worksheet.cell(row, 8).value)
                wikidata_match = False             
            except ValueError:
                pass
            finally:
                datum = {}
                datum['person_id'] = row 
                datum['arabic_name'] = arabic_name
                datum['english_name'] = english_name
                datum['wikidata_match'] = wikidata_match
                items.append(datum)      
        return items
    @staticmethod
    def print_vlaues(items):
        for item in items:
            print (item)
                #print("Accessing one single value (eg. DSPName): {0}".format(item.arabic_name))
            
