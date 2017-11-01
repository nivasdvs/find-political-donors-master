import numpy as np
import pandas as pd


class MedianByZip:

    def __init__(self, output_filename):
        self.data_dict = {}
        self.out_file_name = output_filename

    def _add_amount(self, key, amount):

        try:
            amount = int(amount)
        except ValueError as e:
            raise e

        if key in self.data_dict:
            self.data_dict[key].append(amount)
        else:
            self.data_dict[key] = [amount]

    def _write_record(self, string):
        with open(self.out_file_name, 'a') as f:
            f.write(string + '\n')

    def process_record(self, recipient, zipcode, amount):
        contribution_key = (recipient, zipcode)
        self._add_amount(contribution_key, amount)

        recorded_data = self.data_dict[contribution_key]

        median = str(round(np.median(np.array(recorded_data))))
        num_contributions = str(len(recorded_data))
        running_sum = str(sum(recorded_data))

        median_by_zip = '|'.join([recipient, zipcode, median,
                                  num_contributions, running_sum])

        self._write_record(median_by_zip)


class MedianByDate:
    def __init__(self, output_file):
        self.output_file = output_file
        self.columns = ['recipient', 'date', 'amount']
        self.data_frame = pd.DataFrame(columns=self.columns)
        self.data_frame['amount'] = self.data_frame['amount'].astype('int')

    def add_record(self, recipient, date, amount):
        record_df = pd.DataFrame({
            'recipient': [recipient],
            'date': [date],
            'amount': [int(amount)]
        })

        self.data_frame = self.data_frame.append(record_df, ignore_index=True)

    def generate_report(self):

        grouped_data = self.data_frame.groupby(['recipient', 'date'], sort=True)['amount']
        aggregation = grouped_data.agg([np.sum, np.median, np.alen])

        with open(self.output_file, 'a') as f:
            for index, row in aggregation.iterrows():
                recipient = index[0]
                date = index[1]
                contribution_sum = str(int(row['sum']))
                contribution_median = str(int(round(row['median'],0)))
                num_transactions = str(int(row['alen']))

                line = '|'.join([recipient, date, contribution_median,
                                 num_transactions, contribution_sum])

                f.write(line + '\n')



