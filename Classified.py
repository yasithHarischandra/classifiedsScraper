#Contains classified base class

from abc import ABC, abstractmethod

class Classified(ABC):
    def __init__(self, price, contactNo, date, city, adURL, details):
        super().__init__()
        self.price = price
        self.contactNo = contactNo
        self.date = date
        self.city = city
        self.adURL = adURL
        self.details = details