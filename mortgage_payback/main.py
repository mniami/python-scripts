from simulation import simulate, Params, Strategies
from i18n.i18n import set_locale

if __name__ == "__main__":
    set_locale("pl")
    simulate(
        Params(
            years=15,
            mortgage=200 * 1000,
            rate=0.03,
            capital_strategy=Strategies.get_capital_year_equal,
        )
    )
