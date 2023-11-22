from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime, timedelta, date
import ClassifiedSiteScraper
import vehicles

class RiyaSewanaScraper(ClassifiedSiteScraper.ClassifiedSiteScraper):
        siteUrl = 'https://riyasewana.com/search'
        def __init__(self, dataSource):
                super().__init__(dataSource)
                
                

        def extractVehicleData(self, singleAdPageUrl):
                singleAdPage = urlopen(singleAdPageUrl)
                singleAdHtml = singleAdPage.read().decode("utf-8", 'replace')
                singleAdSoup = BeautifulSoup(singleAdHtml, "html.parser")
                #print(singleAdSoup.get_text())
                dataTable = singleAdSoup.find('table')
                tableRows = dataTable.find_all('tr')

                # returns the two values in a single row
                def getRowProperties(rowindex, getLeftnRight = True):
                        cells = tableRows[rowindex].find_all('td')
                        leftProperty = cells[1].text
                        rightProperty = ''
                        if getLeftnRight:
                            rightProperty = cells[3].text
                        return leftProperty, rightProperty
                
                #print()
                #print(singleAdPageUrl)
                #print(singleAdSoup.h1.text)
                #print(singleAdSoup.h2.text)
                vehicleType = RiyaSewanaScraper.findVehicleType(singleAdSoup.h1.text)
                adPostDate = RiyaSewanaScraper.findAdDate(singleAdSoup.h2.text)
                adCity = RiyaSewanaScraper.findAdCity(singleAdSoup.h2.text)

                #Search for the row where contact no and price is in
                contactRowIndex = 0
                for row in tableRows:
                       if row.find_all('td')[0].text == 'Contact':
                             break
                       contactRowIndex += 1 
                contact, price = getRowProperties(contactRowIndex)

                #We do not want bicycles:
                if vehicleType == 'bicycle' or vehicleType == 'heavyduty':
                    return None
                
                makeRowIndex = contactRowIndex+1

                #Check if the 5th row is leasing ad, if it is not, data starts from 4th row
                fifthRowLabel =  tableRows[makeRowIndex].find_all('td')[0].text
                if fifthRowLabel == 'Get Leasing':
                       makeRowIndex += 1
                
                #if vehicleType == 'heavyduty' or vehicleType == 'tractor' or vehicleType == 'lorry' or vehicleType == 'other' or vehicleType == 'crewcab' or vehicleType == 'bus':
                #    makeRowIndex -= 1
                
                make, model = getRowProperties(makeRowIndex)
                yom, mileage = getRowProperties(makeRowIndex := makeRowIndex+1)
                engineCC = '' 
                startType = ''
                gear = ''
                fuelType = ''
                options = ''
                details = ''

                if vehicleType == 'motorbike':
                    engineCC, startType = getRowProperties(makeRowIndex := makeRowIndex+1)
                    details, _ =  getRowProperties(makeRowIndex := makeRowIndex+2, getLeftnRight=False)
                else:
                    gear, fuelType = getRowProperties(makeRowIndex := makeRowIndex+1)
                    options, engineCC =  getRowProperties(makeRowIndex := makeRowIndex+1)
                    details, _ =  getRowProperties(makeRowIndex := makeRowIndex+1, getLeftnRight=False)
                
                aVehicle = vehicles.Vehicle(vehicleType, make, model, yom, mileage, singleAdPageUrl, gear, fuelType, engineCC, startType, options, details, adPostDate, adCity, price, contact) 
                

                #print(vehicleType)
                #print(adPostDate)
                #print(adCity)
                #print("make =", make)
                #print("model =", model)
                #print("YoM =", yom)
                #print("Mileage =", mileage)
                #print("Price =", price)
                #print("Contact =", contact)
                #print("Details =", details)

                return aVehicle

                
        def findVehicleType(detailString):
                vType = ''
                if ' Heavy-Duty ' in detailString:
                        vType = 'heavyduty'
                elif ' Lorry ' in detailString:
                        vType = 'lorry'
                elif ' Tractor ' in detailString:
                        vType = 'tractor'
                elif ' Motorbike ' in detailString:
                        vType = 'motorbike'
                elif ' Three Wheel ' in detailString:
                        vType = 'threewheel'
                elif ' Van ' in detailString:
                        vType = 'van'
                elif ' SUV ' in detailString:
                        vType = 'suv'
                elif ' Crew Cab ' in detailString:
                        vType = 'crewcab'
                elif ' Pickup ' in detailString:
                        vType = 'pickup'
                elif ' Bus ' in detailString:
                        vType = 'bus'
                elif ' Bicycle ' in detailString:
                        vType = 'bicycle'
                elif ' Car ' in detailString:
                        vType = 'car'
                elif ' Other ' in detailString:
                        vType = 'other'
                else:
                        vType = 'other'
                return vType

        #Find the date ad was posted
        def findAdDate(detailString):
                postDate = ''
                if '202' in detailString:
                        index = detailString.find("on 2023")
                        postDate = detailString[index+3: index+13]
                        year, month, addate = postDate.split("-")
                        convertedDate = date(int(year), int(month), int(addate))
                return convertedDate
        
        #Find the city where the vehicle is in
        def findAdCity(detailString):
                postDateIndex = detailString.find("202")
                if  postDateIndex > 0:
                        subStr = detailString[postDateIndex:]
                        index = subStr.find(",")
                        town = subStr[index+2: ]
                return town

        # this function goes through the list of ads in the page
        # and returns the URL of next ad list page
        def browseAdListPage(self, adListPageUrl, startDate, EndDate):
                myVehicles = []
                #first open the page,
                page = urlopen(adListPageUrl)
                html = page.read().decode("utf-8",'ignore')
                soup = BeautifulSoup(html, "html.parser")

                #now find the table of ads and iterate through it
                for tag in soup.find_all('li', "item round"):
                        singlePageLink = tag.find('a')
                        pageURL = singlePageLink.get('href')

                        print("     " + pageURL)
                        aVehicle = self.extractVehicleData(pageURL)
                        if aVehicle != None:
                                myVehicles.append(aVehicle)
                        
                        #break

                #Find the next page
                nextTag = soup.find('a', string="Next")
                nextURL = None
                if nextTag:
                       nextURL = "https:" + nextTag['href']
                return nextURL, myVehicles
        
        #go through the entire site and pull all the ads
        def traverseSite(self):
                
                #start with first page
                page = self.siteUrl
                while page != None:
                        page, vehicleList = self.browseAdListPage(page)

        def traverseSiteFrontToBack(self):
               Yesterday = date.today() - timedelta(days=1)
               latestSavedAdDate = self.dataSource.getLastClassifiedDate()

               if latestSavedAdDate == Yesterday:
                      print("Database is up to date to yesterday!.")
                      return 'Finished'

               #start with first page
               page = self.siteUrl
               while page != None:
                        page, vehicleList = self.browseAdListPage(page, startDate=Yesterday, EndDate=latestSavedAdDate)
                        for item in vehicleList:
                                #if item.date > Yesterday:
                                # continue
                                if item.date > latestSavedAdDate:
                                  print(item)
                                  writeStatus = self.dataSource.writeToDataSource(item)
                                  if writeStatus == None or writeStatus == 'duplicate':
                                         continue
                                  return writeStatus
                                else:
                                      return 'Finished'
                                
        def traverseSiteBackToFront(self):
               Yesterday = date.today() - timedelta(days=1)
               latestSavedAdDate = self.dataSource.getLastClassifiedDate()

               #start with last page
               # page number is hard coded,
               urlWithNoPageNum = "https://riyasewana.com/search?page="
               pageNum = 278
               page = urlWithNoPageNum+str(pageNum)
               while page != None:
                        print(page)
                        page, vehicleList = self.browseAdListPage(page, startDate=Yesterday, EndDate=latestSavedAdDate)
                        for item in vehicleList:
                                if item.date > Yesterday:
                                 return 'Finished'
                                if item.date > latestSavedAdDate:
                                  print(item)
                                  writeStatus = self.dataSource.writeToDataSource(item)
                                  if writeStatus == None or writeStatus == 'duplicate':
                                         continue
                                  return writeStatus
                                else:
                                       continue
                                
                        pageNum -= 1
                        page = urlWithNoPageNum + str(pageNum)
                        if pageNum < 1: 
                               page = None

                               
                                  

                        
        