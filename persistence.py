#contains classes for saving data

from abc import ABC, abstractmethod
from configparser import ConfigParser
import vehicles

#abstract base class for data persistance
class ClassifiedsPersistence(ABC):

    def __init__(self):
        self.dbSettings = {}

    def readConfigFile(self, section):
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read('database.ini')

        # get postgresql section
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                self.dbSettings[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, 'database.ini'))

    @abstractmethod
    def writeToDataSource(self, classified):
        pass

    @abstractmethod
    def openDataSource(self):
        pass

    @abstractmethod
    def closeDataSource(self):
        pass

    @abstractmethod
    def getLastClassifiedDate(self):
        pass


#abstract base class for relational databases
class databasePersistence(ClassifiedsPersistence):

    def __init__(self):
        super().__init__()

    def writeToDataSource(self, classified):
            pass

    def openDataSource(self):
            pass

    def closeDataSource(self):
            pass

    def getLastClassifiedDate(self):
            pass

#PostgreSQL class
class postgresqlPersistence(databasePersistence):

    def __init__(self):
        super().__init__()
        self.readConfigFile('postgresql')

        def writeToDataSource(self, classified):
            pass

        def openDataSource(self):
            pass

        def closeDataSource(self):
            pass

        def getLastClassifiedDate(self):
            pass

