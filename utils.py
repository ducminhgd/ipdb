"""Utility function"""
import os
from ipaddress import IPv4Network
from geoip2.database import Reader, City, ISP

GEOIP2_CITY = os.environ.get('GEOIP2_CITY')
GEOIP2_ISP = os.environ.get('GEOIP2_ISP')


def get_city(ip_address: str) -> City:
    """Get City information from an IP address

    Args:
        ip_address (str): IP address to get information from

    Returns:
        City: City Model of GeoIP2
    """
    with Reader(GEOIP2_CITY) as reader:
        return reader.city(ip_address)


def get_isp(ip_address: str) -> ISP:
    """Get ISP information from an IP address

    Args:
        ip_address (str): IP address to get information from

    Returns:
        ISP: ISP Model of GeoIP2
    """
    with Reader(GEOIP2_ISP) as reader:
        return reader.isp(ip_address)


def get_ipv4_network_info(ip_network: str):
    n = IPv4Network(ip_network)
    return n


if __name__ == '__main__':
    """Just for testing purpose"""
    ip_network = '27.64.0.0/24'
    ip_net = get_ipv4_network_info(ip_network)
    city = get_city(ip_net[0])
    isp = get_isp(ip_net[0])
    print('Done')
