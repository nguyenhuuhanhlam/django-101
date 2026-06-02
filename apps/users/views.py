from django.shortcuts import render
from django.contrib.auth import get_user_model

User = get_user_model()

def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    context = {
        'users': users,
        'header_title': 'People',
        'header_icon': 'users',
        'header_button': '+ New Person',
    }
    return render(request, 'users/user_list.html', context)

