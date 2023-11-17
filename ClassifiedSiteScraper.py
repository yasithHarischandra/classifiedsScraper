
class ClassifiedSiteScraper:
        def __init__(self):
                self.siteUrl = ''
                self.myVehicles = []

        def findVehicleType(detailString):
                pass

        def findAdDate(detailString):
                pass
        
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

        #go through the entire site and pull all the ads
        def traverseSite():
                
                #start with first page
                page = ClassifiedSiteScraper.siteUrl
                while page != None:
                        ClassifiedSiteScraper.browseAdListPage(page)
                        page = ClassifiedSiteScraper.getNextAdListPage(page)
        