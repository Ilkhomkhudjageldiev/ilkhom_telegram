from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
from data.config import *


class DataBase:
    def __init__(self):
        self.pool = Union[Pool, None]

    async def conf(self):
        self.pool = await asyncpg.create_pool(
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            database=DB_NAME
        )

    async def execute(self, sql, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      executemany: bool = False,
                      execute: bool = False):

        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(sql, *args)
                elif fetchval:
                    result = await connection.fetchval(sql, *args)
                elif fetchrow:
                    result = await connection.fetchrow(sql, *args)
                elif executemany:
                    result = await connection.executemany(sql, *args)
                elif execute:
                    result = await connection.execute(sql, *args)
            return result

    async def create_table_users(self):
        sql = """
                CREATE TABLE IF NOT EXISTS Users(
                    id BIGINT NOT NULL UNIQUE,
                    full_name VARCHAR(130),
                    phone_number VARCHAR(15)
                )
"""
        await self.execute(sql, execute=True)

    async def create_table_day_types(self):
            sql = """
                CREATE TABLE IF NOT EXISTS Days(
                    id SERIAL PRIMARY KEY,
                    day_code TEXT NOT NULL UNIQUE,
                    day_name TEXT NOT NULL
                )
"""
            await self.execute(sql, execute=True)

    async def create_table_product(self):
        sql = """
                CREATE TABLE IF NOT EXISTS Products(
                id SERIAL PRIMARY KEY,
                product_name TEXT NOT NULL,
                product_photo TEXT,
                product_price TEXT NOT NULL,
                product_description TEXT,
                subcategory_id INTEGER NOT NULL,
                FOREIGN KEY(subcategory_id) REFERENCES Days(id) ON DELETE CASCADE
                    )
"""
        await self.execute(sql, execute=True)

    async def create_table_order_item(self):
            sql = """
                CREATE TABLE IF NOT EXISTS OrderItem(
                id SERIAL PRIMARY KEY,
                day_type TEXT,
                user_id TEXT,
                payment_type TEXT,
                product_name TEXT,
                product_quantity INTEGER,
                product_price BIGINT,
                product_total_price BIGINT,
                comments TEXT,
                date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
                status boolean,
                FOREIGN KEY(day_type) REFERENCES Days(day_code) ON DELETE CASCADE
                )
"""
            await self.execute(sql, execute=True)

    async def insert_user(self, chat_id, full_name, phone_number):
        sql = """
                INSERT INTO Users (id, full_name, phone_number)
                VALUES ($1, $2, $3)
                ON CONFLICT (id) DO NOTHING;
"""
        await self.execute(sql, chat_id, full_name, phone_number, execute=True)

    async def insert_day_types(self, week):
        sql = """
            INSERT INTO Days(day_code, day_name)
            VALUES ($1, $2)
"""
        await self.execute(sql, week, executemany=True)

    async def get_day_info(self, day_code):
        sql = """
            SELECT day_name FROM Days  
            WHERE day_code = $1        
"""
        return await self.execute(sql, day_code, fetchval=True)

    async def get_product_info(self, day_code):
        sql = """
            SELECT * FROM Products  
            WHERE subcategory_id = (
            SELECT id FROM Days
            WHERE day_code = $1
            )     
"""
        return await self.execute(sql, day_code, fetch=True)

    async def get_day_id(self, day_code):
        sql = """
            SELECT id FROM Days  
            WHERE day_code = $1 
"""
        return await self.execute(sql, day_code, fetchval=True)

    async def get_product_order(self, day_id):
        sql = """
            SELECT * FROM Products  
            WHERE subcategory_id = (
            SELECT id FROM Days
            WHERE id = $1
            )     
"""
        return await self.execute(sql, day_id, fetch=True)

    async def get_day_type(self, day_id):
        sql = """
            SELECT day_code FROM Days  
            WHERE id = $1
"""
        return await self.execute(sql, int(day_id), fetchval=True)

    async def insert_product_data(self, product_name, product_photo, product_price, product_description, subcategory_id):
        sql = """
            INSERT INTO Products(product_name, product_photo, product_price, product_description, subcategory_id)
            VALUES ($1, $2, $3, $4, $5)
"""
        await self.execute(sql, product_name, product_photo, product_price, product_description, subcategory_id, execute=True)

    async def insert_customer_info_order(self, day_type, user_id, payment_type, product_name, product_quantity, product_price, product_total_price, comments):
        sql = """
            INSERT INTO OrderItem(day_type, user_id, payment_type, product_name, product_quantity, product_price, product_total_price, comments)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
"""
        await self.execute(sql, day_type, user_id, payment_type, product_name, product_quantity, int(product_price), product_total_price, comments, execute=True)
