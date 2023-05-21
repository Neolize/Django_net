from datetime import date


def get_range_of_years():
    """Return range of years for birthday field in signup form"""
    current_year = date.today().year
    initial_year = current_year - 130
    return [year for year in range(initial_year, current_year + 1)]


def get_current_date():
    return date.today()
