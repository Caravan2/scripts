#!/usr/bin/python

import psycopg2
from config import config


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
        """,
        """
        CREATE TABLE companies (
            company_id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
            name VARCHAR(255) NOT NULL,
            vat_number VARCHAR(225),
            logo bytea,
            foundation_date VARCHAR(225)
        )
        """,
        """
        CREATE TABLE addresses (
                address_id SERIAL PRIMARY KEY,
                company_id uuid,
                house_number VARCHAR(225),
                floor VARCHAR(225),
                apartment VARCHAR(225),
                street VARCHAR(225),
                post_code VARCHAR(225),
                city VARCHAR(225),
                region VARCHAR(225),
                country VARCHAR(225),
                geonames_id VARCHAR(225),
                FOREIGN KEY (company_id)
                REFERENCES companies (company_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE phones (
                phone_id SERIAL PRIMARY KEY,
                company_id uuid,
                country_iso VARCHAR(225),
                country_code VARCHAR(225),
                prefix VARCHAR(225),
                phone_number VARCHAR(225),
                extension VARCHAR(225),
                provider VARCHAR(225),
                land_mobile BOOLEAN NOT NULL,
                primary_number BOOLEAN NOT NULL,
                FOREIGN KEY (company_id)
                REFERENCES companies (company_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE emails (
                email_id SERIAL PRIMARY KEY,
                company_id uuid,
                email VARCHAR(225),
                mail_server VARCHAR(225),
                provider_server VARCHAR(225),
                FOREIGN KEY (company_id)
                REFERENCES companies (company_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        # """
        # CREATE TABLE websites (
        #         website_id SERIAL PRIMARY KEY,
        #         company_id uuid,
        #         website VARCHAR(225),
        #         FOREIGN KEY (company_id)
        #         REFERENCES companies (company_id)
        #         ON UPDATE CASCADE ON DELETE CASCADE
        # )
        # """,
        """
        CREATE TABLE business_hours (
                business_hour_id SERIAL PRIMARY KEY,
                company_id uuid,
                days TEXT [],
                hour_from VARCHAR(225),
                hour_to VARCHAR(225),
                FOREIGN KEY (company_id)
                REFERENCES companies (company_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


create_tables()