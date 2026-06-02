def sidebar_menu(request):
    current_path = request.path
    return {
        'sidebar_menu': [
            {
                'name': 'Companies',
                'icon': 'building-2',
                'bg_color': 'bg-sky-500/25',
                'url': '/',
                'active': current_path == '/',
            },
            {
                'name': 'People',
                'icon': 'users',
                'bg_color': 'bg-violet-500/25',
                'url': '/people/',
                'active': current_path.startswith('/people/'),
            },
            {
                'name': 'Tasks',
                'icon': 'check-square',
                'bg_color': 'bg-emerald-500/25',
                'url': '#',
                'active': current_path.startswith('/tasks/'),
            },
            {
                'name': 'Notes',
                'icon': 'file-text',
                'bg_color': 'bg-amber-500/25',
                'url': '#',
                'active': current_path.startswith('/notes/'),
            },
        ]
    }

