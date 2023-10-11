from django.contrib import admin

from screen.models import Screen, ScreenGroup, ScreenCommand, AutomaticScreenSwitcher, AutomaticCommand

# Register your models here.
admin.site.register(Screen)
admin.site.register(ScreenGroup)
admin.site.register(AutomaticScreenSwitcher)
admin.site.register(AutomaticCommand)
admin.site.register(ScreenCommand)
