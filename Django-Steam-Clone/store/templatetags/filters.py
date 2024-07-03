from django.template import Library

from utils import filters

register = Library()


@register.filter
def game_name_length_limit(game):
    return filters.game_name_length_limit(game)
