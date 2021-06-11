from otree.api import *


doc = """
Causal Determination Mouse-tracking experiment
"""

class Constants(BaseConstants):
    name_in_url = 'CausalDetermine'
    players_per_group = None
    num_rounds = 32


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    GivesConsent = models.BooleanField(widget=widgets.CheckboxInput(), label="Agree")
    CausalScore = models.StringField(widget=widgets.RadioSelectHorizontal, choices=['Not at all', 'Very Slightly', 'Slightly', 'Neutral', 'Moderately', 'Very much',
                                                                                     'Almost Entirely'], label="Causal Attribution: ")
    BonusScore = models.IntegerField(widget=widgets.RadioSelectHorizontal, choices=[[-10,'-10%'], [-1,'-1%'], [0,'0%'], [1,'1%'], [10,'10%']], label="Bonus Attribution: ")
    Timeb1 = models.FloatField(blank=True, default=0.0)
    Timeb2 = models.FloatField(blank=True, default=0.0)
    Timeb3 = models.FloatField(blank=True, default=0.0)
    Timeb4 = models.FloatField(blank=True, default=0.0)
    Timeb5 = models.FloatField(blank=True, default=0.0)
    Timeb6 = models.FloatField(blank=True, default=0.0)
    Timeb7 = models.FloatField(blank=True, default=0.0)

    InfoOrderGroup = models.StringField()
    Participant_order = models.IntegerField()

    Agent = models.StringField()
    Outcome1 = models.StringField()
    Outcome2 = models.StringField()
    Action = models.StringField()
    Incentive = models.StringField()
    Pivotality = models.StringField()
    Context = models.StringField()
    Dummy1 = models.StringField()

    Numeracy_Answer = models.IntegerField(label="Answer (%): ")
    Age = models.IntegerField(label="What is your age?: ")
    Nationality = models.StringField(label="What is your nationality?: ")
    Education = models.StringField(choices=["0) None", "1) Highschool", "2) College Diploma", "3) Bachelors Degree", "4) Postgraduate Diploma/Honours Degree", "5) Master's Degree", "6) PhD or Higher"], label="Which of the following best describes the highest level of education you have completed? ")
    Employment = models.StringField(choices=["Unemployed", "Apprentice/Trainee", "Full-time student", "Employed part-time", "Employed full-time", "Self-Employed"], label="Which of the following best describes your current employment situation? ")
    Email_Address = models.StringField(blank=True, label="Email Address")
    KeepPosted = models.BooleanField(widget=widgets.CheckboxInput(), label="I would like to receive a copy of the working paper when it becomes available", blank=True)

# Functions

def response_outcome(player: Player):
    if player.Context == "Business":
        OutcomeResponseTxt = "the company's environmental footprint to " + player.Outcome2
    elif player.Context == "Football":
        OutcomeResponseTxt = "their team to " + player.Outcome2
    return OutcomeResponseTxt


def context_description(player: Player):
    if player.Context == "Football":
        Context_Descr = "In the Football scenario, the agent can either choose to shoot to attempt to score a goal, or can pass the ball to allow another teammate to shoot. This can result in either a goal being scored or not, which ultimately leads to the final outcome of whether or not the team loses. For the sake of this experiment, assume that you support the team for which the agent is playing. "
    elif player.Context == "Business":
        Context_Descr = "In the Business scenario, the agent chooses between adopting a new policy or staying with the same policy. Based on this decision, the company will see a change in their profits, as well as in their environmental footprint. The environmental impact is the ‘end outcome’ for which you will indicate the causal responsibility attributed to the agent. "
    return Context_Descr

def creating_session(subsession):
    import itertools
    FieldOrders = itertools.cycle(["A", "B", "C"])
    PartOrders = itertools.cycle(range(1,61))
    TempDummy = itertools.cycle(["A", "B"])  # Dummy variable doesn't need to be perfectly balanced

    if subsession.round_number == 1:
        for player in subsession.get_players():
            player.participant.vars['InfoOrder'] = next(FieldOrders)
            player.participant.vars['ParticipantNum'] = next(PartOrders)

    for player in subsession.get_players():
        player.InfoOrderGroup = player.participant.vars['InfoOrder']
        player.Participant_order = player.participant.vars['ParticipantNum']
        player.Dummy1 = next(TempDummy)

    import csv
    with open('Vignettes.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            for player in subsession.get_players():
                if int(row["Subject"]) == player.Participant_order and int(row["RoundNum"]) == player.round_number:
                    player.Agent = row["Agent"]
                    player.Outcome1 = row["Outcome1"]
                    player.Outcome2 = row["Outcome2"]
                    player.Action = row["Action"]
                    player.Incentive = row["Incentive"]
                    player.Pivotality = row["Pivotality"]
                    player.Context = row["Context"]

# Pages
class Consent(Page):
    form_model = 'player'
    form_fields = ['GivesConsent']
    def is_displayed(player):
        return player.round_number == 1     # only display in  first round

class Response(Page):
    form_model = 'player'
    form_fields = ['CausalScore','BonusScore']
    def vars_for_template(player: Player):
        return dict(OutcomeResponseTxt=response_outcome(player))


class InfoBlocks(Page):
    form_model = 'player'
    form_fields = ['Timeb1', 'Timeb2', 'Timeb3', 'Timeb4', 'Timeb5', 'Timeb6', 'Timeb7']
    @staticmethod
    def js_vars(player):
        return dict(
            InfoOrder = player.InfoOrderGroup,
            Agent = player.Agent,
            Outcome1 = player.Outcome1,
            Outcome2 = player.Outcome2,
            Action = player.Action,
            Incentive = player.Incentive,
            Pivotality = player.Pivotality,
            Context = player.Context,
            Dummy = player.Dummy1
        )

    @staticmethod
    def vars_for_template(player: Player):
        return dict(OutcomeResponseTxt=context_description(player))

class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass

class FixationCross(Page):
    timeout_seconds = 1.5


class ExperimentAlmostDone(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds    # only display in  last round

class PostQuestions(Page):
    form_model = 'player'
    form_fields = ['Age','Nationality','Education','Employment','Email_Address','KeepPosted']

    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds    # only display in  last round

class Numeracy(Page):
    form_model = 'player'
    form_fields = ['Numeracy_Answer']
    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds    # only display in  last round

class Closing(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds    # only display in  last round

page_sequence = [Consent, FixationCross, InfoBlocks, Response, ExperimentAlmostDone, Numeracy, PostQuestions, Closing]
