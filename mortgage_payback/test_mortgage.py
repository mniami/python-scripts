from simulation import Params, Strategies
from mortgage import MortgagePayment


def test_mortgage():
    params = Params(
        years=10,
        mortgage=10 * 1000,
        rate=0.01,
        capital_strategy=Strategies.get_capital_year_equal,
    )
    payment = MortgagePayment(params)
    payment.pay_off(1)

    assert payment.state.current_mortgage == 9000
    assert payment.state.month_payment == 91.66666666666667
    assert payment.results.total_paid_capital == 1000
    assert payment.results.total_paid_interest == 100.0
