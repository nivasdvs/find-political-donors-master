class Contribution:
    def __init__(self, delimiter, field_names, field_idx):
        self.delimiter = delimiter
        self.field_names = field_names
        self.field_names_idx = field_idx

    def process_string(self, string):
        raw_data_list = string.split(self.delimiter)

        data = {
            # recipient ID
            self.field_names[0]: raw_data_list[self.field_names_idx[0]],
            # considering only the first 5 digits of zipcode
            self.field_names[1]: raw_data_list[self.field_names_idx[1]][:5],
            self.field_names[2]: raw_data_list[self.field_names_idx[2]],
            self.field_names[3]: raw_data_list[self.field_names_idx[3]],
            self.field_names[4]: raw_data_list[self.field_names_idx[4]]
        }

        return data

    def get_fields(self):
        return [x for x in zip(self.field_names_idx, self.field_names)]