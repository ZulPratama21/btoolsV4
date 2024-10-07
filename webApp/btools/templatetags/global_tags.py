from django import template

register = template.Library()

@register.filter(name='in_groups')
def in_groups(user, group_names):
    # Mengonversi string group_names menjadi daftar grup
    group_names_list = [name.strip() for name in group_names.split(',')]
    
    # Memeriksa apakah user berada di salah satu grup
    return user.groups.filter(name__in=group_names_list).exists()
