from simulation import simulate, Params, Strategies


if __name__ == "__main__":
    simulate(
        Params(
            years=15,
            mortgage=200 * 1000,
            rate=0.03,
            capital_strategy=Strategies.get_capital_year_growing,
        )
    )
