from simulation import simulate, Params, Strategies
from i18n.i18n import set_locale

if __name__ == "__main__":
    set_locale("pl")
    params = Params(
        years=30,
        mortgage=414 * 1000,
        rate=0.065,
        capital_strategy=Strategies.get_capital_year_equal,
    )
    simulate(params)
    overpayments = {i: 30000 for i in range(0, 30)}
    simulate(params, overpayments)
