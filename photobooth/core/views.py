from django.shortcuts import render


def index(request):
    return render(request, "index.html")

def snap(request):
    return render(request, "snap.html")

def location(request):
    return render(request, "location.html")

def result(request):
    return render(request, "result.html")