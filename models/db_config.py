import os;
import pyodbc;
from dotenv import load_dotenv

load_dotenv()

class db_config:
    DB_HOST = os.environ.get('DB_HOST')
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    DB_PASS = os.environ.get('DB_PASS')

    def get_connection(self):
        print(self.DB_HOST)
        return pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.DB_HOST+';DATABASE='+self.DB_NAME+';UID='+self.DB_USER+';PWD='+ self.DB_PASS+';')

db = db_config();