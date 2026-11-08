"""Operator płatności: rejestracja karty w testowym środowisku Stripe (wersja rozszerzona, p. 2.5 sprawozdania).

Klient wpisuje kartę na stronie Stripe Checkout (tryb zapisu karty, bez płatności). Stripe pyta przy tym o zgodę
na przyszłe obciążenia i w razie potrzeby o 3-D Secure, a system dostaje tylko identyfikator karty (pm_...).
Kartę zapisuje się przy kliencie operatora (cus_...), więc właściciel może ją później obciążyć bez udziału klienta.
Bez klucza STRIPE_SECRET_KEY widok karta używa symulacji.
"""
import logging

import stripe
from django.conf import settings

log = logging.getLogger(__name__)


class OperatorNiedostepny(Exception):
    """Operator nie odpowiada albo odrzucił żądanie. Widok wyświetla komunikat."""


def wlaczony():
    return bool(settings.STRIPE_SECRET_KEY)


def testowy():
    return settings.STRIPE_SECRET_KEY.startswith('sk_test_')


def _stripe():
    return stripe.StripeClient(
        settings.STRIPE_SECRET_KEY,
        http_client=stripe.new_default_http_client(timeout=10),
        max_network_retries=1,
    )


def _klient_operatora(karta):
    """Klient operatora, do którego należy dotychczasowa karta, albo None (brak karty, karta z symulacji)."""
    if not karta or not karta.startswith('pm_'):
        return None
    try:
        return _stripe().v1.payment_methods.retrieve(karta).customer
    except stripe.StripeError:
        log.warning('Nie odczytano karty %s u operatora', karta, exc_info=True)
        return None


def rozpocznij(konto_id, email, poprzednia_karta, adres_powrotu):
    """PU13 krok 3. Sesja Stripe Checkout w trybie zapisu karty. Zwraca (identyfikator sesji, adres strony operatora).

    Nowa karta trafia do tego samego klienta operatora co poprzednia; przy pierwszej karcie klienta operatora
    tworzy Stripe, dopiero gdy karta zostanie zapisana. Rzuca OperatorNiedostepny.
    """
    parametry = {
        'mode': 'setup',
        'currency': 'pln',
        'locale': 'pl',
        'client_reference_id': str(konto_id),
        # Metody płatności włącza się w ustawieniach konta Stripe; BLIK i Klarna nie są kartami.
        'excluded_payment_method_types': ['blik', 'klarna'],
        'success_url': adres_powrotu + '?sesja={CHECKOUT_SESSION_ID}',
        'cancel_url': adres_powrotu + '?przerwano=1',
    }
    klient = _klient_operatora(poprzednia_karta)
    if klient:
        parametry['customer'] = klient
    else:
        parametry.update(customer_creation='always', customer_email=email)
    try:
        sesja = _stripe().v1.checkout.sessions.create(parametry)
    except stripe.StripeError as blad:
        log.exception('Operator nie utworzył sesji rejestracji karty dla konta %s', konto_id)
        raise OperatorNiedostepny from blad
    return sesja.id, sesja.url


def zapisana_karta(sesja_id, konto_id):
    """PU13 krok 5. Identyfikator karty zapisanej w sesji albo None, gdy sesja nie należy do konta lub karty nie zapisano.

    Wynik sprawdza się u operatora, a nie na podstawie adresu powrotu. Rzuca OperatorNiedostepny.
    """
    try:
        sesja = _stripe().v1.checkout.sessions.retrieve(sesja_id, {'expand': ['setup_intent.payment_method']})
    except stripe.InvalidRequestError:
        log.warning('Nieznana sesja rejestracji karty %s', sesja_id)
        return None
    except stripe.StripeError as blad:
        log.exception('Operator nie potwierdził sesji %s', sesja_id)
        raise OperatorNiedostepny from blad
    intencja = sesja.setup_intent
    if (sesja.client_reference_id != str(konto_id) or sesja.status != 'complete'
            or intencja is None or intencja.status != 'succeeded'):
        return None
    # Link (portfel Stripe) zapisuje kartę pod własnym typem.
    if intencja.payment_method.type not in ('card', 'link'):
        return None
    return intencja.payment_method.id


def odlacz(karta):
    """PU13 krok 5. Odłącza poprzednią kartę u operatora, żeby właściciel nie obciążył jej przez pomyłkę."""
    if not karta or not karta.startswith('pm_'):
        return
    try:
        _stripe().v1.payment_methods.detach(karta)
    except stripe.StripeError:
        log.exception('Nie odłączono poprzedniej karty %s', karta)
