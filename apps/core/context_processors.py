def sidebar_menu(request):
    return {
        'sidebar_menu': [
            {
                'name': 'Companies',
                'icon': 'building-2',
                'bg_color': 'bg-sky-500/25',
                'url': '#',
                'active': True,
            },
            {
                'name': 'People',
                'icon': 'users',
                'bg_color': 'bg-violet-500/25',
                'url': '#',
                'active': False,
            },
            {
                'name': 'Tasks',
                'icon': 'check-square',
                'bg_color': 'bg-emerald-500/25',
                'url': '#',
                'active': False,
            },
            {
                'name': 'Notes',
                'icon': 'file-text',
                'bg_color': 'bg-amber-500/25',
                'url': '#',
                'active': False,
            },
        ]
    }
