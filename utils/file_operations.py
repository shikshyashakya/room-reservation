import pandas as pd
import os

class FileOperations:
    @staticmethod
    def read_file(file_path):
        # Check if file exists
        if not os.path.exists(file_path):
            print('No rooms found.')
            return []

        # Read excel file
        data = pd.read_excel(file_path)

        # Check if file is empty
        if data.empty:
            print('No rooms found.')
            return []
        
        return data
    

    # search in excel file
    @staticmethod
    def search_file(file_path):
        '''Search across multiple columns'''
        data = FileOperations.read_file(file_path)

        if data is None:
            return None

        return data