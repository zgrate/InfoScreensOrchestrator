from django.db.models import Q

from helpermonitor.models import HelperDutyTimeModel


def check_collisions(duty: HelperDutyTimeModel):
    qs = (HelperDutyTimeModel.objects.filter(helper=duty.helper)
          .filter(
            Q(duty_start__lte=duty.duty_start, duty_end__gte=duty.duty_start) | Q(duty_start__lte=duty.duty_end, duty_end__gte=duty.duty_end)
            ).exclude(id=duty.id)
    )
    return qs.all()

