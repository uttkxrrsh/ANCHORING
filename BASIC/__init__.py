from otree.api import *
import random


doc = """
Your app description
"""




class C(BaseConstants):
    NAME_IN_URL = 'BASIC'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 2
    GUESS_MAX = 325


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

    guess = models.FloatField(min = 0, max = C.GUESS_MAX, initial = 0, label = "What is your guess?")

        # fields should be higher or lower true:higher and false:lower
    higher = models.BooleanField(
        choices=[
            [True, 'Higher'],
            [False, 'Lower']
        ],
        widget=widgets.RadioSelect,
        label = "What will be the value be in next round compared to current average?"
    )


def set_payoffs(group: Group):
    player_lists = group.get_players()
    for p in player_lists:
        real_val = p.a + p.b - p.c + p.d
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
    form_model = 'player'
    form_fields = ['higher']



page_sequence = [Introduction, Calculate, ResultsWaitPage, Results]
