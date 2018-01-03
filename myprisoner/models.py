from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random
import csv


doc = """
This is a one-shot "Prisoner's Dilemma". Two players are asked separately
whether they want to cooperate or defect. Their choices directly determine the
payoffs.
"""


class Constants(BaseConstants):
    name_in_url = 'myprisoner'
    players_per_group = None
    num_rounds = 16

    instructions_template = 'myprisoner/Instructions.html'

    # read in 4 csv files
    with open("myprisoner/AG.csv") as f:
        AG = list(csv.DictReader(f))

    with open("myprisoner/AL.csv") as f:
        AL = list(csv.DictReader(f))

    with open("myprisoner/SG.csv") as f:
        SG = list(csv.DictReader(f))

    with open("myprisoner/SL.csv") as f:
        SL = list(csv.DictReader(f))

    # define a treatment list, which is used to make balanced groups
    treatment = ['AG', 'AL', 'SG', 'SL']


class Subsession(BaseSubsession):
    def before_session_starts(self):
        if self.round_number == 1:
#            self.paying_round = random.randint(1, Constants.num_rounds)
#            self.session.vars['paying_round'] = self.paying_round

            # for each player
            for p in self.get_players():
                # in order to match the "treatment" read from csv files with the treatment we assigned to each player
                p.participant.vars['AG'] = Constants.AG
                p.participant.vars['AL'] = Constants.AL
                p.participant.vars['SG'] = Constants.SG
                p.participant.vars['SL'] = Constants.SL

                # just to get rid of the "KeyError"
                p.participant.vars['questions'] = Constants.SL  # arbitrarily choose one as a starting value, which will be modified in the views.py
                p.participant.vars['treatment'] = 'AL'  # arbitrarily choose one as a starting value, which will be modified in the views.py


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    treatment = models.CharField()
    question = models.IntegerField()

    cooperate = models.BooleanField(
        choices=[
            [False, 'Defect'],
            [True, 'Cooperate']
        ]
    )

    time = models.CharField()

    def decision_label(self):
        if self.cooperate:
            return 'cooperate'
        return 'defect'

    def set_payoff(self):
        payoff_matrix = {
            True:
                {
                    True: self.participant.vars['d1'],# .both_cooperate_payoff
                    False: self.participant.vars['d1']  # DOES NOT EXIST
                },
            False:
                {
                    True: self.participant.vars['d2'],  # betray_payoff,
                    False: self.participant.vars['d1']  # DOES NOT EXIST
                }
        }
        self.payoff = payoff_matrix[self.cooperate][True]  # [self.other_player().cooperate]

    def set_time(self):
        time_matrix = {
            True:
                {
                    True: self.participant.vars['t1'],  # .both_cooperate_payoff,
                    False: self.participant.vars['d1']  # DOES NOT EXIST
                },
            False:
                {
                    True: self.participant.vars['t2'],  # betray_payoff,
                    False: self.participant.vars['d1']  # DOES NOT EXIST
                }
        }
        self.time = time_matrix[self.cooperate][True]  # [self.other_player().cooperate]
    gender = models.PositiveIntegerField(
        choices=[
            [0, 'Female'],
            [1, 'Male'],
        ]
    )  # Will ask yes or no (Boolean) {horizontaly}
    age = models.IntegerField(min=1900,max=2000) #Is an integer free value
    is_student = models.BooleanField()
    email = models.CharField()
    level = models.PositiveIntegerField(
        choices=[
            [0, 'Bac'],
            [1, 'classe préparatoire'],
            [2, 'L 1'],
            [3, 'L 2'],
            [4, 'L 3'],
            [5, 'M 1'],
            [6, 'M 2'],
            [7, 'PhD'],
        ]
    )
    income = models.PositiveIntegerField(
        choices=[
            [1, '<1,200€'],
            [2, '1,201€ to 1,800€'],
            [3, '1,800€ to 2,500€'],
            [4, '2,501€ to 3,500€'],
            [5, '>3,500€'],

        ]
    )