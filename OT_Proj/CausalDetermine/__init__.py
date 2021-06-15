from otree.api import *


doc = """
Causal Determination Mouse-tracking experiment
"""

class Constants(BaseConstants):
    name_in_url = 'CausalDetermine'
    players_per_group = None
    num_rounds = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    GivesConsent = models.BooleanField(widget=widgets.CheckboxInput(), label="Agree")
    CausalScore = models.StringField(widget=widgets.RadioSelectHorizontal, choices=['Not at all', 'Very Slightly', 'Slightly', 'Neutral', 'Moderately', 'Very much',
                                                                                     'Almost Entirely'], label="Causal Attribution: ")
    BonusScore = models.IntegerField(widget=widgets.RadioSelectHorizontal, choices=[[-10,'-10%'], [-1,'-1%'], [0,'0%'], [1,'1%'], [10,'10%']], label="Bonus / Malus: ")
    Timeb1 = models.FloatField(blank=True, default=0.0)
    Timeb2 = models.FloatField(blank=True, default=0.0)
    Timeb3 = models.FloatField(blank=True, default=0.0)
    Timeb4 = models.FloatField(blank=True, default=0.0)
    Timeb5 = models.FloatField(blank=True, default=0.0)
    Timeb6 = models.FloatField(blank=True, default=0.0)
    Timeb7 = models.FloatField(blank=True, default=0.0)

    Viewsb1 = models.IntegerField(blank=True, default=0)
    Viewsb2 = models.IntegerField(blank=True, default=0)
    Viewsb3 = models.IntegerField(blank=True, default=0)
    Viewsb4 = models.IntegerField(blank=True, default=0)
    Viewsb5 = models.IntegerField(blank=True, default=0)
    Viewsb6 = models.IntegerField(blank=True, default=0)
    Viewsb7 = models.IntegerField(blank=True, default=0)

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
        Context_Descr = "In the football scenario, the Agent is either a professional football player or a pre-programmed football-AI. This agent then, during a point in the game, is faced with either passing the ball, or shooting to try and score. Either way, this can result in a goal being scored off of the play, or not. The end outcome is then either a win or a loss at the end of the game, and that could be by various margins. For the sake of this experiment, assume that you support the team for which the agent is playing. <br><br><b><u>The question is: to what extent did the football agent cause their team to win/lose?</b></u> "
    elif player.Context == "Business":
        Context_Descr = "In the business scenario, the Agent is either a senior business executive or a pre-programmed strategic-AI. This agent then votes on whether or not their firm should adopt a new business strategy. The individual’s vote can pass by one or more votes on the voting panel (we do not consider cases where the agent was outvoted). In the months following the chosen strategy, the company then either sees an increase or a decrease in their profits; as well as either an improvement or worsening of their environmental footprint. <br><br><b><u>The question is: to what extent did the strategy agent cause their firm’s environmental footprint to improve/worsen?</b></u> "
    return Context_Descr

def buttonlabels(player: Player):
    if player.Context == "Football":
        #Self made OR statement since OTree was being bitchy
        if (player.InfoOrderGroup == "A" ) + (player.InfoOrderGroup == "B") >=1:
            button1 = "Human/A.I."
            button2 = "Shoot/Pass"
            button3 = "Motivation"
            button4 = "Win margin"
            button5 = "Score/Miss"
            button6 = "Home/Away"
            button7 = "Win/Lose"
        if player.InfoOrderGroup == "C":
            button1 = "Score/Miss"
            button2 = "Home/Away"
            button3 = "Human/A.I."
            button4 = "Motivation"
            button5 = "Win/Lose"
            button6 = "Win margin"
            button7 = "Shoot/Pass"
    if player.Context == "Business":
        if player.InfoOrderGroup == "A":
            button1 = "Human/A.I."
            button2 = "Strategy"
            button3 = "Motivation"
            button4 = "Vote margin"
            button5 = "Financial Outcome"
            button6 = "Industry"
            button7 = "Environment Outcome"
        if (player.InfoOrderGroup == "B") + (player.InfoOrderGroup == "C") >= 1:
            button1 = "Strategy"
            button2 = "Motivation"
            button3 = "Financial Outcome"
            button4 = "Human/A.I."
            button5 = "Industry"
            button6 = "Environment Outcome"
            button7 = "Vote margin"
    return button1, button2, button3, button4, button5, button6, button7

