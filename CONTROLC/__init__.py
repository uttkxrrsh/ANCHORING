from otree.api import *
import random


doc = """
Your app description
"""




class C(BaseConstants):
    NAME_IN_URL = 'CONTROLC'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # a is a random value from uniform distribution 60, 150
    a = models.FloatField(initial= random.randint(60, 150))
    # b is random value from uniform distribution 0, 50
    b = models.FloatField(intial = random.randint(0, 50))
    # c is random value from uniform distribution 0, 75
    c = models.FloatField(initial= random.randint(0, 75))
    # d is random value from uniform distribution 0, 10
    d = models.FloatField(initial= random.randint(0, 10))
    # e is random value from uniform distribution -25, 25
    e = models.FloatField(initial= random.randint(-25, 25))

    guess = models.FloatField()


def set_payoffs(group: Group):
    player_lists = group.get_players()
    for p in player_lists:
        real_val = 2*p.a - p.b - 0.5*p.c + p.d*p.d + p.e
        p.payoff = max(0, 0.5 - 0.01*abs(p.guess - real_val))



def get_average_guess(group: Group):
    player_lists = group.get_players()
    average_guess = sum([p.guess for p in player_lists])/len(player_lists)
    return average_guess

# PAGES

class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    
class Calculate(Page):
    timeout_seconds = 30
    def vars_for_template(player: Player):

        player.a = random.randint(60, 150)
        player.b = random.randint(0, 50)
        player.c = random.randint(0, 75)
        player.d = random.randint(0, 10)
        player.e = random.randint(-25, 25)

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

class Results(Page):
    def vars_for_template(player: Player):
        group = player.group
        player_lists = group.get_players()
        average_guess = get_average_guess(group)
        real_val = player.a + player.b - player.c + player.d
        return {
            'average_guess': average_guess,
            'real_val': real_val,
        }

page_sequence = [Introduction, Calculate, ResultsWaitPage, Results]
