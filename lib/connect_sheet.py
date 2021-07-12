import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

class Sheet:
    def __init__(self):
        scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name('lib/fast-calc.json')
        client = gspread.authorize(creds)

        self.sheet = client.open("How to Calculate Quickly").sheet1

        self.data = self.sheet.get_all_values()
        self.question_id = pd.DataFrame({'question_index': self.sheet.col_values(1), 'sub_question_index': self.sheet.col_values(2)})


    def get_question(self, question):
        raw_data = self.data[question]

        numbers = [int(i) for i in raw_data[4:len(raw_data)] if i != '']

        return {
            'question_number': self.question_id.iloc[question, 0],
            'sub_question_index': self.question_id.iloc[question, 1],
            #'question': raw_data[0],
            #'sub_question': raw_data[1],
            #'info': raw_data[2],
            'operator': raw_data[3],
            'numbers':numbers
        }

    def get_numbers(self, question):
        return self.get_question(question)['numbers']

    def get_answer(self, question):
        data = self.get_question(question)

        if data['operator'] == '+':
            return sum(data['numbers'])

    def lookup_question_id(self, question):
        return list(self.question_id.iloc[question].values)

    def get_info(self, question):
        question_id = self.lookup_question_id(question)
        
        info_id = self.question_id.loc[
            (self.question_id['question_index'] == question_id[0]) & 
            (self.question_id['sub_question_index'] == '1')].index[0]

        return self.data[info_id][2]

    def get_everything(self, question):
        return {'question': self.get_question(question),
        'answer': self.get_answer(question),
        'info': self.get_info(question)}

    def lookup_question_number(self, question, sub_question):
        return self.question_id.loc[
            (self.question_id['question_index'] == str(question)) & 
            (self.question_id['sub_question_index'] == str(sub_question))].index[0]