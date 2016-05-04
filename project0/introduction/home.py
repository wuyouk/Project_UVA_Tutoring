from django.shortcuts import render

def home_introduce(request):
    context = {'name': 'Johnson', 'ID': 'yw5g', 'class': 'Internet Scale Application'}
    return render(request, 'home.html', context)
