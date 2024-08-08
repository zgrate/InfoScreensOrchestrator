import datetime
import random

from django.db.models import F, ExpressionWrapper, DurationField, Count
from django.utils import timezone
from workers import task

from screen.models import AutomaticScreenSwitcher

@task(schedule=10)
def screen_automatic_runner():
    print("Screen runner")

    qs = AutomaticScreenSwitcher.objects.prefetch_related('automatic_commands')

    # qs = (AutomaticScreenSwitcher.objects.annotate(next_execution=(
    #             F('last_switch') + ExpressionWrapper(F('change_time_seconds') * 1000000,
    #                                                  output_field=DurationField())))
    #     .filter(
    #     next_execution__lte=timezone.now(), switching_screens_group__isnull=False).annotate(
    #     count_systems=Count('automatic_commands')).prefetch_related('automatic_commands'))
    ele: AutomaticScreenSwitcher
    for ele in qs.iterator():
        next_execution_time = ele.last_switch + datetime.timedelta(seconds=ele.change_time_seconds)
        count_system = ele.automatic_commands.count()

        print("Switching screen", ele.profile_name)

        if next_execution_time > timezone.now() and ele.switching_screens_group is not None:
            if ele.randomise:
                if ele.current_command:
                    ele.current_command = random.choice(list(ele.automatic_commands.exclude(pk=ele.current_command)))
                else:
                    ele.current_command = random.choice(list(ele.automatic_commands))

            if ele.current_command:
                next_obj = ele.automatic_commands.filter(created__gt=ele.current_command.created).order_by('created').first()

                if next_obj is None:
                    ele.current_command = ele.automatic_commands.order_by('created').first()
                else:
                    ele.current_command = next_obj
            else:
                ele.current_command = ele.automatic_commands.order_by('created').first()

            ele.last_switch = timezone.now()
            ele.save(update_fields=['current_command', 'last_switch'])
