from django.shortcuts import render


def home(request):
    return render(request, "website/home.html")


def features(request):
    return render(request, "website/features.html")


def about(request):
    return render(request, "website/about.html")


def contact(request):
    return render(request, "website/contact.html")
