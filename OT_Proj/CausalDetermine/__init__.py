from otree.api import *

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'CausalDetermine'
    players_per_group = None
    num_rounds = 3 # will add more



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    GivesConsent = models.BooleanField(widget=widgets.CheckboxInput(), label="I agree and wish to participate")
    CausalScore = models.StringField(widget=widgets.RadioSelectHorizontal, choices=['Not at all', 'Very Slightly', 'Slightly', 'Neutral', 'Moderately', 'Very much',
                                                                                     'Almost Entirely'])
    BonusScore = models.IntegerField(widget=widgets.RadioSelectHorizontal, choices=[-10, -1, 0, 1, 10], label="Reccomended bonus (%): ")
    Timeb1 = models.FloatField(blank=True, default=0.0)

# PAGES
class Consent(Page):
    form_model = 'player'
    form_fields = ['GivesConsent']
    def is_displayed(player):
        return player.round_number == 1     # only display in  first round

class Causality(Page):
    form_model = 'player'
    form_fields = ['CausalScore']

class Bonus(Page):
    form_model = 'player'
    form_fields = ['BonusScore']

class InfoBlocks(Page):
    form_model = 'player'
    form_fields = ['Timeb1']


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Consent, InfoBlocks, Causality, Bonus]
