import xlrd

class Person(object):

    def __init__(self, id, arabic_name, english_name):
        self.id = id
        self.arabic_name = arabic_name
        self.english_name = english_name

    def __str__(self):
        return("Person object:\n"
                "  Person_id = {0}\n"
                "  arabic_name = {1}\n"
                "  english_name = {2}\n"
                .format(self.id, self.arabic_name, self.english_name))

class Excel():
    EXCEL_PATH = 'Excel/AwraqData.xlsx'
    SHEET_NAME = 'Person'
    COULMN_NAME = 'Name_ar1 offical'
    @classmethod
    def open_excel_file(cls):
        xl_workbook = xlrd.open_workbook(Excel.EXCEL_PATH)
        xl_worksheet = xl_workbook.sheet_by_name(Excel.SHEET_NAME)
        number_of_rows = xl_worksheet.nrows
        load_excel_data(number_of_rows, xl_worksheet)
    @staticmethod
    def load_excel_data(number_of_rows, xl_worksheet):
        items=[]
        for row in range(1, number_of_rows):
            values = []
            arabic_name = (xl_worksheet.cell(row,4).value)
            english_name = (xl_worksheet.cell(row, 8).value)
            try:
                arabic_name = str(int(arabic_name))
                english_name = str(int(english_name))
            except ValueError:
                pass
            finally:
                values.append(row)
                values.append(arabic_name)
                values.append(english_name)
            item = Person(*values)
            items.append(item)
        print_vlaues(items)
    @staticmethod
    def print_vlaues(items):
        for item in items:
            print (item)
                #print("Accessing one single value (eg. DSPName): {0}".format(item.arabic_name))
            
