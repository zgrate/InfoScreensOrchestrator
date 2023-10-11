from django.db.models import F, ExpressionWrapper, DurationField, Count
from django.utils import timezone
from workers import task

from screen.models import AutomaticScreenSwitcher

@task(schedule=10)
def screen_automatic_runner():
    qs = AutomaticScreenSwitcher.objects.annotate(next_execution=(F('last_switch') + ExpressionWrapper(F('change_time_seconds')*1000000, output_field=DurationField()))).filter(next_execution__lte=timezone.now(), switching_screens_group__isnull=False).annotate(count_systems=Count('automatic_commands')).prefetch_related('automatic_commands')
    ele: AutomaticScreenSwitcher
    for (ele) in qs.iterator():
        if ele.current_command:
            curr = ele.current_command.number_order + 1
            if curr >= ele.count_systems:
                curr = 0

            ele.current_command = ele.automatic_commands.get(number_order=curr)
        else:
            ele.current_command = ele.automatic_commands.get(number_order=0)

        ele.last_switch = timezone.now()
        ele.save(update_fields=['current_command', 'last_switch'])


