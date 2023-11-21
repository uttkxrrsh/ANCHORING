from otree.api import *
import random


doc = """
Your app description
"""




class C(BaseConstants):
    NAME_IN_URL = 'CONTROLB'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # a is random value from uniform distribution 50 , 150
    a = models.FloatField(initial= random.randint(50, 150))
    # b is random value from uniform distribution 51, 150
    b = models.FloatField(intial = random.randint(51, 150))
    # c is random value from uniform distribution 0, 75
    c = models.FloatField(initial= random.randint(0, 75))
    # d is random value from uniform distribution -25, 25
    d = models.FloatField(initial= random.randint(-25, 25))

    guess = models.FloatField(intial = 0)


def set_payoffs(group: Group):
    player_lists = group.get_players()
    for p in player_lists:
        real_val = p.a + p.b - p.c + p.d
        p.payoff = max(0, 50 - abs(p.guess - real_val))


# PAGES

class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    
class Calculate(Page):
    timeout_seconds = 60
    def vars_for_template(player: Player):
        player.a = random.randint(50, 150)
        # b is random value from uniform distribution 51, 150
        player.b = random.randint(51, 150)
        # c is random value from uniform distribution 0, 75
        player.c = random.randint(0, 75)
        # d is random value from uniform distribution -25, 25
        player.d = random.randint(-25, 25)
        return {
            'A': player.a,
            'B': player.b,
            'C': player.c,
            'D': player.d,
        }
    form_model = 'player'
    form_fields = ['guess']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


page_sequence = [Introduction, Calculate, ResultsWaitPage]
