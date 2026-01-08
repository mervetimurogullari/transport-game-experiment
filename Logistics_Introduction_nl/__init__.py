import time
from otree.api import *

author = "Merve"
doc = """Eerste deel van het onderzoek"""


class C(BaseConstants):
    NAME_IN_URL = "Logistics_Introduction_nl"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    POSITIONS = ["A", "B", "C"]
    oneens_eens_5_point_scale = [
            [1, "Helemaal mee oneens"],
            [2, "Niet mee eens"],
            [3, "Niet mee eens niet mee oneens"],
            [4, "Mee eens"],
            [5, "Helemaal mee eens"],
        ]


class Subsession(BaseSubsession):
    resources_AB = models.IntegerField()
    resources_AC = models.IntegerField()
    resources_BC = models.IntegerField()
    resources_ABC = models.IntegerField()


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    consent = models.BooleanField(choices=[[True, "Ja"], [False, "Nee"]])
    position = models.StringField()
    resources = models.IntegerField()
    trust_base_1 = models.IntegerField(
        label="Ze zullen dezelfde soort voorstellen doen tijdens alle stappen van de onderhandeling.",
        choices = C.oneens_eens_5_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_base_2 = models.IntegerField(
        label="Ze zullen voorstellen doen die duidelijk laten zien wat ze willen in de onderhandeling.",
        choices = C.oneens_eens_5_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_base_3 = models.IntegerField(
        label="Ze zullen een onderhandelingsstrategie gebruiken die ik goed kan voorspellen.",
        choices = C.oneens_eens_5_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_base_4 = models.IntegerField(
        label="Ze zullen steeds op dezelfde manier voorstellen doen en kiezen tijdens de onderhandeling.",
        choices = C.oneens_eens_5_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_base_5 = models.IntegerField(
        label="Ze zullen proberen om het geld eerlijk te verdelen als we een coalitie vormen in de onderhandeling.",
        choices = C.oneens_eens_5_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_base_6 = models.IntegerField(
        label="Ze zullen rekening houden met wat ik krijg als ze voorstellen doen in de onderhandeling.",
        choices = C.oneens_eens_5_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_base_7 = models.IntegerField(
        label="Ze zullen mijn voorstel waarschijnlijk accepteren als ik een coalitie met hen voorstel in de onderhandeling.",
        choices = C.oneens_eens_5_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_base_8 = models.IntegerField(
        label="Ze zullen rekening houden met mijn belangen tijdens de onderhandeling.",
        choices = C.oneens_eens_5_point_scale,
        widget=widgets.RadioSelect,
    )


# FUNCTIONS
def creating_session(subsession):
    session = subsession.session
    subsession.resources_AB = (
        session.config["resources_player_A"] + session.config["resources_player_B"]
    )
    subsession.resources_AC = (
        session.config["resources_player_A"] + session.config["resources_player_C"]
    )
    subsession.resources_BC = (
        session.config["resources_player_B"] + session.config["resources_player_C"]
    )
    subsession.resources_ABC = (
        session.config["resources_player_A"]
        + session.config["resources_player_B"]
        + session.config["resources_player_C"]
    )


def vars_for_template(player: Player):
    session = player.session
    subsession = player.subsession
    resources_player_A = session.config["resources_player_A"]
    resources_player_B = session.config["resources_player_B"]
    resources_player_C = session.config["resources_player_C"]
    decision_point = session.config["decision_point"]
    total_payoff = session.config["total_payoff"]
    base_fee = session.config["base_fee"]
    payoff_conversion = session.config["payoff_conversion"]
    max_bonus = total_payoff * payoff_conversion
    timeout_time = session.config["timeout_time"]
    timeout_time_minutes = timeout_time / 60
    comprehension_check = session.config["comprehension_check"]
    incentives = session.config["incentives"]
    timers = session.config["timers"]
    possible_coalitions_A = []
    possible_coalitions_B = []
    possible_coalitions_C = []
    possible_coalitions_all = []
    if subsession.resources_AB >= session.config["decision_point"]:
        possible_coalitions_A.append("AB")
        possible_coalitions_B.append("AB")
        possible_coalitions_all.append("AB")
    if subsession.resources_AC >= session.config["decision_point"]:
        possible_coalitions_A.append("AC")
        possible_coalitions_C.append("AC")
        possible_coalitions_all.append("AC")
    if subsession.resources_BC >= session.config["decision_point"]:
        possible_coalitions_B.append("BC")
        possible_coalitions_C.append("BC")
        possible_coalitions_all.append("BC")
    if (
        subsession.resources_ABC >= session.config["decision_point"]
        and session.config["grand_coalition"]
    ):
        possible_coalitions_A.append("ABC")
        possible_coalitions_B.append("ABC")
        possible_coalitions_C.append("ABC")
        possible_coalitions_all.append("ABC")
    return {
        "possible_coalitions_A": possible_coalitions_A,
        "possible_coalitions_B": possible_coalitions_B,
        "possible_coalitions_C": possible_coalitions_C,
        "possible_coalitions_all": possible_coalitions_all,
        "resources_player_A": resources_player_A,
        "resources_player_B": resources_player_B,
        "resources_player_C": resources_player_C,
        "total_payoff": total_payoff,
        "base_fee": base_fee,
        "payoff_conversion": payoff_conversion,
        "decision_point": decision_point,
        "max_bonus": max_bonus,
        "timeout_time": timeout_time,
        "timeout_time_minutes": timeout_time_minutes,
        "comprehension_check": comprehension_check,
        "incentives": incentives,
        "timers": timers,
    }


# PAGES
class InformedConsent(Page):
    form_model = "player"
    form_fields = ["consent"]

    @staticmethod
    def vars_for_template(player: Player):
        return vars_for_template(player)

    @staticmethod
    def error_message(player: Player, values):
        solution = dict(consent=True)
        error_messages = dict()
        for field_name in solution:
            if values[field_name] != solution[field_name]:
                error_messages[field_name] = (
                    "U kunt niet naar de volgende pagina gaan zonder uw toestemming te geven. Verlaat deze webpagina als u niet wilt deelnemen."
                )
        return error_messages


class Overview(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return vars_for_template(player)

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if participant.kicked == False:
            return True
        else:
            return False

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config["timeout_time"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if timeout_happened:
            participant.kicked = True


class GeneralInstructions(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return vars_for_template(player)

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if participant.kicked == False:
            return True
        else:
            return False

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config["timeout_time"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if timeout_happened:
            participant.kicked = True


class Instructions_Coalitions(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return vars_for_template(player)

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if participant.kicked == False:
            return True
        else:
            return False

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config["timeout_time"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if timeout_happened:
            participant.kicked = True


class Bonus(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return vars_for_template(player)

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if participant.kicked == False:
            return True
        else:
            return False

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config["timeout_time"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if timeout_happened:
            participant.kicked = True


class Instructions_Phases(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return vars_for_template(player)

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if participant.kicked == False:
            return True
        else:
            return False

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config["timeout_time"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if timeout_happened:
            participant.kicked = True


class T1(Page):
    """
    Baseline trust measurement for all, regardless the condition, not specific to each player.
    """

    form_model = "player"
    form_fields = [
        "trust_base_1",
        "trust_base_2",
        "trust_base_3",
        "trust_base_4",
        "trust_base_5",
        "trust_base_6",
        "trust_base_7",
        "trust_base_8",
    ]

    @staticmethod
    def is_displayed(player: Player):
        return not player.participant.kicked and player.round_number == 1

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config["timeout_time"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if timeout_happened:
            participant.kicked = True


class Groupassignment(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return vars_for_template(player)

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if participant.kicked == False:
            return True
        else:
            return False

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config["timeout_time"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if timeout_happened:
            participant.kicked = True

        participant.wait_page_arrival = time.time()


class Kicked(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if participant.kicked == True:
            return True
        else:
            return False
        
    @staticmethod
    def vars_for_template(player: Player):
        return vars_for_template(player)


page_sequence = [
    InformedConsent,
    Overview,
    GeneralInstructions,
    Instructions_Coalitions,
    Bonus,
    Instructions_Phases,
    T1,
    Groupassignment,
    Kicked,
]
