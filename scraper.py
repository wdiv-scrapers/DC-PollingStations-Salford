import json
from dc_base_scrapers.ckan_scraper import CkanScraper
from dc_base_scrapers.common import get_data_from_url
from dc_base_scrapers.geojson_scraper import (
    GeoJsonScraper,
    RandomIdGeoJSONScraper
)


class SalfordCkanScraper(CkanScraper):

    def get_data(self):
        data_str = get_data_from_url(self.url)
        data = json.loads(data_str.decode(self.encoding))

        if 'tracking_summary' in data['result']:
            del(data['result']['tracking_summary'])

        for resource in data['result']['resources']:
            if 'tracking_summary' in resource:
                del(resource['tracking_summary'])

        return (
            bytes(json.dumps(data, sort_keys=True, indent=4), 'utf-8'), data)


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


stations_meta_scraper = SalfordCkanScraper(
    base_url,
    council_id,
    stations_info['dataset'],
    stations_info['return_format'],
    stations_info['extra_fields'],
    'utf-8')
stations_url = stations_meta_scraper.scrape()

districts_meta_scraper = SalfordCkanScraper(
    base_url,
    council_id,
    districts_info['dataset'],
    districts_info['return_format'],
    districts_info['extra_fields'],
    'utf-8')
districts_url = districts_meta_scraper.scrape()


if stations_url:
    stations_scraper = RandomIdGeoJSONScraper(
        stations_url, council_id, 'utf-8', 'stations')
    stations_scraper.scrape()

if districts_url:
    districts_scraper = GeoJsonScraper(
        districts_url, council_id, 'utf-8', 'districts')
    districts_scraper.scrape()
