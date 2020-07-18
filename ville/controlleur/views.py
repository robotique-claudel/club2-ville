from django.shortcuts import render


def controlleur(request):
    return render(request, "controlleur/sensor.html", {
        'sensor': '99',
    })
