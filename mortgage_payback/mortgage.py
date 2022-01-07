from dataclasses import dataclass
from typing import Dict
from utils import Money
from mortgage_model import Results, State, Params


class MortgagePayment:
    def __init__(
        self,
        params: Params,
    ):
        self.params = params
        self.state = State()
        self.results = Results()

        self.state.current_mortgage = self.params.mortgage

    def __get_capital(self, year: int) -> Money:
        capital_year = self.params.capital_strategy(
            year, self.params.years, self.params.mortgage
        )
        capital = (
            self.state.current_mortgage
            if self.state.current_mortgage < capital_year
            else capital_year
        )
        if capital < self.state.current_mortgage and self.state.overpayment > 0:
            real_overpayment = min(
                self.state.current_mortgage - capital, self.state.overpayment
            )
            self.state.overpayment = real_overpayment
            capital += real_overpayment
        return capital

    def __get_interest(self) -> Money:
        return self.params.rate * self.state.current_mortgage

    @staticmethod
    def __payment(capital: float, interest: float) -> Money:
        return interest + capital

    def __get_fixed_payment_monthly(self, year: int) -> Money:
        return (
            (self.results.total_paid_capital + self.results.total_paid_interest)
            / year
            / 12
        )

    def pay_off(self, year: int):
        capital = self.__get_capital(year)
        interest = self.__get_interest()
        payment = self.__payment(capital, interest)

        self.state.current_mortgage -= capital
        self.state.month_payment = payment / 12
        self.state.payment = payment
        self.state.interest = interest
        self.state.capital = capital

        self.results.total_paid_capital += capital
        self.results.total_paid_interest += interest
        self.results.fixed_month_payment = self.__get_fixed_payment_monthly(year)


class Overpayment:
    def __init__(self, overpayments: Dict[int, Money] = {}) -> None:
        self.overpayments = overpayments

    def pay(self, year: int, mortgage: MortgagePayment):
        if not self.overpayments:
            return
        if year in self.overpayments:
            mortgage.state.overpayment = self.overpayments[year]
        else:
            mortgage.state.overpayment = 0
