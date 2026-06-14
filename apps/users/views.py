import json

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import UserCreateForm, UserUpdateForm

User = get_user_model()

# Avatar colour palette — rotates by user.id % 6
_AVATAR_COLORS = [
    'bg-violet-600',
    'bg-sky-600',
    'bg-emerald-600',
    'bg-amber-600',
    'bg-rose-600',
    'bg-indigo-600',
]


def serialize_user(user):
    """Return a JSON-serialisable dict for a User instance."""
    return {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name or '-',
        'last_name': user.last_name or '-',
        'email': user.email or '',
        'is_active': user.is_active,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
        'date_joined': user.date_joined.strftime('%b %d, %Y %H:%M'),
        'last_login': (
            user.last_login.strftime('%b %d, %Y %H:%M') if user.last_login else '-'
        ),
        'initial': (user.username[0].upper() if user.username else '?'),
        'avatar_class': _AVATAR_COLORS[user.id % len(_AVATAR_COLORS)],
        'name': (f"{user.first_name} {user.last_name}".strip() or user.username),
        'status': 'Active' if user.is_active else 'Inactive',
    }


# ─────────────────────────────────────────────
# List
# ─────────────────────────────────────────────

def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    users_json = json.dumps([serialize_user(u) for u in users])
    context = {
        'users_json': users_json,
        'header_title': 'People',
        'header_icon': 'users',
        'header_button': '+ New Person',
    }
    return render(request, 'users/user_list.html', context)


# ─────────────────────────────────────────────
# Create
# ─────────────────────────────────────────────

@require_POST
def user_create(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {'success': False, 'errors': {'__all__': ['Invalid request body.']}},
            status=400,
        )
    form = UserCreateForm(data)
    if form.is_valid():
        user = form.save()
        return JsonResponse({'success': True, 'user': serialize_user(user)})
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)


# ─────────────────────────────────────────────
# Update
# ─────────────────────────────────────────────

@require_POST
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {'success': False, 'errors': {'__all__': ['Invalid request body.']}},
            status=400,
        )
    form = UserUpdateForm(data, instance=user)
    if form.is_valid():
        user = form.save()
        return JsonResponse({'success': True, 'user': serialize_user(user)})
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)


# ─────────────────────────────────────────────
# Delete
# ─────────────────────────────────────────────

@require_POST
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_id = user.id
    user.delete()
    return JsonResponse({'success': True, 'id': user_id})


# ─────────────────────────────────────────────
# Bulk delete
# ─────────────────────────────────────────────

@require_POST
def user_bulk_delete(request):
    try:
        data = json.loads(request.body)
        ids = [int(i) for i in data.get('ids', [])]
    except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
        return JsonResponse(
            {'success': False, 'error': 'Invalid request body.'}, status=400
        )
    User.objects.filter(id__in=ids).delete()
    return JsonResponse({'success': True, 'deleted_ids': ids})


# ─────────────────────────────────────────────
# Toggle active status
# ─────────────────────────────────────────────

@require_POST
def user_toggle_active(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.is_active = not user.is_active
    user.save(update_fields=['is_active'])
    return JsonResponse({'success': True, 'user': serialize_user(user)})
