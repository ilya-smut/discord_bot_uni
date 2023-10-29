import jsonpickle
import os


class ComplaintsDb:
    def __init__(self):
        self.complaints = {}
        self.path = None

    async def load(self, path):
        self.path = path
        if os.path.isfile(path):
            with open(path, 'r') as file:

                contents = file.read()

                if contents != '':

                    extracted_dict = jsonpickle.decode(contents)
                    if type(extracted_dict) == dict:

                        self.complaints = extracted_dict
        else:
            self.path = path
            with open(path, 'a') as file:
                pass

    def add_complaint(self, key=None, complaint='I am lazy'):
        self.complaints[str(key)] = str(key) + " : " + complaint

    def save(self, path=None):
        if path:
            with open(path, 'w') as file:
                encoded_dict = jsonpickle.encode(self.complaints)
                file.write(encoded_dict)
        else:
            with open(self.path, 'w') as file:
                encoded_dict = jsonpickle.encode(self.complaints)
                file.write(encoded_dict)

    def drop(self):
        self.complaints = {}

    def get_keys(self):
        return self.complaints.keys()

    def get_complaint(self, key):
        if str(key) in self.get_keys():
            return self.complaints[str(key)]

    def del_complaint(self, key):
        if str(key) in self.get_keys():
            del(self.complaints[str(key)])

    def get_all_complaints(self):
        complaints = []
        for key in self.get_keys():
            complaints.append(self.complaints[key])

        return complaints
