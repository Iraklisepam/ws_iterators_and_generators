from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator


@dataclass(frozen=True)
class Order:
    id: int
    order_id: str
    customer_name: str
    customer_email: str
    product: str
    category: str
    amount: int
    unit_price: float
    order_date: str
    country: str
    status: str
    line_error: bool = False


class Orders:
    """Reusable iterable that produces a fresh iterator for every iteration."""

    def __init__(self, lines: Iterator[str]) -> None:
        self._iter_lines = lines

    def __iter__(self) -> Iterator[Order]:
        return OrdersIterator(self._iter_lines)

class OrdersIterator:
    """Stateful iterator over CSV-like lines."""

    def __init__(self, lines: Iterator[str]) -> None:
        self._lines=lines
        self._cursor = 0
    
    def __iter__(self) -> OrdersIterator:
        return self
        
    @staticmethod
    def _line_parser(line: str, index: int) -> Order:
        # hope I got the role of index right
        _id = order_id=customer_name=customer_email=product=category=amount=unit_price=order_date=country=status = ''
        try:
            l=list(map(lambda x: x.strip(), line.split(',')))
            order_id, customer_name, customer_email, product, category, amount, unit_price, order_date, country, status =  \
            l[0], l[1], l[2], l[3], l[4], int(l[5]), float(l[-4]), l[-3], l[-2], l[-1]
            return Order(index, order_id, customer_name, customer_email, product, category, amount, unit_price, order_date, country, status)
        except (ValueError, Exception) as e:
            print(e.__cause__)
            return Order(index, order_id, customer_name, customer_email, product, category, amount, unit_price, order_date, country, status, True)


    def __next__(self) -> Order:
        self._cursor += 1
        return self._line_parser(next(self._lines), self._cursor-1)
    

def paid_sales(orders: Orders) -> Iterator[Order]:
    """Yield only paid orders."""
    for order in orders:
        if order.status == "paid":
            yield order

def above_threshold(
    orders: Iterable[Order],
    threshold: int,
) -> Iterator[Order]:
    """Yield only orders with an <price * amount> greater than or equal to threshold."""
    # TODO: implement as a generator
    for order in orders:
        if order.amount * order.unit_price >= threshold:
            yield order


def report_all_sales(
    orders: Orders,
    threshold: int,
) -> tuple[int, float]:
    """Report total amount and total revenue for paid orders above threshold."""
    # FIX: this function has a bug, the total_order_count is always 0
    selected = above_threshold(paid_sales(orders), threshold=threshold)
    items = list(selected)
    total_sum = sum(order.amount * order.unit_price for order in items)
    total_order_count = len(items)
    return total_order_count, total_sum
