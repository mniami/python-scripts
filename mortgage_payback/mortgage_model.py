from typing import NamedTuple
from dataclasses import dataclass
from utils import Money, Utils
from typing import Protocol


@dataclass
class Results:
    total_paid_capital: Money = 0
    total_paid_interest: Money = 0

    def __repr__(self):
        return "\t".join(Utils.get_all_fields_values(self))


@dataclass
class State:
    year_payment: Money = 0
    month_payment: Money = 0
    current_mortgage: Money = 0

    def __repr__(self):
        return f"year payment: {round(self.year_payment,2)}, month payment: {round(self.month_payment, 2)}, current mortage: {round(self.current_mortgage, 2)}"


class CapitalCalculationStrategy(Protocol):
    def __call__(self, year: int, total_years: int, mortgage: Money) -> Money:
        ...


class Params(NamedTuple):
    years: int
    mortgage: Money
    rate: float
    capital_strategy: CapitalCalculationStrategy

    def __repr__(self):
        return f"years: {self.years}, mortgage: {round(self.mortgage, 2)}, rate: {self.rate}"
