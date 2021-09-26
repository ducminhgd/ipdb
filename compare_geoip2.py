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
            headers = ['Network', 'City', 'ISP', 'GeoIP2 City', 'GeoIP2 ISP',
                       'Start Address', 'End Address', 'Number of Addresses']
            _ = input_fh.readline()  # Skip headers
            output_fh.write('\t'.join(headers) + '\n')
            for read_line in input_fh.readlines():
                network, city, isp = read_line.strip().split(',')
                ip_net = IPv4Network(network)

                try:
                    geoip2_city = get_city(ip_net[0]).city.name or 'Other'
                except AddressNotFoundError:
                    geoip2_city = 'Other'

                try:
                    geoip2_isp = get_isp(ip_net[0]).isp or 'Other'
                except AddressNotFoundError:
                    geoip2_isp = 'Other'

                row = [
                    network,
                    city,
                    isp,
                    geoip2_city,
                    geoip2_isp,
                    str(int(ip_net[0])),
                    str(int(ip_net[-1])),
                    str(ip_net.num_addresses),
                ]
                output_fh.write('\t'.join(row) + '\n')  # Some IPS has a comma `,` in their names
                count += 1
    print(f'Done {count} row(s)')
