# -*- coding: utf-8 -*-


from django import template
import gguru.gg_json

register = template.Library()


# Преобразовывает питон-переменную к JSON
def gg_json_filter(value):
    return gguru.gg_json.ggJsonDumps(value, gguru.gg_json.makeJSONDjangoEncoder())

register.filter('gg_json_filter', gg_json_filter)
