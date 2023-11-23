from otree.api import *
import random
import numpy as np


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

def normal_random_integer_within_range(min_value, max_value):
    # Calculate the mean of the range
    mean_value = (min_value + max_value) / 2

    # Calculate the standard deviation based on the range
    std_deviation = (max_value - min_value) / 4  # You can adjust the factor as needed

    # Generate a random variable from a normal distribution
    random_variable = np.random.normal(loc=mean_value, scale=std_deviation)

    # Ensure the random variable is within the specified range
    random_variable = max(min(random_variable, max_value), min_value)

    # Round the result to the nearest integer
    random_variable = round(random_variable)

    return random_variable

class Player(BasePlayer):
    # a is a random value from uniform distribution 60, 150
    a = models.FloatField(initial= random.randint(60, 150))
    # b is random value from uniform distribution 0, 50
    b = models.FloatField(initial = random.randint(0, 50))
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
        p.payoff = max(0, 50 - abs(p.guess - real_val))


# PAGES

class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    
class Calculate(Page):
    timeout_seconds = 30
    def vars_for_template(player: Player):
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
