from datetime import date


def get_min_birthdate() -> str:
    """Return min possible birthdate for user's birthday field"""
    min_year = date.today().year - 130
    return str(date(year=min_year, month=1, day=1))


def get_max_birthdate() -> str:
    """Return max possible birthdate for user's birthday field"""
    return str(date.today())


def form_user_data_for_profile_view(user_data: dict) -> dict:
    """Return dict with formatted user's data"""
    full_name = f'{user_data.pop("first_name")} {user_data.pop("middle_name")} {user_data.pop("last_name")}'

    user_data['full_name'] = full_name.strip() or user_data.get('username')
    user_data['birthday'] = user_data.get('birthday') or ''
    user_data['phone'] = user_data.get('phone') or ''
    user_data['address'] = user_data.get('address') or ''
    return user_data
