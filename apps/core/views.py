from django.shortcuts import render

def home(request):
    context = {
        'title': 'Hello Django',
        'username': 'admin',
        'items': ['Lab A', 'Lab B', 'Lab C']
    }

    return render(request, 'home.html', context)

def dashboard(request):
    return render(request, 'dashboard.html')