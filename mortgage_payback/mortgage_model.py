from typing import NamedTuple
from dataclasses import dataclass, fields
from utils import Money, Utils
from typing import Protocol
from i18n.i18n import get_text


@dataclass
class Results:
    total_paid_capital: Money = 0
    total_paid_interest: Money = 0
    fixed_month_payment: Money = 0

    def __repr__(self):
        total_paid_capital_text = get_text("total_paid_capital")
        total_paid_interest_text = get_text("total_paid_interest")
        fixed_month_payment_text = get_text("fixed_month_payment")

        return (
            f"{total_paid_capital_text}: {self.total_paid_capital}, "
            f"{total_paid_interest_text}: {self.total_paid_interest}, "
            f"{fixed_month_payment_text}: {self.fixed_month_payment}"
        )


@dataclass
class State:
    payment: Money = 0
    interest: Money = 0
    capital: Money = 0
    month_payment: Money = 0
    current_mortgage: Money = 0
    overpayment: Money = 0

    def __repr__(self):
        result = ""
        fields_names = {field.name: field.type for field in fields(State)}
        for name in fields_names.keys():
            v = round(getattr(self, name), 2)
            name = get_text(name)
            result += f"{name}: {v}, "
        return result


class CapitalCalculationStrategy(Protocol):
    def __call__(self, year: int, total_years: int, mortgage: Money) -> Money:
        ...


class Params(NamedTuple):
    years: int
    mortgage: Money
    rate: float
    capital_strategy: CapitalCalculationStrategy

    def __repr__(self):
        years_text = get_text("years")
        mortgage_text = get_text("mortgage")
        rate_text = get_text("rate")
        return f"{years_text}: {self.years}, {mortgage_text}: {round(self.mortgage, 2)}, {rate_text}: {self.rate}"
