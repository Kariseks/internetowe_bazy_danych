from django.shortcuts import render

from . import services


def zaleglosc(request):
    return render(request, 'rozliczenia/zaleglosc.html', {'dane': services.zaleglosc_klienta(request.user)})
