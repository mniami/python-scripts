from typing import Dict
from mortgage import MortgagePayment, Overpayment
from mortgage_model import Params
from strategies import Strategies
from i18n.i18n import get_text


class Simulation:
    def __init__(
        self, mortgagePayment: MortgagePayment, overpayment: Overpayment
    ) -> None:
        self.mortgagePayment = mortgagePayment
        self.overpayment = overpayment

    def run(self):
        year = 1
        print(self.mortgagePayment.params)
        while self.mortgagePayment.state.current_mortgage > 0:
            if self.overpayment:
                self.overpayment.pay(year, self.mortgagePayment)
            self.mortgagePayment.pay_off(year)
            year_text = get_text("year")
            print(f"{year_text}: {year}", self.mortgagePayment.state)
            year += 1

        print(self.mortgagePayment.results)


def simulate(params: Params, overpayments: Dict[int, int] = None):
    Simulation(MortgagePayment(params), Overpayment(overpayments)).run()


__all__ = ["simulate", "Strategies", "Params"]
