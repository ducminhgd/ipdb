"""This module contains models of data"""

from peewee import Model, CharField, IntegerField, AutoField


class IPDbModel(Model):
    cidr = CharField(max_length=20,primary_key=True)
    city = CharField(max_length=100)
    isp = CharField(max_length=100)
    start_address = IntegerField(index=True)
    end_address = IntegerField(index=True)
    number_of_address = IntegerField(index=True)

    class Meta:
        table_name = 'tbl_ipdb'
        without_rowid = True
