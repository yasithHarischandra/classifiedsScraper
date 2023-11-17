from bs4 import BeautifulSoup
from urllib.request import urlopen

class Vehicle:
        def __init__(self, make, model, year, mileage, adNum):
                self.make = make
                self.model = model
                self.year = year
                self.mileage = mileage
                self.adNum = adNum

class ClassifiedSiteScraper:
        def __init__(self):
                self.siteUrl = ''

        def findVehicleType(detailString):
                pass

        def findAdDate(detailString):
                postDate = ''
                if '202' in detailString:
                        index = detailString.find("202")
                        postDate = detailString[index: index+10]
                return postDate
        
        def findAdCity(detailString):
                postDate = ''
                if '202' in detailString:
                        index = detailString.find(",")
                        town = detailString[index+2: ]
                return town

        def extractVehicleData(singleAdPageUrl):
                pass

        def browseAdListPage(adListPageUrl):
                pass

        def getNextAdListPage(currentpageUrl):
                return None

        def traverseSite():
                pass

class RiyaSewanaScraper(ClassifiedSiteScraper):
        def __init__(self):
                self.siteUrl = 'https://riyasewana.com/search'

        def extractVehicleData(self, singleAdPageUrl):
                singleAdPage = urlopen(singleAdPageUrl)
                singleAdHtml = singleAdPage.read().decode("utf-8")
                singleAdSoup = BeautifulSoup(singleAdHtml, "html.parser")
                #print(singleAdSoup.get_text())
                dataTable = singleAdSoup.find('table')
                tableRows = dataTable.find_all('tr')
                
                print()
                print(singleAdPageUrl)
                print(singleAdSoup.h1.text)
                print(singleAdSoup.h2.text)
                print(RiyaSewanaScraper.findAdDate(singleAdSoup.h2.text))
                print(RiyaSewanaScraper.findAdCity(singleAdSoup.h2.text))
                
                #Find make and model
                makeAndModelCells = tableRows[4].find_all('td')
                print("make =", makeAndModelCells[1].text)
                print("model =", makeAndModelCells[3].text)
                makeAndModelCells = tableRows[5].find_all('td')
                print("YoM =", makeAndModelCells[1].text)
                print("Mileage =", makeAndModelCells[3].text)
                makeAndModelCells = tableRows[2].find_all('td')
                print("Price =", makeAndModelCells[3].text)
                print("Contact =", makeAndModelCells[1].text)

        # this function goes through the list of ads in the page
        def browseAdListPage(self, adListPageUrl):

                #first open the page,
                page = urlopen(adListPageUrl)
                html = page.read().decode("utf-8")
                soup = BeautifulSoup(html, "html.parser")

                #now find the table of ads and iterate through it
                for tag in soup.find_all('li', "item round"):
                        singlePageLink = tag.find('a')
                        pageURL = singlePageLink.get('href')

                        self.extractVehicleData(pageURL)
                        break
        
        def getNextAdListPage(self, currentpageUrl):
                return None

        #go through the entire site and pull all the ads
        def traverseSite(self):
                
                #start with first page
                page = self.siteUrl
                while page != None:
                        self.browseAdListPage(page)
                        page = self.getNextAdListPage(page)


myrsScraper = RiyaSewanaScraper()
myrsScraper.traverseSite()


