#contains classes for saving data

from abc import ABC, abstractmethod
from configparser import ConfigParser
from datetime import datetime, timedelta, date
import psycopg2
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
            return False

    def closeDataSource(self):
            pass

    def getLastClassifiedDate(self):
            pass

#PostgreSQL class
class postgresqlPersistence(databasePersistence):

    def __init__(self):
        super().__init__()
        self.readConfigFile('postgresql')
        self.conn = None

    def writeToDataSource(self, classified):
        return self.writeVehicleAd(classified)

    def openDataSource(self):
        try:
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(**self.dbSettings)
            
            # create a cursor
            cur = self.conn.cursor()
            
        # execute a statement
            print('PostgreSQL database version:')
            cur.execute('SELECT version()')

            # display the PostgreSQL database server version
            db_version = cur.fetchone()
            print(db_version)
        
        # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            if self.conn is not None:
                self.conn.close()
                print('Database connection closed due to error.')
            return False
        return True


    def closeDataSource(self):
        if self.conn is not None:
            self.conn.close()
            print('Database connection closed.')

    def getLastClassifiedDate(self):
        sql = """SELECT vehicle_ad_date
                 FROM classifieds.vehicle_ad
                 ORDER BY vehicle_ad_date DESC
                 LIMIT 1;"""
        latestDate = [None]
        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            latestDate = cur.fetchone()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        
        return latestDate[0]

    def getCityId(self, city):
        insertSql = """INSERT INTO classifieds.city(city) 
                  VALUES(%s)
                  ON CONFLICT (city) DO NOTHING 
                  RETURNING city_id"""
        getIdSql = """SELECT city_id FROM classifieds.city
                       WHERE city = %s"""
        cityId = None
        try:
            cur = self.conn.cursor()
            
            cur.execute(getIdSql, (city,))
            cityId = cur.fetchone()
            if cityId == None:
                cur.execute(insertSql, (city,))
                cityId = cur.fetchone()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return cityId[0]
    
    def getVehicleTypeId(self, type):
        insertSql = """INSERT INTO classifieds.vehicle_type(vehicle_type) 
                  VALUES(%s)
                  ON CONFLICT (vehicle_type) DO NOTHING 
                  RETURNING vehicle_type_id"""
        getIdSql = """SELECT vehicle_type_id FROM classifieds.vehicle_type
                       WHERE vehicle_type = %s"""
        typeId = None
        try:
            cur = self.conn.cursor()

            cur.execute(getIdSql, (type,))
            typeId = cur.fetchone()
            if typeId == None:
                cur.execute(insertSql, (type,))
                typeId = cur.fetchone()
            
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return typeId[0]
    
    def getVehicleMakerId(self, make):
        insertSql = """INSERT INTO classifieds.vehicle_maker(vehicle_maker) 
                  VALUES(%s)
                  ON CONFLICT (vehicle_maker) DO NOTHING 
                  RETURNING vehicle_maker_id"""
        getIdSql = """SELECT vehicle_maker_id FROM classifieds.vehicle_maker
                       WHERE vehicle_maker = %s"""
        makeId = None
        try:
            cur = self.conn.cursor()
            
            cur.execute(getIdSql, (make,))
            makeId = cur.fetchone()
            if makeId == None:
                cur.execute(insertSql, (make,))
                makeId = cur.fetchone()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return makeId[0]
    
    def getVehicleModelId(self, model, makeId):
        insertSql = """INSERT INTO classifieds.vehicle_model(vehicle_model, vehicle_maker_id) 
                  VALUES(%s, %s)
                  ON CONFLICT (vehicle_model) DO NOTHING 
                  RETURNING vehicle_model_id"""
        getIdSql = """SELECT vehicle_model_id FROM classifieds.vehicle_model
                       WHERE vehicle_model = %s"""
        modelId = None
        try:
            cur = self.conn.cursor()
            
            cur.execute(getIdSql, (model,))
            modelId = cur.fetchone()
            if modelId == None:
                cur.execute(insertSql, (model, makeId))
                modelId = cur.fetchone()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return modelId[0]
    
    def writeVehicleAd(self, vehicleAd):
         if type(vehicleAd) != vehicles.Vehicle:
              return 'not_vehicle'
         
         checkDuplicateSql = """SELECT COUNT(vehicle_ad_url) FROM classifieds.vehicle_ad WHERE vehicle_ad_url = %s"""
         
         try:
            cur = self.conn.cursor()
            cur.execute(checkDuplicateSql, (vehicleAd.adURL,))
            row = cur.fetchone()
            if row[0] != 0:
                return 'duplicate'
            
            typeId = self.getVehicleTypeId(vehicleAd.type)
            makerId = self.getVehicleMakerId(vehicleAd.make)
            modelId = self.getVehicleModelId(vehicleAd.model, makerId)
            cityId = self.getCityId(vehicleAd.city)
            
            insertAdSql = """INSERT INTO classifieds.vehicle_ad(
                                vehicle_type_id, 
                                vehicle_maker_id,
                                vehicle_model_id,
                                vehicle_ad_year,
                                vehicle_ad_mileage,
                                vehicle_ad_transmission,
                                vehicle_ad_fuel_type,
                                vehicle_ad_engine_capacity,
                                vehicle_ad_start_type,
                                vehicle_ad_price,
                                vehicle_ad_url,
                                vehicle_ad_date,
                                city_id,
                                vehicle_ad_contactno,
                                vehicle_ad_options,
                                vehicle_ad_details
                                ) 
                           VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                  ON CONFLICT (vehicle_ad_url) DO NOTHING 
                  RETURNING vehicle_ad_id"""
            
            cur.execute(insertAdSql, (typeId, makerId, modelId, vehicleAd.year, vehicleAd.mileage, 
                                      vehicleAd.transmission, vehicleAd.fuel, vehicleAd.engineCapacity,
                                      vehicleAd.startType,
                                      vehicleAd.price, vehicleAd.adURL, vehicleAd.date, cityId, vehicleAd.contactNo, vehicleAd.options, vehicleAd.details,))

            self.conn.commit()

         except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return str(error)

         return None


