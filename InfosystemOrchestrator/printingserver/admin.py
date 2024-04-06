from gettext import ngettext

from django.contrib import admin, messages
from django.utils import timezone

from printingserver.models import StoredDocument

# Register your models here.

@admin.register(StoredDocument)
class StoredDocumentAdmin(admin.ModelAdmin):
    list_filter = ('printed_at', )
    list_display = ('description', 'user', 'priority', 'is_printed')
    search_fields = ('priority',)
    actions = ('mark_as_printed', 'mark_as_unprinted')
    ordering = ('-priority', 'created', )
    readonly_fields = ('printed_at', )

    def mark_as_printed(self, request, queryset):
        if queryset.filter(printed_at__isnull=False).exists():
            self.message_user(
                request,
                "Some documents are already marked as printed",
                messages.ERROR,
            )
        else:
            updated = queryset.update(printed_at=timezone.now())
            self.message_user(
                request,
                ngettext(
                    "%d document was successfully marked as printed.",
                    "%d documents were successfully marked as not printed.",
                    updated,
                )
                % updated,
                messages.SUCCESS,
            )

    def mark_as_unprinted(self, request, queryset):
        if queryset.filter(printed_at__isnull=True).exists():
            self.message_user(
                request,
                "Some documents are already marked as not printed",
                messages.ERROR,
            )
        else:
            updated = queryset.update(printed_at=None)
            self.message_user(
                request,
                ngettext(
                    "%d document was successfully marked as printed.",
                    "%d documents were successfully marked as not printed.",
                    updated,
                )
                % updated,
                messages.SUCCESS,
            )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        print(request.path)
        if request.path == "/admin/printingserver/storeddocument/" and 'printed_at__isnull' not in request.GET and 'printed_at__gte' not in request.GET and 'printed_at__lte' not in request.GET:
            qs = qs.filter(printed_at__isnull=True)
        return qs

