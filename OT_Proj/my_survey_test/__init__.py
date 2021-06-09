from otree.api import *

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'my_survey_test'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    name = models.StringField()
    age = models.IntegerField()
    pass


# PAGES
class MyPage(Page):
    form_model = 'player'
    form_fields = ['name', 'age']
    pass



class Results(Page):
    pass


page_sequence = [MyPage, Results]
