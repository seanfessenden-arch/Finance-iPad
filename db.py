#!/bin/python

import sqlite3 as lite
import enums

class DB:

    def __init__(self, name: str) -> None:
        """
        Open a connection to the database.
        """

        self.name = name
        self.conn = lite.connect(name)
        self.conn.execute(
            "PRAGMA foreign_keys = ON"
            )
        self.cursor = self.conn.cursor()
        self.create_tables()

#Functions for Context Manager Support
    def __enter__(self):
        return self

    def __exit__(
    	self,
    	exc_type,
    	exc_val,
    	exc_tb
		):
    	self.close()
#end init

    def create_tables(self):
        """
        Create all required tables.
        """
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS stocks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT UNIQUE,
            name TEXT
        );
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_prices(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            high REAL,
            low REAL,
            last_price REAL,

            FOREIGN KEY (stock_id)
            REFERENCES Stocks(id)
            ON DELETE CASCADE

            UNIQUE(stock_id, date)
        );
        """)

        self.cursor.execute("""
		CREATE TABLE IF NOT EXISTS transactions(
    	id INTEGER PRIMARY KEY AUTOINCREMENT,
    	stock_id INTEGER NOT NULL,
    	transaction_type TEXT NOT NULL,
    	quantity REAL NOT NULL,
    	price REAL NOT NULL,
    	date TEXT NOT NULL,

    	FOREIGN KEY (stock_id)
        REFERENCES stocks(id)
        ON DELETE CASCADE
		);
        """)

# Index for looking up latest prices
        self.cursor.execute("""
    	CREATE INDEX IF NOT EXISTS
    	idx_stockprices_stock_date
    	ON stock_prices(stock_id, date);
    	""")

# Index for joining positions to stocks
        self.cursor.execute("""
    	CREATE INDEX IF NOT EXISTS
    	idx_transactions_stock
    	ON transactions(stock_id);
    	""")


        self.conn.commit()
#end create tables

    def add_stock(self, symbol: str, name: str)-> None:
        """
        Add a stock symbol.
        Ignore duplicates.
        """

        print(f"Adding stock info: {symbol=}, {name=}")

        self.cursor.execute("""
        INSERT OR IGNORE INTO Stocks
        (
            symbol,
            name
        )
        VALUES (?, ?)
        """, (symbol, name))

        print(f"Rows affected: {self.cursor.rowcount}")
        self.conn.commit()
#end add stock

    def delete_stock(self, symbol: str)-> None:
        """
        Delete a stock .
        """

        print(f"Deleting stock info: {symbol=}")

        self.cursor.execute("""
        DELETE FROM Stocks
        where  symbol = ?
        """, (symbol,))

        print(f"Rows affected: {self.cursor.rowcount}")
        self.conn.commit()
#end delete stock

    def get_stock_id(self, symbol):
    	self.cursor.execute("""
    	SELECT id
    	FROM Stocks
    	WHERE symbol = ?
		""", (symbol,))

    	row = self.cursor.fetchone()

    	if row is None:
        	raise ValueError(
            f"Stock symbol '{symbol}' not found"
        	)

    	return row[0]
#end get stock id


    def add_transaction(
        self,
        symbol,
        transaction_type,
        quantity,
        price,
        date
    ):
        """
        Add a transaction for a stock.
        """

        stock_id = self.get_stock_id(symbol)

        self.cursor.execute("""
        INSERT INTO transactions
        (
            stock_id,
            transaction_type,
            quantity,
            price,
            date
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            stock_id,
            transaction_type,
            quantity,
            price,
            date
        ))

        self.conn.commit()

    def add_stock_price(
        self,
        symbol,
        date,
        high,
        low,
        last_price
    ):
        """
        Add daily pricing information.
        """

        stock_id = self.get_stock_id(symbol)

        self.cursor.execute("""
        INSERT OR REPLACE INTO stock_prices
        (
            stock_id,
            date,
            high,
            low,
            last_price
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            stock_id,
            date,
            high,
            low,
            last_price
        ))

        self.conn.commit()

    def get_stock_list(self):
        """
        Return all stocks.
        """

        self.cursor.execute("""
        SELECT
            symbol,
            name
        FROM Stocks
        ORDER BY symbol
        """)

        return self.cursor.fetchall()

    def get_transactions(self, symbol=None):
        """
        Return one transaction or all transactions.
        """
        if symbol is None:

            self.cursor.execute("""
            SELECT
                s.symbol,
                p.quantity,
                p.price,
                p.date
            FROM transactions p
            JOIN Stocks s
                ON p.stock_id = s.id
            ORDER BY s.symbol
            """)

            return self.cursor.fetchall()

        self.cursor.execute("""
        SELECT
            s.symbol,
            p.quantity,
            p.price,
            p.date
        FROM transactions p
        JOIN Stocks s
            ON p.stock_id = s.id
        WHERE s.symbol = ?
        """, (symbol,))

        return self.cursor.fetchone()

    def get_transaction_values(self):
        """
        Return current transaction values
        and transaction total.

        Uses the most recent pricing
        record for each stock.
        """

        self.cursor.execute("""
        SELECT
            s.symbol,
            p.quantity,
            p.price,
            sp.last_price,

            (p.quantity * sp.last_price)
                AS current_value,

            ((sp.last_price - p.price)
                * p.quantity)
                AS gain_loss

        FROM transactions p

        JOIN stocks s
            ON p.stock_id = s.id

        JOIN stock_prices sp
            ON sp.stock_id = s.id

        WHERE sp.date =
        (
            SELECT MAX(sp2.date)
            FROM stock_prices sp2
            WHERE sp2.stock_id = s.id
        )

        ORDER BY current_value DESC
        """)

        rows = self.cursor.fetchall()

        total_value = sum(
            row[4]
            for row in rows
        )

        return rows, total_value

    def drop_tables(self):
        """
        Drop all tables.
        """

        print("Dropping tables...")

        self.cursor.execute(
            "DROP TABLE IF EXISTS transactions"
        )

        self.cursor.execute(
            "DROP TABLE IF EXISTS stock_prices"
        )

        self.cursor.execute(
            "DROP TABLE IF EXISTS stocks"
        )

        self.conn.commit()

        return "Tables Dropped"

    def close(self):
        """
        Close the database connection.
        """

        self.conn.close()

if __name__ == '__main__':
    symbol = 'FPURX'
    symbol2 = 'ECHO'
    date ='2026-06-24'
    high= 12.34
    low= 11.34
    last_price= 13.34
    quantity=563
    purchase_price= 9.85
    purchase_dt='2025-04-23'

    try:
        with DB("test.db") as db:
            db.drop_tables()
            db.create_tables()
            db.add_stock( symbol, "Puritan fund")
            db.add_stock( symbol2, "Echostar")
            db.add_stock( 'CVNA', "Carvana")

            for row in db.get_stock_list():
                print(f"{row=}")

            db.delete_stock(symbol2)

            db.add_stock_price(symbol, date, high, low, last_price)
            db.add_stock_price("CVNA", date, high, low, last_price)
            db.add_transaction( symbol, "BUY", quantity, purchase_price, purchase_dt)
            db.add_transaction( 'CVNA', "BUY", 13, 10.2, '2026-06-30')
            rows, tval = db.get_transaction_values()
            print("####")
            print(f"{rows}, total value is {tval}")
            print("####")

            transactions = db.get_transactions('FPURX')
            print(f"{transactions=}")
    except ValueError as e:
        print(e)
