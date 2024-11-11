from django.shortcuts import render


def home_view(request):
    return render(request, 'common/home-view.html')
