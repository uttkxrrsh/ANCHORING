from otree.api import *
import random
import numpy as np

doc = """
Your app description
"""

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


class C(BaseConstants):
    NAME_IN_URL = 'BASIC'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 4
    GUESS_MAX = 325


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    # a is random value from uniform distribution 50 , 150
    a = models.FloatField(initial= normal_random_integer_within_range(50, 150))
    # b is random value from uniform distribution 51, 150
    b = models.FloatField(initial = normal_random_integer_within_range(51, 150))
    # c is random value from uniform distribution 0, 75
    c = models.FloatField(initial= normal_random_integer_within_range(0, 75))
    # d is random value from uniform distribution -25, 25
    d = models.FloatField(initial= normal_random_integer_within_range(-25, 25))

    guess = models.FloatField(min = 0, max = C.GUESS_MAX, label = "What is your guess?")

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
        p.payoff = max(0, 50 - abs(p.guess - real_val))

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
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number != C.NUM_ROUNDS
    
    def vars_for_template(player: Player):
        group = player.group
        average_guess = get_average_guess(group)
        real_val = player.a + player.b - player.c + player.d
        return {
            'average_guess': average_guess,
            'real_val': real_val,
        }
        

    form_model = 'player'
    form_fields = ['higher']

class ResultsE(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    
    def vars_for_template(player: Player):
        group = player.group
        # player_lists = group.get_players()
        average_guess = get_average_guess(group)
        real_val = player.a + player.b - player.c + player.d
        return {
            'average_guess': average_guess,
            'real_val': real_val,
        }

class AwaitPage(WaitPage):
        def vars_for_template(player: Player):
            group = player.group
            player_lists = group.get_players()
            A = normal_random_integer_within_range(50, 150)
            B = normal_random_integer_within_range(51, 150)
            C = normal_random_integer_within_range(0, 75)
            for p in player_lists:
                p.a = A
                p.b = B
                p.c = C
                p.d = normal_random_integer_within_range(-25, 25)


page_sequence = [Introduction, AwaitPage, Calculate, ResultsWaitPage, Results, ResultsE]
