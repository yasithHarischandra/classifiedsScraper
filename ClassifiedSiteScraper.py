
class ClassifiedSiteScraper:
        siteUrl = ''
        def __init__(self):
                
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

        # this function goes through the list of ads in the page
        # and returns the URL of next ad list page
        def browseAdListPage(adListPageUrl):
                pass

        #go through the entire site and pull all the ads
        def traverseSite(self):
                pass
        