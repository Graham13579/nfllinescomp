from django.contrib import admin
from groups.models import Group,Player,PlayerPick,Game

# Register your models here.
admin.site.register(Group)
admin.site.register(Player)

class PlayerPickAdmin(admin.ModelAdmin):
    readonly_fields=('timemade',)
admin.site.register(PlayerPick,PlayerPickAdmin)

admin.site.register(Game)