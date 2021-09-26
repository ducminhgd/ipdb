"""This module for testing check IP address from GeoIP2 databases"""

from utils import get_isp, get_city

if __name__ == '__main__':
    ip_address = '27.64.0.1'
    _ = get_isp(ip_address)
    _ = get_city(ip_address)
    print('Done')
