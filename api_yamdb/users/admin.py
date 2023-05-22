from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role'
    )
    search_fields = ('username',)
    list_editable = ('role',)
    list_display_links = ('username',)
    empty_value_display = '-пусто-'

    def __str__(self):
        return self.username[:15]
