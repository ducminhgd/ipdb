"""This module is compare input with GeoIP2 DB
Provide an input file contains 3 column: network or IP address, expected city, expected ISP;
    this module will create a CSV file for detail information from GeoIP2.
"""
import os
from ipaddress import IPv4Network
from geoip2.errors import AddressNotFoundError
from utils import get_isp, get_city

INPUT_FILE = os.getenv('INPUT_NETWORK_FILE', 'input_networks.csv')
OUTPUT_FILE = os.getenv('OUTPUT_NETWORK_FILE', 'output_networks.csv')

if __name__ == '__main__':
    count = 0
    with open(INPUT_FILE, 'r') as input_fh:
        print(f'Opened file: {INPUT_FILE}')
        with open(OUTPUT_FILE, 'w') as output_fh:
            print(f'Opened file: {OUTPUT_FILE}')
            headers = [
                'Source Network', 'Source City', 'Source ISP', 'Network', 'Private', 'Int start', 'Int end', 'Num of Addresses',
                'City name', 'City Geoname ID', 'Country name', 'Country ISO code', 'Country Geoname ID',
                'Continent name', 'Continent code', 'Continent Geoname ID',
                'ISP name', 'ISP organization'
            ]
            _ = input_fh.readline()  # Skip headers
            output_fh.write('\t'.join(headers) + '\n')
            for read_line in input_fh.readlines():
                network, city, isp = read_line.replace('"', '').strip().split('\t')
                ip_net = IPv4Network(network)
                is_private = 0

                try:
                    geoip2_city = get_city(ip_net[0])
                    city_name = geoip2_city.city.name or '--'
                    city_geoname_id = geoip2_city.city.geoname_id or '--'
                    country_name = geoip2_city.country.name or geoip2_city.registered_country.name or '--'
                    country_iso_code = geoip2_city.country.iso_code or geoip2_city.registered_country.iso_code or '--'
                    country_geoname_id = geoip2_city.country.geoname_id or geoip2_city.registered_country.geoname_id or '--'
                    continent_name = geoip2_city.continent.name or '--'
                    continent_code = geoip2_city.continent.code or '--'
                    continent_geoname_id = geoip2_city.continent.geoname_id or '--'
                    is_private = int(geoip2_city.traits.ip_address.is_private)
                except AddressNotFoundError:
                    city_name = '--'
                    city_geoname_id = '--'
                    country_name = '--'
                    country_iso_code = '--'
                    country_geoname_id = '--'
                    continent_name = '--'
                    continent_code = '--'
                    continent_geoname_id = '--'

                try:
                    geoip2_isp = get_isp(ip_net[0])
                    isp_name = geoip2_isp.isp or '--'
                    isp_org = geoip2_isp.organization or '--'
                    is_private = int(geoip2_isp.ip_address.is_private)  # Double check again
                    isp_network = geoip2_isp.network.compressed or '--'
                except AddressNotFoundError:
                    isp_name = '--'
                    isp_org = '--'
                    isp_network = '--'

                row = [
                    network,
                    city,
                    isp,
                    isp_network,
                    str(is_private),
                    str(int(ip_net[0])),
                    str(int(ip_net[-1])),
                    str(ip_net.num_addresses),
                    city_name,
                    str(city_geoname_id),
                    country_name,
                    country_iso_code,
                    str(country_geoname_id),
                    continent_name,
                    continent_code,
                    str(continent_geoname_id),
                    isp_name,
                    isp_org,
                ]
                output_fh.write('\t'.join(row) + '\n')  # Some IPS has a comma `,` in their names
                count += 1
    print(f'Done {count} row(s)')
