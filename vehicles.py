class Vehicle:
        def __init__(self, type, make, model, year, mileage, adURL, transmission, 
                     fuelType, engineCC, startType, options, details, date, city, price, contactNo):
                self.type = type
                self.make = make
                self.model = model
                self.year = year
                self.mileage = mileage
                self.adURL = adURL
                self.transmission = transmission
                self.fuel = fuelType
                self.engineCapacity = engineCC
                self.startType = startType
                self.options = options
                self.details = details
                self.date = date
                self.city = city
                self.price = price
                self.contactNo = contactNo

        def __str__(self):  
                return "Make:% s \nModel:% s \nType:% s \nYear:% s \nMileage:% s \nFuel:% s \nEngine capacity:% s \nTransmission:% s \nPrice:% s \nURL:% s \nDate posted:% s \nCity:% s" % (self.make, self.model, self.type, self.year, self.mileage, self.fuel, self.engineCapacity, self.transmission, self.price, self.adURL, self.date, self.city)
                