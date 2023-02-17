import os
import json


class FileIO:
    def __init__(self, file_name) -> None:

        if not file_name.endswith('.json'):
            raise Exception('File must be a JSON file!')

        self.file = file_name

        if not os.path.isfile(self.file):
            print("DB file not found! Creating new DB file...")
            try:
                with open(self.file, 'w', encoding='utf-8') as f:
                    f.write('')
            except Exception as e:
                print('Error creating DB file!\n' + str(e))
                exit(1)

    def save(self, data: dict) -> None:
        try:
            with open(self.file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print('Error saving data!\n' + str(e))

    def load(self) -> dict:
        try:
            with open(self.file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print('Error loading data!\n' + str(e))
            return {}
