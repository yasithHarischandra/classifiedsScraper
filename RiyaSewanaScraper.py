from bs4 import BeautifulSoup
from urllib.request import urlopen
import ClassifiedSiteScraper

class RiyaSewanaScraper(ClassifiedSiteScraper.ClassifiedSiteScraper):
        def __init__(self):
                self.siteUrl = 'https://riyasewana.com/search'

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
                
                print()
                print(singleAdPageUrl)
                print(singleAdSoup.h1.text)
                print(singleAdSoup.h2.text)
                vehicleType = RiyaSewanaScraper.findVehicleType(singleAdSoup.h1.text)
                adPostDate = RiyaSewanaScraper.findAdDate(singleAdSoup.h2.text)
                adCity = RiyaSewanaScraper.findAdCity(singleAdSoup.h2.text)
                contact, price = getRowProperties(2)

                #We do not want bicycles:
                if vehicleType == 'bicycle':
                    return None
                
                makeRowIndex = 4
                # need to optimise below line
                # if "Get Leasing" in dataTable: makeRowIndex -= 1
                if vehicleType == 'heavyduty' or vehicleType == 'tractor' or vehicleType == 'lorry' or vehicleType == 'other' or vehicleType == 'crewcab' or vehicleType == 'bus':
                    makeRowIndex -= 1
                
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
                
                

                print(vehicleType)
                print(adPostDate)
                print(adCity)
                print("make =", make)
                print("model =", model)
                print("YoM =", yom)
                print("Mileage =", mileage)
                print("Price =", price)
                print("Contact =", contact)
                print("Details =", details)

                


        def findVehicleType(detailString):
                vType = ''
                if ' Car ' in detailString:
                        vType = 'car'
                elif ' Motorbike ' in detailString:
                        vType = 'motorbike'
                elif ' Three Wheel ' in detailString:
                        vType = 'threewheel'
                elif ' Van ' in detailString:
                        vType = 'van'
                elif ' SUV ' in detailString:
                        vType = 'suv'
                elif ' Lorry ' in detailString:
                        vType = 'lorry'
                elif ' Tractor ' in detailString:
                        vType = 'tractor'
                elif ' Crew Cab ' in detailString:
                        vType = 'crewcab'
                elif ' Pickup ' in detailString:
                        vType = 'pickup'
                elif ' Bus ' in detailString:
                        vType = 'bus'
                elif ' Bicycle ' in detailString:
                        vType = 'bicycle'
                elif ' Heavy-Duty ' in detailString:
                        vType = 'heavyduty'
                elif ' Other ' in detailString:
                        vType = 'other'
                else:
                        vType = 'other'
                return vType

        #Find the date ad was posted
        def findAdDate(detailString):
                postDate = ''
                if '202' in detailString:
                        index = detailString.find("202")
                        postDate = detailString[index: index+10]
                return postDate
        
        #Find the city where the vehicle is in
        def findAdCity(detailString):
                postDate = ''
                if '202' in detailString:
                        index = detailString.find(",")
                        town = detailString[index+2: ]
                return town

        # this function goes through the list of ads in the page
        def browseAdListPage(self, adListPageUrl):

                #first open the page,
                page = urlopen(adListPageUrl)
                html = page.read().decode("utf-8",'ignore')
                soup = BeautifulSoup(html, "html.parser")

                #now find the table of ads and iterate through it
                for tag in soup.find_all('li', "item round"):
                        singlePageLink = tag.find('a')
                        pageURL = singlePageLink.get('href')

                        self.extractVehicleData(pageURL)
                        #break
        
        def getNextAdListPage(self, currentpageUrl):
                return None

        #go through the entire site and pull all the ads
        def traverseSite(self):
                
                #start with first page
                page = self.siteUrl
                while page != None:
                        self.browseAdListPage(page)
                        page = self.getNextAdListPage(page)