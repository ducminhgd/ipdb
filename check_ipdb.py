"""This module for testing check IP address from generated database"""
import os
import sqlite3
from ipaddress import IPv4Address
from peewee import SqliteDatabase
from models import IPDbModel

DB_FILE = os.getenv('DB_FILE', 'ipdb.sqlite')
MEM_DB = sqlite3.connect(':memory:')


def progress(status, remaining, total):
    print(f'Copied {total-remaining} of {total} pages...')


def init_memdb():
    print('[Begin] Migrate')
    source = sqlite3.connect(DB_FILE)
    with MEM_DB:
        # source.backup(MEM_DB, pages=1, progress=progress)
        source.backup(MEM_DB)
    source.close()
    print('[End] Migrate')


# If use file: file:tempdb.sqlite?cache=shared
InMemDb = SqliteDatabase(DB_FILE, pragmas={
    'journal_mode': 'wal',
    'cache_size': -1 * 64000,  # 64MB
    'foreign_keys': 1,
    'ignore_check_constraints': 0,
    'synchronous': 0,
})


def test_pure_mem(ip_str: str):
    ip_address = int(IPv4Address(ip_str))
    q = f'SELECT * FROM tbl_ipdb WHERE {ip_address} >= start_address AND {ip_address} <= end_address ORDER BY number_of_address LIMIT 1'
    r = MEM_DB.cursor().execute(q).fetchone()
    MEM_DB.close()
    return r


def test_pure_file(ip_str: str):
    ip_address = int(IPv4Address(ip_str))
    conn = sqlite3.connect(DB_FILE)
    q = f'SELECT * FROM tbl_ipdb WHERE {ip_address} >= start_address AND {ip_address} <= end_address ORDER BY number_of_address LIMIT 1'
    r = conn.cursor().execute(q).fetchone()
    conn.close()
    return r


def test_peewee_file(ip_str: str):
    ip_address = int(IPv4Address(ip_str))
    InMemDb.connect(reuse_if_open=True)
    with InMemDb.connection_context():
        with InMemDb.bind_ctx([IPDbModel, ]):
            r = IPDbModel.select().where(
                IPDbModel.start_address <= ip_address,
                IPDbModel.end_address >= ip_address,
            ).order_by(IPDbModel.number_of_address).first()
            return r


if __name__ == '__main__':
    init_memdb()
    ip_str = '27.64.0.1'
    print(test_pure_mem(ip_str))
