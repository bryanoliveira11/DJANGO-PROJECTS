from django.utils.text import Truncator


def game_name_length_limit(game: str):
    if not len(game) > 25:
        return game
    return str(Truncator(game).chars(25))
