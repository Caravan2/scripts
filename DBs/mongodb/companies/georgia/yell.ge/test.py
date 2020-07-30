#!/usr/bin/python

import psycopg2
from config import config
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Companies"]
mycol = mydb["yell.ge"]


def Check_Company(vat):
    """ query data from the vendors table """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(f"SELECT company_id, name FROM companies WHERE vat_number = '{vat}'")
        
        row = cur.fetchone()

        # while row is not None:
        #     print(row)
        #     row = cur.fetchone()

        cur.close()

        print(cur.rowcount)
        return cur.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

Check_Company("404903985")