"""This module creates an SQLite Database, contains IP Addresses or Networks information
"""
import os
from peewee import SqliteDatabase
from models import IPDbModel

INPUT_FILE = os.getenv('INPUT_NETWORK_FILE', 'output_networks.csv')
OUTPUT_FILE = os.getenv('OUTPUT_NETWORK_FILE', 'ipdb.sqlite?cache=shared')

# If use file: file:tempdb.sqlite?cache=shared
InMemDb = SqliteDatabase(OUTPUT_FILE, pragmas={
    'journal_mode': 'wal',
    'cache_size': -1 * 64000,  # 64MB
    'foreign_keys': 1,
    'ignore_check_constraints': 0,
    'synchronous': 0,
})

if __name__ == '__main__':
    count = 0
    with open(INPUT_FILE, 'r') as input_fh:
        print(f'Opened file: {INPUT_FILE}')
        _ = input_fh.readline()  # Skip headers
        InMemDb.connect(reuse_if_open=True)
        with InMemDb.connection_context():
            with InMemDb.bind_ctx([IPDbModel, ]):
                InMemDb.create_tables([IPDbModel, ])
                for read_line in input_fh.readlines():
                    network, _, _, city, isp, start_address, end_address, number_of_address = read_line.strip().split('\t')
                    IPDbModel.insert(
                        cidr=network,
                        city=city,
                        isp=isp,
                        start_address=int(start_address),
                        end_address=int(end_address),
                        number_of_address=int(number_of_address),
                    ).on_conflict_ignore().execute()
                    count += 1
    print(f'Done {count} row(s)')
