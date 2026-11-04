WLASCICIEL = 'wlasciciel'


def jest_wlascicielem(user):
    return user.is_superuser or user.groups.filter(name=WLASCICIEL).exists()
