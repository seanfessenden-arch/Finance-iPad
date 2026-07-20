#!/bin/python3
import pytest

from src.db import DB

symbol = 'FSELX'
company = "Fidelity Select Electronics"

@pytest.fixture
def db_instance():
    return DB('portfolio.db')

def test_create_tables(db_instance):
    assert db_instance.create_tables() is True

def test_add_stock(db_instance):
    sym, comp = db_instance.add_stock(symbol, company)
    assert sym == symbol and comp == company

def test_get_stock_id(db_instance):
    stock_id = db_instance.get_stock_id(symbol)
    assert stock_id is not None 

def test_get_stock_list(db_instance):
    sl = db_instance.get_stock_list()
    assert len(sl) > 0 and sl is not None

def test_add_stock_price(db_instance):
    pytest.fail("method not fleshed out")

def test_delete_stock(db_instance): 
    assert db_instance.delete_stock('FPURX') is False
    assert db_instance.delete_stock(symbol) is True

def test_add_transaction(db_instance):
    pytest.fail("method not fleshed out")

def test_get_transactions(db_instance):
    pytest.fail("method not fleshed out")

def test_get_transaction_values(db_instance):
    pytest.fail("method not fleshed out")

def test_drop_tables(db_instance):
    pytest.fail("method not fleshed out")

def test_close(db_instance):
    pytest.fail("method not fleshed out")
