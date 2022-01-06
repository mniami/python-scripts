from utils import Money


class Strategies:
    @staticmethod
    def get_capital_year_growing(
        year: int, total_years: int, total_capital: Money
    ) -> Money:
        """Stable capital growing installment
        f(x) = 2 / years * x * (total/years) = y
        """
        return (2 / total_years) * year * (total_capital / total_years)

    @staticmethod
    def get_capital_year_equal(
        year: int, total_years: int, total_capital: Money
    ) -> Money:
        """Equal capital installment"""
        return total_capital / total_years
