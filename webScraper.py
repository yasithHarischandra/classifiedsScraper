
import vehicles
import RiyaSewanaScraper
import persistence

dataSource = persistence.postgresqlPersistence()
dataSource.openDataSource()


myrsScraper = RiyaSewanaScraper.RiyaSewanaScraper(dataSource)
myrsScraper.traverseSiteFrontToBack()
#myrsScraper.traverseSiteBackToFront()

#myrsScraper.extractVehicleData("https://riyasewana.com/buy/mitsubishi-canter-sale-mulleriyawa-7223998")

dataSource.closeDataSource()

