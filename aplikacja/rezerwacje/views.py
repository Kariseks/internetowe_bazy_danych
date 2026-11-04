from django.shortcuts import render


def katalog(request):
    return render(request, 'rezerwacje/katalog.html')