def buttonlabelsFootDummy(player: Player):
      #Self made OR statement since OTree was being bitchy
    if (player.InfoOrderGroup == "A" ) + (player.InfoOrderGroup == "B") >=1:
        button1 = "Human/A.I."
        button2 = "Shoot/Pass"
        button3 = "Motivation"
        button4 = "Win margin"
        button5 = "Score/Miss"
        button6 = "Home/Away"
        button7 = "Win/Lose"
    if player.InfoOrderGroup == "C":
        button1 = "Score/Miss"
        button2 = "Home/Away"
        button3 = "Human/A.I."
        button4 = "Motivation"
        button5 = "Win/Lose"
        button6 = "Win margin"
        button7 = "Shoot/Pass"
    return button1, button2, button3, button4, button5, button6, button7


def buttonlabelsBusDummy(player: Player):
    # Self made OR statement since OTree was being bitchy
    if player.InfoOrderGroup == "A":
        button1 = "Human/A.I."
        button2 = "Strategy"
        button3 = "Motivation"
        button4 = "Vote margin"
        button5 = "Financial Outcome"
        button6 = "Industry"
        button7 = "Environment Outcome"
    if (player.InfoOrderGroup == "B") + (player.InfoOrderGroup == "C") >= 1:
        button1 = "Strategy"
        button2 = "Motivation"
        button3 = "Financial Outcome"
        button4 = "Human/A.I."
        button5 = "Industry"
        button6 = "Environment Outcome"
        button7 = "Vote margin"
    return button1, button2, button3, button4, button5, button6, button7

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

class ExampleFootball(Page):
    def is_displayed(player):
        return player.round_number == 1   # only display in  first round
    @staticmethod
    def js_vars(player):
        return dict(
            InfoOrder = player.InfoOrderGroup,
        )
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            Button1=buttonlabelsFootDummy(player)[0],
            Button2=buttonlabelsFootDummy(player)[1],
            Button3=buttonlabelsFootDummy(player)[2],
            Button4=buttonlabelsFootDummy(player)[3],
            Button5=buttonlabelsFootDummy(player)[4],
            Button6=buttonlabelsFootDummy(player)[5],
            Button7=buttonlabelsFootDummy(player)[6]
        )

class ExampleBusiness(Page):
    def is_displayed(player):
        return player.round_number == 1  # only display in  first round
    @staticmethod
    def js_vars(player):
        return dict(
            InfoOrder=player.InfoOrderGroup,
        )
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            Button1=buttonlabelsBusDummy(player)[0],
            Button2=buttonlabelsBusDummy(player)[1],
            Button3=buttonlabelsBusDummy(player)[2],
            Button4=buttonlabelsBusDummy(player)[3],
            Button5=buttonlabelsBusDummy(player)[4],
            Button6=buttonlabelsBusDummy(player)[5],
            Button7=buttonlabelsBusDummy(player)[6]
        )

class Response(Page):
    form_model = 'player'
    form_fields = ['CausalScore','BonusScore']
    def vars_for_template(player: Player):
        return dict(OutcomeResponseTxt=response_outcome(player))


class InfoBlocks(Page):
    form_model = 'player'
    form_fields = ['Timeb1', 'Timeb2', 'Timeb3', 'Timeb4', 'Timeb5', 'Timeb6', 'Timeb7', 'Viewsb1', 'Viewsb2', 'Viewsb3', 'Viewsb4', 'Viewsb5', 'Viewsb6', 'Viewsb7']
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
        return dict(
            ContextDescr=context_description(player),
            Button1=buttonlabels(player)[0],
            Button2=buttonlabels(player)[1],
            Button3=buttonlabels(player)[2],
            Button4=buttonlabels(player)[3],
            Button5=buttonlabels(player)[4],
            Button6=buttonlabels(player)[5],
            Button7=buttonlabels(player)[6]


        )

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



page_sequence = [Consent, ExampleFootball, ExampleBusiness, FixationCross, InfoBlocks, Response, ExperimentAlmostDone, Numeracy, PostQuestions, Closing]
