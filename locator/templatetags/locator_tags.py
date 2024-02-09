from django import template

from locator.models import (DistributiveSubstation as DS,
                            MotorControlCenter as MCC)

register = template.Library()


@register.inclusion_tag('locator/room_list.html')
def show_substations():
    return {'rooms': DS.objects.all(),}
