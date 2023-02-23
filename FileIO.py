import os
import json
from bcolors import bcolors as bc


class FileIO:
    """FileIO class for handling file operations
    """

    def __init__(self, file_name: str) -> None:
        """Constructor for FileIO class

        Args:
            file_name (str): Name of the JSON file
        """
        self.b = bc()

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

    def __save(self, data: dict) -> bool:
        """Saves data to the file

        Args:
            data (dict): Data to be saved

        Returns:
            bool: True if data is saved successfully, False otherwise
        """
        try:
            with open(self.file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
                return True
        except Exception as e:
            print(self.b.error('Error saving data!\n') + str(e))
            return False

    def __load(self) -> dict:
        """Loads data from the file

        Returns:
            dict: Data loaded from the file
        """
        try:
            with open(self.file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(self.b.error('Error loading data!\n') + str(e))
            return {}

    def create(self, id: int, status: str, os: str) -> None:
        """Creates a new PC in the DB

        Args:
            id (int): ID of the PC
            status (str): Status of the PC
            os (str): OS of the PC
        """
        data = self.__load()

        if not data:
            return

        data.append({
            "id": id,
            "status": status,
            "os": os
        })
        if self.__save(data):
            print(
                self.b.success(f'\nPC with ID {id} added successfully to DB\n'))

    def get(self, value: str | int, key: str) -> list:
        """Gets a PC from the DB based on the search criteria

        Args:
            value (str | int): Value to be searched
            key (str, optional): Search criteria. Must be 'id' or 'status' or 'os'.

        Returns:
            list: List of PCs matching the search criteria
        """

        if key not in ['id', 'status', 'os']:
            print(self.b.error('Invalid key!'))
            return []

        res = []
        data = self.__load()
        if not data:
            return
        for pc in data:
            if str(pc[key]) == str(value):
                res.append(pc)
        return res

    def get_all(self) -> list:
        """Gets all PCs from the DB"""
        return self.__load()

    def update(self, id: int, status: str, os: str) -> None:
        """Updates a PC in the DB

        Args:
            id (int): ID of the PC
            status (str): Status of the PC
            os (str): OS of the PC
        """
        data = self.__load()
        if not data:
            return
        for pc in data:
            if pc['id'] == id:
                pc['status'] = status
                pc['os'] = os
                if self.__save(data):
                    print(
                        self.b.success(f'\nPC with ID {id} update successfully\n'))
                else:
                    print(
                        self.b.error(f'\nError updating PC with ID {id}\n'))
                return
        print(
            self.b.error(f'\nPC with ID {id} was not found from DB\n'))

    def delete(self, id: int) -> None:
        """Deletes a PC from the DB

        Args:
            id (int): ID of the PC to be deleted
        """
        data = self.__load()
        if not data:
            return
        for pc in data:
            if pc['id'] == id:
                data.remove(pc)
                if self.__save(data):
                    print(
                        self.b.success(f'\nPC with ID {id} removed successfully from DB\n'))
                else:
                    print(
                        self.b.error(f'\nError removing PC with ID {id}\n'))
                return

        print(
            self.b.error(f'\nPC with ID {id} was not found from DB\n'))
