from ckan_scraper import scrape_resources
from geojson_scraper import scrape


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


stations_url = scrape_resources(
    base_url,
    stations_info['dataset'],
    stations_info['return_format'],
    stations_info['extra_fields'],
    'utf-8')
districts_url = scrape_resources(
    base_url,
    districts_info['dataset'],
    districts_info['return_format'],
    districts_info['extra_fields'],
    'utf-8')


if stations_url:
    scrape(stations_url, council_id, 'utf-8', 'stations')
if districts_url:
    scrape(districts_url, council_id, 'utf-8', 'districts')
