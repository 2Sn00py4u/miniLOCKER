import duckdb as duck
import pandas as pd
import os

class DBMS:
    def __init__(self, DBfilePath:str) -> duck.DuckDBPyConnection:
        self.DBpath = DBfilePath
        self.__dbConnection = duck.connect(self.DBpath)
        self.__Tables = self.getTables()
    
    def importCSV(self, csvPath: str, tableName: str):
        with open(csvPath, "r") as csvFile:
            attributes = []
            values = []
            for i, line in enumerate(csvFile):
                if i == 0:
                    line = line.split(";")
                    line.pop(len(line)-1)
                    attributes = line
                else:
                    line = line.split(";")
                    line.pop(len(line)-1)
                    values.append(tuple(line))
            csvFile.close()
        if tableName in self.getTables():
            self.deleteTable(tableName)
        self.createTable(tableName, attributes)
        self.insertValues(tableName, values)
    
    """  get-functions  """
    def getConnection(self):
        return self.__dbConnection
    
    def getTables(self, pdOutput: bool = False) -> list|pd.DataFrame:
        if pdOutput == True:
            return self.execute("""SHOW TABLES""", pdOutput)
        else:
            tables = []
            tableTuples = self.execute("""SHOW TABLES""", pdOutput)
            for i in range(len(tableTuples)):
                tables.append(tableTuples[i][0])
            return tables

    def getAttributes(self, table: str,pdOutput: bool = False):
        return self.execute(f"""PRAGMA table_info({table})""", pdOutput)
    
    """  key-functions  """
    def connectDB(self, dbPath: str):
        try:
            self.disconnectDB()
        except:
            pass
        self.__dbConnection = duck.connect(dbPath)
    
    def createTable(self, tableName: str, tableAttributes: list[str]):
        try:
            command = f"""CREATE TABLE IF NOT EXISTS {tableName}("""
            for i in range(len(tableAttributes)-1):
                command += f"{tableAttributes[i]},"
            command+= f"{tableAttributes[len(tableAttributes)-1]})"
            self.execute(command)
        except:
            raise Exception(f"error creating table {tableName}")

    def insertValues(self, table: str, rows: list[tuple,tuple]):
        insertCommand = f"""INSERT INTO {table} ("""
        attributes = []
        for attributeInfo in self.getAttributes(table):
            attributes.append(attributeInfo[1])
        for i, attribute in enumerate(attributes):
            if i == len(attributes)-1:
                insertCommand += f"{attribute}) "
            else:
                insertCommand += f"{attribute},"
        insertCommand += "VALUES ("
        for i, attribute in enumerate(attributes):
            if i == len(attributes)-1:
                insertCommand += "?) "
            else:
                insertCommand += "?,"
                
        for row in rows:
            self.__dbConnection.execute(insertCommand, row)
        self.__dbConnection.commit()
    
    def deleteValues(self, table: str, condition: str) -> bool:
        deleted = False
        try:
            self.execute(f"""DELETE FROM {table} WHERE {condition}""")
            deleted = True
        except Exception as e:
            print(e)
        return deleted
    
    def addCollumn(self, table: str, collumnName: str, collumnType: str) -> None:
        self.execute(f"""ALTER TABLE {table} ADD COLUMN {collumnName} {collumnType}""")
    
    def renameTable(self, table: str, newTablename: str) -> None:
        self.execute(f"""ALTER TABLE {table} RENAME TO {newTablename}""")
    
    def deleteTable(self, table: str):
        self.execute(f"""DROP TABLE IF EXISTS {table}""")
    
    def disconnectDB(self):
        self.__dbConnection.close()
    
    def deleteDB(self):
        try:
            os.remove(self.DBpath)
        except Exception as e:
            raise Exception(f"error deleting self:\n{e}")
    
    def execute(self, command:str, pdOutput: bool= False, *args) -> list[tuple]|pd.DataFrame:
        if not args:
            result = self.__dbConnection.execute(command).fetchall()
        else:
            result = self.__dbConnection.execute(command, args).fetchall()
        
        if not pdOutput:
            return result
        else:
            try:
                pandasOutput = pd.DataFrame(result)
                return duck.sql("""SELECT * FROM pandasOutput""")
            except:
                return "min 1 value"
            
    
    """  magic-functions  """
    def __str__(self):
        return "class for interacting with a DB via duckdb"
"""
dbms = DBMS("backend\\l0ck3rdb.duckdb")
print(dbms.execute("SELECT * FROM users", True))

print(dbms.deleteValues("users", "username = 'user'"))
print(dbms.execute("SELECT * FROM users", True))"""