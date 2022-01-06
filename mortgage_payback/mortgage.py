from dataclasses import dataclass
from utils import Money, Utils
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
        return capital

    def __get_interest(self) -> Money:
        return self.params.rate * self.state.current_mortgage

    @staticmethod
    def __payment(capital: float, interest: float) -> Money:
        return interest + capital

    def pay_off(self, year: int):
        capital = self.__get_capital(year)
        interest = self.__get_interest()
        payment = self.__payment(capital, interest)

        self.state.current_mortgage -= capital
        self.state.month_payment = payment / 12
        self.state.year_payment = payment
        self.results.total_paid_capital += capital
        self.results.total_paid_interest += interest
