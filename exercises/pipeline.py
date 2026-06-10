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
        # TODO: return a Orders iterator
        raise NotImplementedError("TODO: return OrdersIterator instance")


class OrdersIterator:
    """Stateful iterator over CSV-like lines."""

    def __init__(self, lines: Iterator[str]) -> None:
        # TODO: save the lines and initialize the cursor
        raise NotImplementedError("TODO: save the lines and initialize the cursor")

    def __iter__(self) -> OrdersIterator:
        # TODO: an iterator must return itself
        raise NotImplementedError("TODO: return self")

    @staticmethod
    def _line_parser(line: str, index: int) -> Order:
        # TODO:
        # implement line parser that converts a line to an Order instance
        # Handle Exception if the line is not in the expected format,
        # print exception message and return an Order instance with line_error=True
        raise NotImplementedError(
            "TODO: implement line parser that converts a line to an Order instance"
        )

    def __next__(self) -> Order:
        # TODO:
        # Return the next order.
        raise NotImplementedError("TODO: Return the next order")


def paid_sales(orders: Orders) -> Iterator[Order]:
    """Yield only paid orders."""
    # TODO: implement as a generator
    raise NotImplementedError("TODO: implement as a generator")


def above_threshold(
    orders: Iterable[Order],
    threshold: int,
) -> Iterator[Order]:
    """Yield only orders with an <price * amount> greater than or equal to threshold."""
    # TODO: implement as a generator
    raise NotImplementedError("TODO: implement as a generator")


def report_all_sales(
    orders: Orders,
    threshold: int,
) -> tuple[int, float]:
    """Report total amount and total revenue for paid orders above threshold."""
    # FIX: this function has a bug, the total_order_count is always 0
    selected = above_threshold(paid_sales(orders), threshold=threshold)
    total_sum = sum(order.amount * order.unit_price for order in selected)
    total_order_count = len(list(selected))
    return (total_order_count, total_sum)
