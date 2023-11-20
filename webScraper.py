
import vehicles
import RiyaSewanaScraper
import persistence

dataSource = persistence.postgresqlPersistence()

myrsScraper = RiyaSewanaScraper.RiyaSewanaScraper()
myrsScraper.traverseSite()


