from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
import random


class Introduction(Page):
    timeout_seconds = 180

    def before_next_page(self):
        ########
        # 1. code for balanced groups
        ########

        # create a list for all the treatments assigned for all the previous players
        treatment_so_far = []
        for p in self.subsession.get_players():  # for all players
            treatment_so_far.append(p.treatment)  # the list "treatment_so_far" only contains existing treatments, i.e.: treatments assigned to each "previous player"

        # Count how often each treatment has been run
        treatment_n = {}
        # Here we call the "treatment" list we wrote in Constants
        for t in Constants.treatment:
            treatment_n[t] = treatment_so_far.count(t)

        # Create a new array containing the treatments that have been run the least amount of times
        treatments = []
        for c, n in treatment_n.items():
            if n == min(treatment_n.values()):
                treatments.append(c)

        # Randomly assign the participant to one of these treatments
        temp = random.choice(treatments)
        self.player.treatment = temp
        # create a participant var because we will use this var in different rounds
        # only the participant.vars and session.vars can be passed through different rounds
        self.participant.vars['treatment'] = self.player.treatment

        ########
        # done 1
        ########

        ########
        # 2. code for randomizing the 16 questions
        ########

        randomized_sample = self.participant.vars[self.player.treatment]
        self.participant.vars['questions'] = random.sample(randomized_sample, len(randomized_sample))

        ########
        # done 2
        ########

        ########
        # 3. code for reading the first line of one specific csv file
        ########

        question_data = self.participant.vars['questions'][self.round_number - 1]  # we need to minus 1 because python counts it from 0, not from 1, but round_number starts from 1
        self.participant.vars['question'] = question_data['Question']
        self.participant.vars['x1'] = question_data['x1']
        self.participant.vars['x2'] = question_data['x2']
        self.participant.vars['t1'] = question_data['t1']
        self.participant.vars['t2'] = question_data['t2']
        self.participant.vars['endowment'] = question_data['Endowment']
        self.participant.vars['d1'] = question_data['d1']
        self.participant.vars['d2'] = question_data['d2']

        ########
        # done 3
        ########

    def is_displayed(self):
        return self.round_number == 1

class Decision(Page):
    form_model = models.Player
    form_fields = ['cooperate']

    def before_next_page(self):  #any code is gona be executed before you go to next page
        self.player.set_payoff()
        self.player.set_time()
        self.player.question = self.participant.vars['question']

        if self.round_number != 16:
            # prepare data for the next round
            question_data = self.participant.vars['questions'][self.round_number]
            self.participant.vars['question'] = question_data['Question']
            self.participant.vars['x1'] = question_data['x1']
            self.participant.vars['x2'] = question_data['x2']
            self.participant.vars['t1'] = question_data['t1']
            self.participant.vars['t2'] = question_data['t2']
            self.participant.vars['endowment'] = question_data['Endowment']
            self.participant.vars['d1'] = question_data['d1']
            self.participant.vars['d2'] = question_data['d2']

        self.participant.vars['payoff_%s' % self.round_number] = self.player.payoff
        self.participant.vars['time_%s' % self.round_number] = self.player.time

    def vars_for_template(self):
        # this function can pass the value to html
        # for each round, x1, x2, t1, t2 etc. are different, this func will modified the html according to the values you put here
        return {
            'x1': str(abs(int(self.participant.vars['x1']))),
            'x2': str(abs(int(self.participant.vars['x2']))),
            't1':  self.participant.vars['t1'],
            't2':  self.participant.vars['t2'],
            'endowment': self.participant.vars['endowment'],
            'treatment': self.participant.vars['treatment'],
            "round": self.round_number #########
        }

class MyPage(Page):
    form_model = models.Player
    form_fields = ["gender","age","is_student","level","income","email"]

    def before_next_page(self): #any code is gona be executed before you go to next page
        self.participant.vars["is_student"]=self.player.is_student #we safe this on the participant :)

    def is_displayed(self):
        return self.round_number == 16

class ResultsSummary(Page):

    def vars_for_template(self):

        payoff = []
        time = []
        round = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
        for i in range (1,17):

            payoff.append(self.participant.vars['payoff_%s' %i])
            time.append(self.participant.vars['time_%s' % i])
        lst = zip(payoff, time, round)

        return {
            'lst': lst,
            'treatment': self.participant.vars['treatment']
        }
    def is_displayed(self):
        return self.round_number == 16

page_sequence = [
    Introduction,
    Decision,
    MyPage,
    ResultsSummary
]
