import glob
import re
import datetime
from models import Contribution
from analysis import MedianByZip, MedianByDate

class DataProcessor:
    def __init__(self, filename, delimiter, field_names, field_idx):
        self.callbacks = None
        self.filename = filename
        self.field_names = field_names
        self.field_idx = field_idx
        self.delimiter = delimiter

        # creating contribution object
        self.contribution = Contribution(self.delimiter, self.field_names, self.field_idx)

    def read_file(self):
        with open(self.filename, 'r') as f:
            for line in f.readlines():
                data = self.contribution.process_string(line)
                yield data

def valid_date(datestring):
        try:
            datetime.datetime.strptime(datestring, '%Y%m%d')
            return True
        except ValueError:
            return False

if __name__ == '__main__':
    input_file = r'C:\Users\vxd15\Desktop\DataEngineeringCodingChallenge\insight_testsuite\tests\my_test\input\your-own-input.txt'
    zip_output_file = r'C:\Users\vxd15\Desktop\DataEngineeringCodingChallenge\insight_testsuite\tests\my_test\output\medianvals_by_zip.txt'
    date_output_file = r'C:\Users\vxd15\Desktop\DataEngineeringCodingChallenge\insight_testsuite\tests\my_test\output\medianvals_by_date.txt'
    delimiter = '|'
    field_names = ['CMTE_ID', 'ZIP_CODE', 'TRANSACTION_DT', 'TRANSACTION_AMT', 'OTHER_ID']
    field_names_idx = [0, 10, 13, 14, 15]

    dp = DataProcessor(input_file, delimiter, field_names, field_names_idx)

    m_zip = MedianByZip(zip_output_file)
    m_date = MedianByDate(date_output_file)

    for data in dp.read_file():
        # print(data)
        recipient = data[field_names[0]]
        zipcode = data[field_names[1]]
        t_date = data[field_names[2]]
        t_amount = data[field_names[3]]
        other_id = data[field_names[4]]

        if not other_id:
            if re.match('^\d{5}(?:[-\s]\d{4})?$',zipcode):
                m_zip.process_record(recipient, zipcode, t_amount)
            if valid_date(t_date):
                m_date.add_record(recipient, t_date, t_amount)

    m_date.generate_report()
