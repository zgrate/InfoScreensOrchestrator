from django.contrib import admin
from django.contrib.admin import TabularInline
from django.contrib.admin.options import InlineModelAdmin

from screen.models import Screen, ScreenGroup, ScreenCommand, AutomaticScreenSwitcher, AutomaticCommand


# Register your models here.
# admin.site.register(ScreenCommand)
admin.site.register(AutomaticCommand)

class AutomaticCommandAdmin(TabularInline):
    model = AutomaticCommand


@admin.register(ScreenCommand)
class ScreenCommandAdmin(admin.ModelAdmin):
    list_filter = ('permit_background_audio',)
    list_display = ('command_name', 'base_command',)
    search_fields = ('command_name', 'base_command',)


@admin.register(AutomaticScreenSwitcher)
class AutomaticScreenSwitcherAdmin(admin.ModelAdmin):
    readonly_fields = ('last_switch',)
    list_filter = ('profile_name',)
    list_display = ('profile_name', 'last_switch', 'current_command')
    search_fields = ('profile_name',)
    inlines = (AutomaticCommandAdmin,)


@admin.register(Screen)
class ScreenAdmin(admin.ModelAdmin):
    list_filter = ('screen_group',)
    list_display = ('name', 'command', 'screen_group')
    readonly_fields = ('passphrase',)
    search_fields = ('name',)
    autocomplete_fields = ('overriden_current_command', 'screen_group')


@admin.register(ScreenGroup)
class ScreenGroupAdmin(admin.ModelAdmin):
    list_filter = ('disabled',)
    list_display = ('name', 'assigned_command', 'switching_mode', 'disabled')
    search_fields = ('name',)
    autocomplete_fields = ('assigned_command', 'switching_mode')
