from dc_base_scrapers.ckan_scraper import CkanScraper
from dc_base_scrapers.geojson_scraper import GeoJsonScraper
from dc_base_scrapers.xml_scraper import Wfs2Scraper


base_url = 'https://salforddataquay.uk/api/3/action/package_show?id='

stations_info = {
    'dataset': 'salford-polling-stations',
    'extra_fields': ['revision_timestamp'],
    'return_format': 'geojson',
}

districts_info = {
    'dataset': 'salford-polling-districts',
    'extra_fields': ['revision_timestamp'],
    'return_format': 'geojson'
}

council_id = 'E08000006'


stations_meta_scraper = CkanScraper(
    base_url,
    stations_info['dataset'],
    stations_info['return_format'],
    stations_info['extra_fields'],
    'utf-8')
stations_meta_scraper.scrape()
stations_url = "http://map.salford.gov.uk/geoserver/OpenData/ows?service=wfs&version=2.0.0&request=GetFeature&typeNames=OpenData%3Av_polling_stations&srsName=EPSG%3A4326"
stations_fields = {
    '{http://www.salford.gov.uk/maps/OpenData}id': 'id',
    '{http://www.salford.gov.uk/maps/OpenData}ward': 'ward',
    '{http://www.salford.gov.uk/maps/OpenData}polling_district': 'polling_district',
    '{http://www.salford.gov.uk/maps/OpenData}station_location': 'station_location',
    '{http://www.salford.gov.uk/maps/OpenData}easting': 'easting',
    '{http://www.salford.gov.uk/maps/OpenData}northing': 'northing',
    '{http://www.salford.gov.uk/maps/OpenData}longitude_wgs_84': 'longitude_wgs_84',
    '{http://www.salford.gov.uk/maps/OpenData}latitude_wgs_84': 'latitude_wgs_84',
}

districts_meta_scraper = CkanScraper(
    base_url,
    districts_info['dataset'],
    districts_info['return_format'],
    districts_info['extra_fields'],
    'utf-8')
districts_url = districts_meta_scraper.scrape()


if stations_url:
    stations_scraper = Wfs2Scraper(
        stations_url, council_id, 'stations', stations_fields, 'id')
    stations_scraper.scrape()

if districts_url:
    districts_scraper = GeoJsonScraper(
        districts_url, council_id, 'utf-8', 'districts')
    districts_scraper.scrape()
