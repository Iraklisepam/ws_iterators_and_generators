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
        self._lines = iter(lines)
        self._cursor = 0
    
    def __iter__(self) -> OrdersIterator:
        return self
        
    @staticmethod
    def _line_parser(line: str, index: int) -> Order:
        try:
            data = line.split(',')
            return Order(
                id=index,
                order_id=data[0],
                customer_name=data[1],
                customer_email=data[2],
                product=data[3],
                category=data[4],
                amount=int(data[5]),
                unit_price=float(data[6]),
                order_date=data[7],
                country=data[8],
                status=data[9],
                line_error=False
            )
        except Exception as e:
            print(f"Error happened: {str(e)}")
            return Order(
                id=index,
                order_id="",
                customer_name="",
                customer_email="",
                product="",
                category="",
                amount=0,
                unit_price=0.0,
                order_date="",
                country="",
                status="",
                line_error=False
            )

    def __next__(self) -> Order:
        line = next(self._lines)
        self._cursor += 1
        return self._line_parser(line, self._cursor)
    

def paid_sales(orders: Orders) -> Iterator[Order]:
    """Yield only paid orders."""
    for order in orders:
        if order.status == 'paid':
            yield order

def above_threshold(
    orders: Iterable[Order],
    threshold: int,
) -> Iterator[Order]:
    """Yield only orders with an <price * amount> greater than or equal to threshold."""
    for order in orders:
        if order.unit_price * order.amount >= threshold:
            yield order


def report_all_sales(
    orders: Orders,
    threshold: int,
) -> tuple[int, float]:
    """Report total amount and total revenue for paid orders above threshold."""
    selected = above_threshold(paid_sales(orders), threshold=threshold)
    total_sum = 0.0
    total_order_count = 0
    for order in selected:
        total_sum += order.amount * order.unit_price
        total_order_count += 1
    return total_order_count, total_sum
