
import vehicles
import RiyaSewanaScraper
import persistence

dataSource = persistence.postgresqlPersistence()
dataSource.openDataSource()


myrsScraper = RiyaSewanaScraper.RiyaSewanaScraper(dataSource)
myrsScraper.traverseSiteFrontToBack()
#myrsScraper.traverseSiteBackToFront()

#myrsScraper.extractVehicleData("https://riyasewana.com/buy/isuzu-car-carrier-sale-colombo-6842177")

dataSource.closeDataSource()

