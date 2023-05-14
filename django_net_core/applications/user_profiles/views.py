from django.shortcuts import render, HttpResponse


def main(request):
    return HttpResponse("<h1>Social Network</h1>")
