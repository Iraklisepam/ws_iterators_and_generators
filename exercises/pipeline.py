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
    """Reusable iterable that produces a fresh iterator for every iteration.
    P.S This can't be reusable, since we're passing the iterator."""

    def __init__(self, lines: Iterator[str]) -> None:
        self._iter_lines = lines

    def __iter__(self) -> Iterator[Order]:
        return OrdersIterator(self._iter_lines)


class OrdersIterator:
    """Stateful iterator over CSV-like lines."""

    def __init__(self, lines: Iterator[str]) -> None:
        self._lines = lines
        self._cursor = 0

    def __iter__(self) -> OrdersIterator:
        return self

    @staticmethod
    def _line_parser(line: str, index: int) -> Order:
        # TODO:
        # implement line parser that converts a line to an Order instance
        # Handle Exception if the line is not in the expected format,
        # print exception message and return an Order instance with line_error=True

        parts = line.strip("\n").split(",")
        line_error = False
        if len(parts) != 10:
            line_error = True
            parts = (parts + [""] * 10)[:10]

        (
            order_id,
            customer_name,
            customer_email,
            product,
            category,
            str_amount,
            str_unit_price,
            order_date,
            country,
            status,
        ) = parts
        try:
            amount = int(str_amount)
        except ValueError:
            print(
                f"[Row {index}] Failed to convert `amount` to `int`. Invalid input: `{str_amount}`"
            )
            amount = 0
            line_error = True
        try:
            unit_price = float(str_unit_price)
        except ValueError:
            print(
                f"[Row {index}] Failed to convert `unit_price` to `float`. Invalid input: `{str_unit_price}`"
            )
            unit_price = 0.0
            line_error = True

        order = Order(
            id=index,
            order_id=order_id,
            customer_name=customer_name,
            customer_email=customer_email,
            product=product,
            category=category,
            amount=amount,
            unit_price=unit_price,
            order_date=order_date,
            country=country,
            status=status,
            line_error=line_error,
        )
        return order

    def __next__(self) -> Order:
        line = next(self._lines)
        order = self._line_parser(line, self._cursor)
        self._cursor += 1
        return order


def paid_sales(orders: Orders) -> Iterator[Order]:
    """Yield only paid orders."""
    for order in orders:
        if order.status != "paid":
            continue
        yield order


def above_threshold(
    orders: Iterable[Order],
    threshold: int,
) -> Iterator[Order]:
    """Yield only orders with an <price * amount> greater than or equal to threshold."""
    for order in orders:
        if order.amount * order.unit_price < threshold:
            continue
        yield order


def report_all_sales(
    orders: Orders,
    threshold: int,
) -> tuple[int, float]:
    """Report total amount and total revenue for paid orders above threshold."""
    # Issue was in this line. We were exhausting the generator, and then trying to use `len` on it.
    # We either have to convert generator to the list once and then work on this converted list
    # Or dynamically calculate the values per iteration.
    selected = above_threshold(paid_sales(orders), threshold=threshold)

    total_order_count = 0
    total_sum = 0.0
    for order in selected:
        total_order_count += 1
        total_sum += order.amount * order.unit_price

    return (total_order_count, total_sum)
