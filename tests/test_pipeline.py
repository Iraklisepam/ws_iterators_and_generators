from exercises.pipeline import report_all_sales, paid_sales, Orders, above_threshold
from typing import Iterable, Iterator
import pytest

@pytest.fixture
def data_fixture():
    return iter([
        "order_id,customer_name,email,product,category,amount,unit_price,order_date,country,status",
        "ORD-0001,Salome Kiknadze,salome.kiknadze1@example.com,Wireless Mouse,Electronics,3,24.90,2026-03-04,Armenia,paid",
        "ORD-0002,Irakli Kiknadze,irakli.kiknadze2@example.com,Pen Set,Stationery,1,6.80,2026-04-19,Georgia,paid",
        "ORD-0003,Giorgi Maisuradze,giorgi.maisuradze3@example.com,Notebook,Stationery,5,4.50,2026-01-07,France,shipped",
        "ORD-0004,Irakli Gogoladze,irakli.gogoladze4@example.com,Backpack,Lifestyle,2,48.25,2026-04-25,France,delivered",
        "ORD-0005,Sandro Beridze,sandro.beridze5@example.com,USB-C Cable,Electronics,4,9.99,2026-03-29,Turkey,paid"
    ])

def test_orders_iterator(data_fixture):
    orders = Orders(data_fixture)
    assert isinstance(orders, Iterable)
    orders_iterator = iter(orders)
    assert isinstance(orders_iterator, Iterator)
    # skip the header
    next(orders_iterator)
    first_order = next(orders_iterator)
    assert first_order.order_id == "ORD-0001"

def test_pipeline(data_fixture):
    orders = Orders(data_fixture)
    assert isinstance(orders, Iterable)
    paid_orders = paid_sales(orders)
    above_threshold_orders = above_threshold(paid_orders, threshold=10)
    reported_orders = list(above_threshold_orders)
    # one paid order with price 6.80, so it should be filtered out
    assert len(reported_orders) == 2

def test_pipeline_paid_orders(data_fixture):
    orders = Orders(data_fixture)
    paid_orders = paid_sales(orders)
    reported_paid_orders = list(paid_orders)
    assert len(reported_paid_orders) == 3

def test_pipeline_above_threshold(data_fixture):
    orders = Orders(data_fixture)
    above_threshold_orders = above_threshold(orders, threshold=10)
    reported_above_threshold_orders = list(above_threshold_orders)
    assert len(reported_above_threshold_orders) == 4

def test_pipeline_report_all_sales(data_fixture):
    orders = Orders(data_fixture)
    total_sales, total_income = report_all_sales(orders, threshold=10)
    assert total_sales == 2
    assert total_income == 3*24.90 + 4*9.99
