# Classifieds scraper
This is a web scraper which goes through Sri Lankan classifieds sites and extract data from advertisements selling vehicles and will push those data to a database. 
Currently it supports https://riyasewana.com/ and PostgreSQL. It is planned to be extended to other sites as well.
Database information is saved in the following format in database.ini file.
[postgresql]
host=hostserver
port=5432
database=classifieds
user=postgres
password=pa55wp0rd
