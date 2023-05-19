from datetime import datetime

from applications.user_profiles import models


def update_first_login_record(user: models.CustomUser) -> None:
    if not user.first_login:
        user.first_login = datetime.today()
        user.save()
