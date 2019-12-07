from django.shortcuts import render


def create_view(request):
    return render(request, 'autoria/create.html')
