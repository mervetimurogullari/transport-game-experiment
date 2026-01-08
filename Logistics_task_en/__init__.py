import random
import string
import time
import csv
from otree.api import *

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

# example: store the file inside your app folder
preload_csv = "Logistics_task_en/data/svo_preload_example.csv"

author = "Merve"
doc = """
Second section of the study
"""


class C(BaseConstants):
    NAME_IN_URL = "Logistics_task_en"
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 20
    POSITIONS = ["A", "B", "C"]
    five_point_scale = [
            [1, "Strongly Disagree"],
            [2, "Disagree"],
            [3, "Neither Agree nor Disagree"],
            [4, "Agree"],
            [5, "Strongly Agree"],
        ]


class Subsession(BaseSubsession):
    resources_AB = models.IntegerField()
    resources_AC = models.IntegerField()
    resources_BC = models.IntegerField()
    resources_ABC = models.IntegerField()


class Group(BaseGroup):
    # Initialize treatment as False
    is_experimental = models.BooleanField(
        initial= False
    )  
    proposed_coalition_player_A = models.StringField(
        widget=widgets.RadioSelect,
    )
    proposed_coalition_player_B = models.StringField(
        widget=widgets.RadioSelect,
    )
    proposed_coalition_player_C = models.StringField(
        widget=widgets.RadioSelect,
    )
    allocation_A_to_A = models.IntegerField()
    allocation_A_to_B = models.IntegerField()
    allocation_A_to_C = models.IntegerField()
    allocation_B_to_A = models.IntegerField()
    allocation_B_to_B = models.IntegerField()
    allocation_B_to_C = models.IntegerField()
    allocation_C_to_A = models.IntegerField()
    allocation_C_to_B = models.IntegerField()
    allocation_C_to_C = models.IntegerField()
    selected_coalition_name_player_A = models.StringField()
    selected_coalition_name_player_B = models.StringField()
    selected_coalition_name_player_C = models.StringField()
    selected_coalition_allocation_A_player_A = models.IntegerField()
    selected_coalition_allocation_B_player_A = models.IntegerField()
    selected_coalition_allocation_C_player_A = models.IntegerField()
    selected_coalition_allocation_A_player_B = models.IntegerField()
    selected_coalition_allocation_B_player_B = models.IntegerField()
    selected_coalition_allocation_C_player_B = models.IntegerField()
    selected_coalition_allocation_A_player_C = models.IntegerField()
    selected_coalition_allocation_B_player_C = models.IntegerField()
    selected_coalition_allocation_C_player_C = models.IntegerField()
    coalition_formed = models.BooleanField(default=False)
    formed_coalition_name = models.StringField()
    payoff_A = models.IntegerField()
    payoff_B = models.IntegerField()
    payoff_C = models.IntegerField()


class Player(BasePlayer):
    gauge_plot_svo = models.LongStringField()
    # Set initial svo_score to -19 (out of the scope), this score is overwritten when a value is found in the preload csv.
    svo_score = models.IntegerField(
        initial= -19
    ) 
    completion_code = models.StringField()
    position = models.StringField()
    resources = models.IntegerField()
    comment = models.StringField(blank=True)
    # age = models.IntegerField()
    # gender = models.IntegerField(
    #     choices=[
    #         [0, "Vrouw"],
    #         [1, "Man"],
    #         [2, "Anders"],
    #         [3, "Geen voorkeur om te antwoorden"],
    #     ],
    #     widget=widgets.RadioSelect(),
    # )
    comprehension_position = models.IntegerField(widget=widgets.RadioSelect())
    comprehension_position_fail = models.IntegerField()
    comprehension_resources = models.IntegerField(widget=widgets.RadioSelect())
    comprehension_resources_fail = models.IntegerField()
    comprehension_bonus = models.IntegerField(
        choices=[
            [0, "10000 euros"],
            [1, "9000 euros"],
            [2, "8000 euros"],
        ],
        widget=widgets.RadioSelect(),
    )
    comprehension_bonus_fail = models.IntegerField()
    comprehension_coalitions = models.IntegerField(widget=widgets.RadioSelect())
    comprehension_coalitions_fail = models.IntegerField()
    proposed_coalition = models.StringField(max_length=3)
    selected_coalition = models.StringField()
    selected_coalition_name = models.StringField(max_length=3)
    selected_coalition_allocation_A = models.IntegerField()
    selected_coalition_allocation_B = models.IntegerField()
    selected_coalition_allocation_C = models.IntegerField()
    allocate_to_player_A = models.IntegerField(blank=True, null=True, initial=0)
    allocate_to_player_B = models.IntegerField(blank=True, null=True, initial=0)
    allocate_to_player_C = models.IntegerField(blank=True, null=True, initial=0)
    money = models.IntegerField()

    # Trust measurement items; after the information. For both groups, specific to each player
    trust_pre_1_A_to_B = models.IntegerField(
        label="Player B will make consistent offers while negotiating.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_2_A_to_B = models.IntegerField(
        label="Player B will make offers that clearly show what they want in the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_3_A_to_B = models.IntegerField(
        label="Player B will use a negotiation strategy that I can easily predict throughout.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_4_A_to_B = models.IntegerField(
        label="Player B will use the same approach when making and accepting offers throughout the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_5_A_to_B = models.IntegerField(
        label="Player B will aim to share the bonus fairly if we form a coalition in the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_6_A_to_B = models.IntegerField(
        label="Player B will care about my outcomes when making offers in the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_7_A_to_B = models.IntegerField(
        label="Player B will likely accept if I propose a coalition with them in the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_8_A_to_B = models.IntegerField(
        label="Player B will look out for my interests in the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )

    #####################################

    trust_pre_1_A_to_C = models.IntegerField(
        label="Player C will make consistent offers while negotiating.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_2_A_to_C = models.IntegerField(
        label="Player C will make offers that clearly show what they want in the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_3_A_to_C = models.IntegerField(
        label="Player C will use a negotiation strategy that I can easily predict throughout.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_4_A_to_C = models.IntegerField(
        label="Player C will use the same approach when making and accepting offers throughout the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_5_A_to_C = models.IntegerField(
        label="Player C will aim to share the bonus fairly if we form a coalition in the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_6_A_to_C = models.IntegerField(
        label="Player C will care about my outcomes when making offers in the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_7_A_to_C = models.IntegerField(
        label="Player C will likely accept if I propose a coalition with them in the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_8_A_to_C = models.IntegerField(
        label="Player C will look out for my interests in the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )

    #####################################

    trust_pre_1_B_to_A = models.IntegerField(
        label="Player A will make consistent offers while negotiating.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_2_B_to_A = models.IntegerField(
        label="Player A will make offers that clearly show what they want in the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_3_B_to_A = models.IntegerField(
        label="Player A will use a negotiation strategy that I can easily predict throughout.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_4_B_to_A = models.IntegerField(
        label="Player A will use the same approach when making and accepting offers throughout the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_5_B_to_A = models.IntegerField(
        label="Player A will aim to share the bonus fairly if we form a coalition in the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_6_B_to_A = models.IntegerField(
        label="Player A will care about my outcomes when making offers in the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_7_B_to_A = models.IntegerField(
        label="Player A will likely accept if I propose a coalition with them in the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_8_B_to_A = models.IntegerField(
        label="Player A will look out for my interests in the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )

    #####################################

    trust_pre_1_B_to_C = models.IntegerField(
        label="Player C will make consistent offers while negotiating.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_2_B_to_C = models.IntegerField(
        label="Player C will make offers that clearly show what they want in the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_3_B_to_C = models.IntegerField(
        label="Player C will use a negotiation strategy that I can easily predict throughout.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_4_B_to_C = models.IntegerField(
        label="Player C will use the same approach when making and accepting offers throughout the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_5_B_to_C = models.IntegerField(
        label="Player C will aim to share the bonus fairly if we form a coalition in the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_6_B_to_C = models.IntegerField(
        label="Player C will care about my outcomes when making offers in the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_7_B_to_C = models.IntegerField(
        label="Player C will likely accept if I propose a coalition with them in the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_8_B_to_C = models.IntegerField(
        label="Player C will look out for my interests in the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )

    #####################################

    trust_pre_1_C_to_A = models.IntegerField(
        label="Player A will make consistent offers while negotiating.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_2_C_to_A = models.IntegerField(
        label="Player A will make offers that clearly show what they want in the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_3_C_to_A = models.IntegerField(
        label="Player A will use a negotiation strategy that I can easily predict throughout.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_4_C_to_A = models.IntegerField(
        label="Player A will use the same approach when making and accepting offers throughout the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_5_C_to_A = models.IntegerField(
        label="Player A will aim to share the bonus fairly if we form a coalition in the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_6_C_to_A = models.IntegerField(
        label="Player A will care about my outcomes when making offers in the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_7_C_to_A = models.IntegerField(
        label="Player A will likely accept if I propose a coalition with them in the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_8_C_to_A = models.IntegerField(
        label="Player A will look out for my interests in the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )

    #####################################

    trust_pre_1_C_to_B = models.IntegerField(
        label="Player B will make consistent offers while negotiating.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_2_C_to_B = models.IntegerField(
        label="Player B will make offers that clearly show what they want in the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_3_C_to_B = models.IntegerField(
        label="Player B will use a negotiation strategy that I can easily predict throughout.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_4_C_to_B = models.IntegerField(
        label="Player B will use the same approach when making and accepting offers throughout the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_5_C_to_B = models.IntegerField(
        label="Player B will aim to share the bonus fairly if we form a coalition in the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_6_C_to_B = models.IntegerField(
        label="Player B will care about my outcomes when making offers in the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_7_C_to_B = models.IntegerField(
        label="Player B will likely accept if I propose a coalition with them in the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_pre_8_C_to_B = models.IntegerField(
        label="Player B will look out for my interests in the negotiation.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    ###############################################################################################################

    # Trust measurement, after the negotiation. For both groups, specific to each player

    trust_aft_1_A_to_B = models.IntegerField(
        label="Player B will make consistent offers in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_2_A_to_B = models.IntegerField(
        label="Player B will make offers that clearly show what they want in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_3_A_to_B = models.IntegerField(
        label="Player B will use a predictable negotiation strategy throughout future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_4_A_to_B = models.IntegerField(
        label="Player B will use the same approach when making and accepting offers throughout future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_5_A_to_B = models.IntegerField(
        label="Player B will aim to share the bonus fairly if we form a coalition in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_6_A_to_B = models.IntegerField(
        label="Player B will care about my outcomes when making offers in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_7_A_to_B = models.IntegerField(
        label="Player B will likely accept if I propose a coalition with them in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_8_A_to_B = models.IntegerField(
        label="Player B will look out for my interests in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )

    #####################################

    trust_aft_1_A_to_C = models.IntegerField(
        label="Player C will make consistent offers in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_2_A_to_C = models.IntegerField(
        label="Player C will make offers that clearly show what they want in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_3_A_to_C = models.IntegerField(
        label="Player C will use a predictable negotiation strategy throughout future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_4_A_to_C = models.IntegerField(
        label="Player C will use the same approach when making and accepting offers throughout future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_5_A_to_C = models.IntegerField(
        label="Player C will aim to share the bonus fairly if we form a coalition in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_6_A_to_C = models.IntegerField(
        label="Player C will care about my outcomes when making offers in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_7_A_to_C = models.IntegerField(
        label="Player C will likely accept if I propose a coalition with them in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_8_A_to_C = models.IntegerField(
        label="Player C will look out for my interests in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )

    #####################################

    trust_aft_1_B_to_A = models.IntegerField(
        label="Player A will make consistent offers in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_2_B_to_A = models.IntegerField(
        label="Player A will make offers that clearly show what they want in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_3_B_to_A = models.IntegerField(
        label="Player A will use a predictable negotiation strategy throughout future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_4_B_to_A = models.IntegerField(
        label="Player A will use the same approach when making and accepting offers throughout future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_5_B_to_A = models.IntegerField(
        label="Player A will aim to share the bonus fairly if we form a coalition in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_6_B_to_A = models.IntegerField(
        label="Player A will care about my outcomes when making offers in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_7_B_to_A = models.IntegerField(
        label="Player A will likely accept if I propose a coalition with them in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_8_B_to_A = models.IntegerField(
        label="Player A will look out for my interests in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )

    #####################################

    trust_aft_1_B_to_C = models.IntegerField(
        label="Player C will make consistent offers in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_2_B_to_C = models.IntegerField(
        label="Player C will make offers that clearly show what they want in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_3_B_to_C = models.IntegerField(
        label="Player C will use a predictable negotiation strategy throughout future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_4_B_to_C = models.IntegerField(
        label="Player C will use the same approach when making and accepting offers throughout future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_5_B_to_C = models.IntegerField(
        label="Player C will aim to share the bonus fairly if we form a coalition in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_6_B_to_C = models.IntegerField(
        label="Player C will care about my outcomes when making offers in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_7_B_to_C = models.IntegerField(
        label="Player C will likely accept if I propose a coalition with them in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_8_B_to_C = models.IntegerField(
        label="Player C will look out for my interests in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )

    #####################################

    trust_aft_1_C_to_A = models.IntegerField(
        label="Player A will make consistent offers in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_2_C_to_A = models.IntegerField(
        label="Player A will make offers that clearly show what they want in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_3_C_to_A = models.IntegerField(
        label="Player A will use a predictable negotiation strategy throughout future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_4_C_to_A = models.IntegerField(
        label="Player A will use the same approach when making and accepting offers throughout future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_5_C_to_A = models.IntegerField(
        label="Player A will aim to share the bonus fairly if we form a coalition in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_6_C_to_A = models.IntegerField(
        label="Player A will care about my outcomes when making offers in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_7_C_to_A = models.IntegerField(
        label="Player A will likely accept if I propose a coalition with them in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_8_C_to_A = models.IntegerField(
        label="Player A will look out for my interests in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )

    #####################################

    trust_aft_1_C_to_B = models.IntegerField(
        label="Player B will make consistent offers in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_2_C_to_B = models.IntegerField(
        label="Player B will make offers that clearly show what they want in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_3_C_to_B = models.IntegerField(
        label="Player B will use a predictable negotiation strategy throughout future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_4_C_to_B = models.IntegerField(
        label="Player B will use the same approach when making and accepting offers throughout future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_5_C_to_B = models.IntegerField(
        label="Player B will aim to share the bonus fairly if we form a coalition in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_6_C_to_B = models.IntegerField(
        label="Player B will care about my outcomes when making offers in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_7_C_to_B = models.IntegerField(
        label="Player B will likely accept if I propose a coalition with them in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )
    trust_aft_8_C_to_B = models.IntegerField(
        label="Player B will look out for my interests in future negotiations.",
        choices = C.five_point_scale,
        widget=widgets.RadioSelect,
    )

    ##################################### Only for leftovers, for a graceful ending

    competition = models.IntegerField(
        label="Could you give your opinion on the following issue. How would you place your views on this scale?",
        choices=[
            [
                1,
                "1 Competition is good. It stimulates people to work hard and develop new ideas",
            ],
            [2, "2"],
            [3, "3"],
            [4, "4"],
            [5, "5 Competition is harmful, it brings out the worst in people"],
            [6, "I don't know"],
        ],
        widget=widgets.RadioSelect,
    )

    gen_trust_1 = models.IntegerField(
        label="Generally speaking, would you say that most people can be trusted, or that you can’t be too careful in dealing with people? Please indicate a score between 1 and 5, where 1 means you can’t be too careful and 5 means that most people can be trusted.",
        choices=[
            [1, "1 You can’t be too careful"],
            [2, "2"],
            [3, "3"],
            [4, "4"],
            [5, "5 Most people can be trusted"],
            [6, "I don't know"],
        ],
        widget=widgets.RadioSelect,
    )

    gen_trust_2 = models.IntegerField(
        label="Do you think that most people would try to take advantage of you if they got the chance, or would they try to be fair? Please indicate a score of 1 to 5, where 1 means most people would try to take advantage of you and 5 means that most people would try to be fair.",
        choices=[
            [1, "1 Most people would try to take advantage of me"],
            [2, "2"],
            [3, "3"],
            [4, "4"],
            [5, "5 Most people would try to be fair"],
            [6, "I don't know"],
        ],
        widget=widgets.RadioSelect,
    )

    gen_trust_3 = models.IntegerField(
        label="Would you say that most of the time people try to be helpful or that they are mostly looking out for themselves? Please select a score from 1 to 5, where 1 means most people look out for themselves and 5 means that most people would try to be helpful.",
        choices=[
            [1, "1 People mostly look out for themselves"],
            [2, "2"],
            [3, "3"],
            [4, "4"],
            [5, "5 People mostly try to be helpful"],
            [6, "I don't know"],
        ],
        widget=widgets.RadioSelect,
    )

    gen_trust_4 = models.IntegerField(
        label="Would you say that most people deserve your trust or that only very few deserve your trust? Please indicate a score of 1 to 5, where 1 means very few people deserve your trust and 5 means that most people deserve your trust.",
        choices=[
            [1, "1 Very few people deserve my trust"],
            [2, "2"],
            [3, "3"],
            [4, "4"],
            [5, "5 Most people deserve my trust"],
            [6, "I don't know"],
        ],
        widget=widgets.RadioSelect,
    )

    ###############################################################################################################


# FUNCTIONS
# Create gauge plot for svo scores
def create_gauge(svo_value):

    fig, ax = plt.subplots(
        figsize=(6, 3),
        subplot_kw={"projection": "polar"},
        constrained_layout=False,
    )

    ax.set_theta_zero_location("W")
    ax.set_theta_direction(-1)

    category_boundaries_deg = np.linspace(0, 180, 7)
    category_boundaries_rad = np.radians(category_boundaries_deg)

    def determine_color(degree):
        index = int(degree // 30)
        colors = ["#7CB9E8" if i == index else "white" for i in range(6)]
        return colors

    def value_to_degrees(value):
        if -20 <= value < 1.5:
            return np.interp(value, [-20, 1.5], [0, 30])
        elif 1.5 <= value < 9.5:
            return np.interp(value, [1.5, 9.5], [30, 60])
        elif 9.5 <= value < 22.45:
            return np.interp(value, [9.5, 22.45], [60, 90])
        elif 22.45 <= value < 30.8:
            return np.interp(value, [22.45, 30.8], [90, 120])
        elif 30.8 <= value < 36.3:
            return np.interp(value, [30.8, 36.3], [120, 150])
        elif 36.3 <= value <= 65:
            return np.interp(value, [36.3, 65], [150, 180])
        return 0

    # Generate the plot based on the player's value
    degree = value_to_degrees(svo_value)
    section_colors = determine_color(degree)

    # Clear the axes and draw the plot
    ax.set_yticklabels([])
    ax.grid(False)
    ax.spines["polar"].set_visible(False)
    ax.set_xticklabels([])
    ax.set_rlim(0, 1.3)

    for i in range(len(category_boundaries_rad) - 1):
        theta_start = category_boundaries_rad[i]
        theta_end = category_boundaries_rad[i + 1]
        theta = np.linspace(theta_start, theta_end, 100)
        r = np.ones_like(theta)
        ax.fill_between(
            theta, 0, r, color=section_colors[i], edgecolor="#696969", linewidth=1
        )

    # Draw the needle
    needle_theta = np.radians(degree)
    triangle_width = np.radians(4)
    triangle_height = 0.15
    triangle_theta = [
        needle_theta - triangle_width / 2,
        needle_theta + triangle_width / 2,
        needle_theta,
    ]
    triangle_radius = [1.2, 1.2, 1.2 - triangle_height]

    ax.fill(triangle_theta, triangle_radius, color="#696969")

    # Labels with adjusted positions
    ax.text(
        np.radians(0),
        1.3,
        "Self",
        ha="center",
        va="center",
        fontsize=12,
        color="#696969",
    )
    ax.text(
        np.radians(180),
        1.3,
        "Other",
        ha="center",
        va="center",
        fontsize=12,
        color="#696969",
    )

    # Save the figure with tight bounding box
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    buf.seek(0)
    image_png = buf.getvalue()
    buf.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode("utf-8")

    return graphic


def creating_session(subsession: Subsession):
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
    for p in subsession.get_players():
        p.participant.end_game = False
    for p in subsession.get_players():
        p.participant.grouped = False
    for p in subsession.get_players():
        p.participant.leftover = False
    for p in subsession.get_players():
        p.participant.kicked = False
    for p in subsession.get_players():
        p.completion_code = "DS" + "".join(random.choices(string.digits, k=4))


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


def offer_summary(player: Player):
    offers = (
        player.allocate_to_player_A,
        player.allocate_to_player_B,
        player.allocate_to_player_C,
    )
    offers_int = map(int, offers)
    offers_str = map(str, offers_int)
    return "-".join(offers_str)


def leftover_check(player: Player):
    participant = player.participant
    group = player.group
    other_players = player.get_others_in_group()
    for p in other_players:
        if p.participant.kicked == True:
            participant.leftover = True
        if (
            p.participant._current_page_name == "Funnel"
            and group.coalition_formed == False
        ):
            participant.leftover = True
        if (
            p.participant._current_page_name == "Debriefing"
            and group.coalition_formed == False
        ):
            participant.leftover = True
        if (
            p.participant._current_page_name == "Kicked"
            and group.coalition_formed == False
        ):
            participant.leftover = True


def comprehension_position_choices(player: Player):
    session = player.session
    choices = [
        [0, "Company A"],
        [1, "Company B"],
        [2, "Company C"],
    ]
    return choices


def comprehension_position_error_message(player: Player, value):
    session = player.session
    if (
        (player.position == "A" and value != 0)
        or (player.position == "B" and value != 1)
        or (player.position == "C" and value != 2)
    ):
        player.comprehension_position_fail = 1
        return "This is incorrect. You are representing Company {}. Please enter the correct answer.".format(
            player.position
        )


def comprehension_resources_choices(player: Player):
    session = player.session
    choices = [
        [0, "My company transports 4 tons"],
        [1, "My company transports 3 tons"],
        [2, "My company transports 2 tons"],
    ]
    return choices


def comprehension_resources_error_message(player: Player, value):
    session = player.session
    if (
        (player.position == "A" and value != 0)
        or (player.position == "B" and value != 1)
        or (player.position == "C" and value != 2)
    ):
        player.comprehension_resources_fail = 1
        return "This is not correct. You are transporting {} tons. Please enter the correct answer.".format(
            player.resources
        )


def comprehension_coalitions_choices(player: Player):
    session = player.session
    choices = []
    if not session.config["grand_coalition"]:
        choices = [
            [0, "AB, AC "],
            [1, "AB, BC"],
            [2, "AC, BC"],
            [3, "AB, AC, BC"],
        ]
    elif session.config["grand_coalition"]:
        choices = [
            [0, "AB, AC "],
            [1, "AB, BC"],
            [2, "AC, BC"],
            [3, "AB, AC, BC"],
            [4, "AB, AC, BC, ABC"],
        ]
    return choices


def comprehension_coalitions_error_message(player: Player, value):
    session = player.session
    if session.config["grand_coalition"] == False and value != 3:
        if value == 0:
            player.comprehension_coalitions_fail = 0
        if value == 1:
            player.comprehension_coalitions_fail = 1
        if value == 2:
            player.comprehension_coalitions_fail = 2
        return "This is incorrect. There are 3 possible coalitions: AB, AC and BC. Please enter the correct answer."
    if session.config["grand_coalition"] == True and value != 4:
        if value == 0:
            player.comprehension_coalitions_fail = 1
        return "This is incorrect. There are 4 possible coalitions: AB, AC, BC and ABC. Please enter the correct answer."


def comprehension_bonus_error_message(player: Player, value):
    if value != 1:
        player.comprehension_bonus_fail = 1
        return "This is not correct. You are negotiating an amount of 9000 euros. Please enter the correct answer."


def waiting_too_long(player):
    participant = player.participant
    return (time.time() - participant.wait_page_arrival) > 5 * 60


def group_by_arrival_time_method(subsession, waiting_players):
    if len(waiting_players) >= 3:
        return waiting_players[:3]
    for player in waiting_players:
        if waiting_too_long(player):
            player.participant.leftover = True


# PAGES
class Waitforgroup(WaitPage):
    title_text = "Matching you with participants"
    body_text = "Please wait a few minutes for other participants."
    group_by_arrival_time = True
    startwp_timer = 5 * 60

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if (
            participant.end_game == False
            and player.round_number == 1
            and participant.kicked == False
            and participant.leftover == False
        ):
            return True
        else:
            return False


class Groupingconfirmation(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return vars_for_template(player)

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if (
            participant.end_game == False
            and player.round_number == 1
            and participant.kicked == False
            and participant.leftover == False
        ):
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
        participant.grouped = True
        leftover_check(player)


class Waitforparticipants(WaitPage):

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        session = player.session
        if (
            participant.end_game == False
            and player.round_number == 1
            and participant.grouped == True
            and participant.kicked == False
            and participant.leftover == False
        ):
            return True
        else:
            return False

    title_text = "Position assignment"
    body_text = "You will be randomly assigned a position"

    @staticmethod
    def after_all_players_arrive(group: Group):
        session = group.session
        p1 = group.get_player_by_id(1)
        p2 = group.get_player_by_id(2)
        p3 = group.get_player_by_id(3)

        # Assign roles and resources
        p1.position = "A"
        p1.resources = session.config["resources_player_A"]

        p2.position = "B"
        p2.resources = session.config["resources_player_B"]

        p3.position = "C"
        p3.resources = session.config["resources_player_C"]


        # Assign SVO scores based on preload_csv
        # NOTE:
        # This code assumes that an external CSV file is provided.
        # If no CSV file is supplied, or if the expected columns are missing,
        # the code will raise an error. Users who wish to use this functionality
        # should adapt the file path, identifier column, and SVO column
        # to match their own data and oTree setup.
        #
        # The CSV is expected to contain:
        #  - 'participant_id': an identifier matching the participant in oTree
        #  - 'svo_score': the participant's SVO value

        with open(preload_csv, encoding='utf-8-sig', mode='r') as file:
            csv_reader = list(csv.DictReader(file, delimiter=";"))
            for p in group.get_players(): 
                for row in csv_reader: 
                    if row['participant_id'] == p.participant.label: 
                        svo_score = row['svo_score']
                        if svo_score is not None and svo_score != "":
                            p.svo_score = float(svo_score.replace(',', '.'))
                        else:                
                            print(f"For {p.participant} No SVO score found for participant. Initial value is kept.")
                        break

        # Set experimental condition 50/50 based on group ID.
        group.is_experimental = group.id_in_subsession % 2 == 0


class SVO_Assigned(Page):
    @staticmethod
    def is_displayed(player: Player):
        # If it is on the first round, assign the SVO scores
        if player.round_number == 1:
            player.gauge_plot_svo = create_gauge(player.svo_score)  
        else:
            player.svo_score = player.in_round(1).svo_score  # Assign the first rounds' svo score so that it does not reset for each round
            player.gauge_plot_svo = player.in_round(1).gauge_plot_svo
            player.position = player.in_round(1).position
            # Retreive other players' SVO assignments too
            for other_player in player.get_others_in_group():
                other_player.svo_score = other_player.in_round(1).svo_score  # Assign the first rounds svo score
                other_player.gauge_plot_svo = other_player.in_round(1).gauge_plot_svo  # Assign the first rounds gauge plot
                other_player.position = other_player.in_round(1).position
        return False

    @staticmethod
    def vars_for_template(player: Player):
        return vars_for_template(player)


class AssignedPosition(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if (
            participant.end_game == False
            and player.round_number == 1
            and participant.kicked == False
            and participant.leftover == False
        ):
            return True
        else:
            return False

    @staticmethod
    def vars_for_template(player: Player):
        return vars_for_template(player)

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config["timeout_time"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if timeout_happened:
            participant.kicked = True
        leftover_check(player)


class AssignedPosition2(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if (
            participant.end_game == False
            and player.round_number == 1
            and participant.kicked == False
            and participant.leftover == False
        ):
            return True
        else:
            return False

    @staticmethod
    def vars_for_template(player: Player):
        return vars_for_template(player)

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config["timeout_time"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if timeout_happened:
            participant.kicked = True
        leftover_check(player)


class ComprehensionCheck(Page):
    form_model = "player"
    form_fields = ["comprehension_position"]

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        session = player.session
        if (
            session.config["comprehension_check"] == True
            and player.round_number == 1
            and participant.kicked == False
            and participant.leftover == False
        ):
            return True
        else:
            return False

    @staticmethod
    def vars_for_template(player: Player):
        vars = vars_for_template(player)
        vars.update({"position_label": "Which company do you represent?"})
        return vars

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config["timeout_time"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if timeout_happened:
            participant.kicked = True
        leftover_check(player)


class ComprehensionCheck1(Page):
    form_model = "player"
    form_fields = ["comprehension_resources"]

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        session = player.session
        if (
            session.config["comprehension_check"] == True
            and player.round_number == 1
            and participant.kicked == False
            and participant.leftover == False
        ):
            return True
        else:
            return False

    @staticmethod
    def vars_for_template(player: Player):
        vars = vars_for_template(player)
        vars.update(
            {
                "resources_label": "How many tons does your company transport to Paris each day?"
            }
        )
        return vars

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config["timeout_time"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if timeout_happened:
            participant.kicked = True
        leftover_check(player)


class ComprehensionCheck2(Page):
    form_model = "player"
    form_fields = ["comprehension_bonus"]

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        session = player.session
        if (
            session.config["comprehension_check"] == True
            and player.round_number == 1
            and participant.kicked == False
            and participant.leftover == False
        ):
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
        leftover_check(player)


class ComprehensionCheck3(Page):
    form_model = "player"
    form_fields = ["comprehension_coalitions"]

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        session = player.session
        if (
            session.config["comprehension_check"] == True
            and player.round_number == 1
            and participant.kicked == False
            and participant.leftover == False
        ):
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
        leftover_check(player)


class T2_A(Page):
    """
    Trust measurement page after information, the description depends on the condition (check the html). Speficic to each player.
    """

    form_model = "player"
    form_fields = [
        "trust_pre_1_A_to_B",
        "trust_pre_2_A_to_B",
        "trust_pre_3_A_to_B",
        "trust_pre_4_A_to_B",
        "trust_pre_5_A_to_B",
        "trust_pre_6_A_to_B",
        "trust_pre_7_A_to_B",
        "trust_pre_8_A_to_B",
        "trust_pre_1_A_to_C",
        "trust_pre_2_A_to_C",
        "trust_pre_3_A_to_C",
        "trust_pre_4_A_to_C",
        "trust_pre_5_A_to_C",
        "trust_pre_6_A_to_C",
        "trust_pre_7_A_to_C",
        "trust_pre_8_A_to_C",
    ]

    @staticmethod
    def is_displayed(player: Player):
        return (
            not player.participant.kicked
            and player.round_number == 1
            and player.participant.kicked == False
            and player.participant.leftover == False
            and player.position == "A"
        )

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config["timeout_time"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if timeout_happened:
            participant.kicked = True
        leftover_check(player)


class T2_B(Page):
    """
    Trust measurement page after information, the description depends on the condition (check the html). Speficic to each player.
    """

    form_model = "player"
    form_fields = [
        "trust_pre_1_B_to_A",
        "trust_pre_2_B_to_A",
        "trust_pre_3_B_to_A",
        "trust_pre_4_B_to_A",
        "trust_pre_5_B_to_A",
        "trust_pre_6_B_to_A",
        "trust_pre_7_B_to_A",
        "trust_pre_8_B_to_A",
        "trust_pre_1_B_to_C",
        "trust_pre_2_B_to_C",
        "trust_pre_3_B_to_C",
        "trust_pre_4_B_to_C",
        "trust_pre_5_B_to_C",
        "trust_pre_6_B_to_C",
        "trust_pre_7_B_to_C",
        "trust_pre_8_B_to_C",
    ]

    @staticmethod
    def is_displayed(player: Player):
        return (
            not player.participant.kicked
            and player.round_number == 1
            and player.participant.kicked == False
            and player.participant.leftover == False
            and player.position == "B"
        )

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config["timeout_time"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if timeout_happened:
            participant.kicked = True
        leftover_check(player)


class T2_C(Page):
    """
    Trust measurement page after information, the description depends on the condition (check the html). Speficic to each player.
    """

    form_model = "player"
    form_fields = [
        "trust_pre_1_C_to_A",
        "trust_pre_2_C_to_A",
        "trust_pre_3_C_to_A",
        "trust_pre_4_C_to_A",
        "trust_pre_5_C_to_A",
        "trust_pre_6_C_to_A",
        "trust_pre_7_C_to_A",
        "trust_pre_8_C_to_A",
        "trust_pre_1_C_to_B",
        "trust_pre_2_C_to_B",
        "trust_pre_3_C_to_B",
        "trust_pre_4_C_to_B",
        "trust_pre_5_C_to_B",
        "trust_pre_6_C_to_B",
        "trust_pre_7_C_to_B",
        "trust_pre_8_C_to_B",
    ]

    @staticmethod
    def is_displayed(player: Player):
        return (
            not player.participant.kicked
            and player.round_number == 1
            and player.participant.kicked == False
            and player.participant.leftover == False
            and player.position == "C"
        )

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config["timeout_time"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if timeout_happened:
            participant.kicked = True
        leftover_check(player)


class NewRound(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return vars_for_template(player)

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if (
            participant.end_game == False
            and player.round_number > 1
            and participant.kicked == False
            and participant.leftover == False
        ):
            return True
        else:
            return False

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        group = player.group

        # Re-assign treatment condition from previous round 
        prev_round_group = group.in_round(
            group.round_number - 1
        )  # Retrieve value from group object from the previous round
        group.is_experimental = (
            prev_round_group.is_experimental
        )  # Set value for current group object

        for player in group.get_players():
            prev_player = player.in_round(1)
            player.position = prev_player.position
            player.resources = prev_player.resources
            player.completion_code = prev_player.completion_code

        leftover_check(player)
        if timeout_happened:
            participant.kicked = True

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config["timeout_time"]


class PhaseI(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return vars_for_template(player)

    form_model = "player"
    form_fields = [
        "proposed_coalition",
        "allocate_to_player_A",
        "allocate_to_player_B",
        "allocate_to_player_C",
    ]

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if (
            participant.end_game == False
            and participant.kicked == False
            and participant.leftover == False
        ):
            return True
        else:
            return False

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        group = player.group
        for p in group.get_players():
            try:
                p.proposed_coalition
            except:
                p.proposed_coalition = ""
                p.allocate_to_player_A = 0
                p.allocate_to_player_B = 0
                p.allocate_to_player_C = 0

            if p.proposed_coalition == "BC":
                p.allocate_to_player_A = 0
            if p.proposed_coalition == "AC":
                p.allocate_to_player_B = 0
            if p.proposed_coalition == "AB":
                p.allocate_to_player_C = 0
            if p.position == "A":
                group.proposed_coalition_player_A = p.proposed_coalition
                try:
                    group.allocation_A_to_A = p.allocate_to_player_A
                except:
                    group.allocation_A_to_A = 0
                try:
                    group.allocation_A_to_B = p.allocate_to_player_B
                except:
                    group.allocation_A_to_B = 0
                try:
                    group.allocation_A_to_C = p.allocate_to_player_C
                except:
                    group.allocation_A_to_C = 0
            elif p.position == "B":
                group.proposed_coalition_player_B = p.proposed_coalition
                try:
                    group.allocation_B_to_A = p.allocate_to_player_A
                except:
                    group.allocation_B_to_A = 0
                try:
                    group.allocation_B_to_B = p.allocate_to_player_B
                except:
                    group.allocation_B_to_B = 0
                try:
                    group.allocation_B_to_C = p.allocate_to_player_C
                except:
                    group.allocation_B_to_C = 0
            elif p.position == "C":
                group.proposed_coalition_player_C = p.proposed_coalition
                try:
                    group.allocation_C_to_A = p.allocate_to_player_A
                except:
                    group.allocation_C_to_A = 0
                try:
                    group.allocation_C_to_B = p.allocate_to_player_B
                except:
                    group.allocation_C_to_B = 0
                try:
                    group.allocation_C_to_C = p.allocate_to_player_C
                except:
                    group.allocation_C_to_C = 0
        if timeout_happened:
            participant.kicked = True
        leftover_check(player)

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config["timeout_time"]


class WaitForOffers(WaitPage):
    title_text = "Waiting for offers from other participants"
    body_text = (
        "Wait until all participants have submitted offers. This may take some time."
    )
    startwp_timer = 5 * 60

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if (
            participant.end_game == False
            and participant.kicked == False
            and participant.leftover == False
        ):
            return True
        else:
            return False

    def after_all_players_arrive(group: Group):
        # If any of the players are arrived the wait page without a proposed coalition, assign others to leftovers
        for player in group.get_players():
            if player.participant.kicked:
                # Assign other players to leftovers
                other_players = player.get_others_in_group()
                for other_player in other_players:
                    other_player.participant.leftover = True


class PhaseII(Page):
    form_model = "player"
    form_fields = ["selected_coalition"]

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if (
            participant.end_game == False
            and participant.kicked == False
            and participant.leftover == False
        ):
            return True
        else:
            return False

    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        group = player.group
        vars = vars_for_template(player)
        offers = dict()
        for p in group.get_players():
            pc = p.proposed_coalition
            if pc and player.position in p.proposed_coalition:
                summary = (
                    pc,
                    offer_summary(p),
                    p.allocate_to_player_A,
                    p.allocate_to_player_B,
                    p.allocate_to_player_C,
                    p.id_in_group,
                )
                summary_wo_id = summary[:-1]
                offers[summary_wo_id] = summary

        vars.update({"offers": sorted(offers.values())})
        return vars

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config["timeout_time"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if timeout_happened:
            participant.kicked = True
        leftover_check(player)


class WaitForSelection(WaitPage):
    title_text = "Waiting for selection"
    body_text = (
        "Wait until all participants have chosen a proposal. This may take some time."
    )
    startwp_timer = 5 * 60

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if (
            participant.end_game == False
            and participant.grouped == True
            and participant.kicked == False
            and participant.leftover == False
        ):
            return True
        else:
            return False

    @staticmethod
    def after_all_players_arrive(group: Group):

        validity_status = True
        # If any of the players are arrived the wait page without a proposed coalition, assign others to leftovers
        for player in group.get_players():
        
            if player.field_maybe_none('selected_coalition') is None: 
                player.selected_coalition = ""
        
            if player.selected_coalition == "":
                # Assign other players to leftovers
                other_players = player.get_others_in_group()
                for other_player in other_players:
                    other_player.participant.leftover = True
                    validity_status = False

                    # Assign all coalition related variables to default values if the coalition is not valid
                    group.proposed_coalition_player_A = ""
                    group.proposed_coalition_player_B = ""
                    group.proposed_coalition_player_C = ""
                    group.allocation_A_to_A = 0
                    group.allocation_A_to_B = 0
                    group.allocation_A_to_C = 0
                    group.allocation_B_to_A = 0
                    group.allocation_B_to_B = 0
                    group.allocation_B_to_C = 0
                    group.allocation_C_to_A = 0
                    group.allocation_C_to_B = 0
                    group.allocation_C_to_C = 0
                    group.selected_coalition_name_player_A = ""
                    group.selected_coalition_name_player_B = ""
                    group.selected_coalition_name_player_C = ""
                    group.selected_coalition_allocation_A_player_A = 0
                    group.selected_coalition_allocation_B_player_A = 0
                    group.selected_coalition_allocation_C_player_A = 0
                    group.selected_coalition_allocation_A_player_B = 0
                    group.selected_coalition_allocation_B_player_B = 0
                    group.selected_coalition_allocation_C_player_B = 0
                    group.selected_coalition_allocation_A_player_C = 0
                    group.selected_coalition_allocation_B_player_C = 0
                    group.selected_coalition_allocation_C_player_C = 0

        # If the all players arrive this point without any problems
        if validity_status:

            session = group.session
            players = group.get_players()

            for p in players:

                cs = p.selected_coalition
                p.selected_coalition_name = group.get_player_by_id(
                    cs
                ).proposed_coalition
                p.selected_coalition_allocation_A = group.get_player_by_id(
                    cs
                ).allocate_to_player_A
                p.selected_coalition_allocation_B = group.get_player_by_id(
                    cs
                ).allocate_to_player_B
                p.selected_coalition_allocation_C = group.get_player_by_id(
                    cs
                ).allocate_to_player_C

                if p.position == "A":
                    group.selected_coalition_name_player_A = p.selected_coalition_name
                    group.selected_coalition_allocation_A_player_A = (
                        p.selected_coalition_allocation_A
                    )
                    group.selected_coalition_allocation_B_player_A = (
                        p.selected_coalition_allocation_B
                    )
                    group.selected_coalition_allocation_C_player_A = (
                        p.selected_coalition_allocation_C
                    )
                elif p.position == "B":
                    group.selected_coalition_name_player_B = p.selected_coalition_name
                    group.selected_coalition_allocation_A_player_B = (
                        p.selected_coalition_allocation_A
                    )
                    group.selected_coalition_allocation_B_player_B = (
                        p.selected_coalition_allocation_B
                    )
                    group.selected_coalition_allocation_C_player_B = (
                        p.selected_coalition_allocation_C
                    )
                elif p.position == "C":
                    group.selected_coalition_name_player_C = p.selected_coalition_name
                    group.selected_coalition_allocation_A_player_C = (
                        p.selected_coalition_allocation_A
                    )
                    group.selected_coalition_allocation_B_player_C = (
                        p.selected_coalition_allocation_B
                    )
                    group.selected_coalition_allocation_C_player_C = (
                        p.selected_coalition_allocation_C
                    )
            list_AB = []
            list_AC = []
            list_BC = []
            list_ABC = []
            for p in players:
                if p.selected_coalition_name == "AB":
                    list_AB.append(p.position)
                if p.selected_coalition_name == "AC":
                    list_AC.append(p.position)
                if p.selected_coalition_name == "BC":
                    list_BC.append(p.position)
                if p.selected_coalition_name == "ABC":
                    list_ABC.append(p.position)

            if (
                len(list_AB) == 2
                and group.selected_coalition_allocation_A_player_A
                == group.selected_coalition_allocation_A_player_B
            ):
                if (
                    group.selected_coalition_allocation_B_player_A
                    == group.selected_coalition_allocation_B_player_B
                ):
                    group.coalition_formed = True
                    group.formed_coalition_name = "AB"
                    group.payoff_A = group.selected_coalition_allocation_A_player_A
                    group.payoff_B = group.selected_coalition_allocation_B_player_B
                    group.payoff_C = 0
            elif (
                len(list_AC) == 2
                and group.selected_coalition_allocation_A_player_A
                == group.selected_coalition_allocation_A_player_C
            ):
                if (
                    group.selected_coalition_allocation_C_player_A
                    == group.selected_coalition_allocation_C_player_C
                ):
                    group.coalition_formed = True
                    group.formed_coalition_name = "AC"
                    group.payoff_A = group.selected_coalition_allocation_A_player_A
                    group.payoff_B = 0
                    group.payoff_C = group.selected_coalition_allocation_C_player_C
            elif (
                len(list_BC) == 2
                and group.selected_coalition_allocation_B_player_B
                == group.selected_coalition_allocation_B_player_C
            ):
                if (
                    group.selected_coalition_allocation_C_player_B
                    == group.selected_coalition_allocation_C_player_C
                ):
                    group.coalition_formed = True
                    group.formed_coalition_name = "BC"
                    group.payoff_A = 0
                    group.payoff_B = group.selected_coalition_allocation_B_player_B
                    group.payoff_C = group.selected_coalition_allocation_C_player_C
            elif (
                len(list_ABC) == 3
                and group.selected_coalition_allocation_A_player_A
                == group.selected_coalition_allocation_A_player_B
                == group.selected_coalition_allocation_A_player_C
            ):
                if (
                    group.selected_coalition_allocation_B_player_A
                    == group.selected_coalition_allocation_B_player_B
                    == group.selected_coalition_allocation_B_player_C
                ):
                    if (
                        group.selected_coalition_allocation_C_player_A
                        == group.selected_coalition_allocation_C_player_B
                        == group.selected_coalition_allocation_C_player_C
                    ):
                        group.coalition_formed = True
                        group.formed_coalition_name = "ABC"
                        group.payoff_A = group.selected_coalition_allocation_A_player_A
                        group.payoff_B = group.selected_coalition_allocation_B_player_B
                        group.payoff_C = group.selected_coalition_allocation_C_player_C
            else:
                group.coalition_formed = False
                group.payoff_A = 0
                group.payoff_B = 0
                group.payoff_C = 0
            for p in players:
                if p.position == "A":
                    p.money = group.payoff_A
                    p.payoff = group.payoff_A * session.config["payoff_conversion"]
                if p.position == "B":
                    p.money = group.payoff_B
                    p.payoff = group.payoff_B * session.config["payoff_conversion"]
                if p.position == "C":
                    p.money = group.payoff_C
                    p.payoff = group.payoff_C * session.config["payoff_conversion"]


class PhaseIII_Success(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        group = player.group
        try:
            group.coalition_formed
        except:
            group.coalition_formed = 0
        if (
            participant.end_game == False
            and group.coalition_formed == 1
            and participant.kicked == False
            and participant.leftover == False
        ):
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
        leftover_check(player)

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        offers_dict = dict()
        vars = vars_for_template(player)
        prop_name_A = group.proposed_coalition_player_A
        prop_name_B = group.proposed_coalition_player_B
        prop_name_C = group.proposed_coalition_player_C
        prop_A_to_A = group.allocation_A_to_A
        prop_A_to_B = group.allocation_A_to_B
        prop_A_to_C = group.allocation_A_to_C
        prop_B_to_A = group.allocation_B_to_A
        prop_B_to_B = group.allocation_B_to_B
        prop_B_to_C = group.allocation_B_to_C
        prop_C_to_A = group.allocation_C_to_A
        prop_C_to_B = group.allocation_C_to_B
        prop_C_to_C = group.allocation_C_to_C
        sel_name_A = group.selected_coalition_name_player_A
        sel_name_B = group.selected_coalition_name_player_B
        sel_name_C = group.selected_coalition_name_player_C
        sel_A_to_A = group.selected_coalition_allocation_A_player_A
        sel_A_to_B = group.selected_coalition_allocation_B_player_A
        sel_A_to_C = group.selected_coalition_allocation_C_player_A
        sel_B_to_A = group.selected_coalition_allocation_A_player_B
        sel_B_to_B = group.selected_coalition_allocation_B_player_B
        sel_B_to_C = group.selected_coalition_allocation_C_player_B
        sel_C_to_A = group.selected_coalition_allocation_A_player_C
        sel_C_to_B = group.selected_coalition_allocation_B_player_C
        sel_C_to_C = group.selected_coalition_allocation_C_player_C
        proposed_by_A = 0
        proposed_by_B = 0
        proposed_by_C = 0
        selected_by_A = 0
        selected_by_B = 0
        selected_by_C = 0
        offer_A = [
            group.proposed_coalition_player_A,
            group.allocation_A_to_A,
            group.allocation_A_to_B,
            group.allocation_A_to_C,
            proposed_by_A,
            proposed_by_B,
            proposed_by_C,
            selected_by_A,
            selected_by_B,
            selected_by_C,
        ]
        offer_B = [
            group.proposed_coalition_player_B,
            group.allocation_B_to_A,
            group.allocation_B_to_B,
            group.allocation_B_to_C,
            proposed_by_A,
            proposed_by_B,
            proposed_by_C,
            selected_by_A,
            selected_by_B,
            selected_by_C,
        ]
        offer_C = [
            group.proposed_coalition_player_C,
            group.allocation_C_to_A,
            group.allocation_C_to_B,
            group.allocation_C_to_C,
            proposed_by_A,
            proposed_by_B,
            proposed_by_C,
            selected_by_A,
            selected_by_B,
            selected_by_C,
        ]
        offers = (offer_A, offer_B, offer_C)
        for offer in offers:
            if (
                offer[0] == prop_name_A
                and offer[1] == prop_A_to_A
                and offer[2] == prop_A_to_B
                and offer[3] == prop_A_to_C
            ):
                offer[4] = 1
            if (
                offer[0] == prop_name_B
                and offer[1] == prop_B_to_A
                and offer[2] == prop_B_to_B
                and offer[3] == prop_B_to_C
            ):
                offer[5] = 1
            if (
                offer[0] == prop_name_C
                and offer[1] == prop_C_to_A
                and offer[2] == prop_C_to_B
                and offer[3] == prop_C_to_C
            ):
                offer[6] = 1
            if (
                offer[0] == sel_name_A
                and offer[1] == sel_A_to_A
                and offer[2] == sel_A_to_B
                and offer[3] == sel_A_to_C
            ):
                offer[7] = 1
            if (
                offer[0] == sel_name_B
                and offer[1] == sel_B_to_A
                and offer[2] == sel_B_to_B
                and offer[3] == sel_B_to_C
            ):
                offer[8] = 1
            if (
                offer[0] == sel_name_C
                and offer[1] == sel_C_to_A
                and offer[2] == sel_C_to_B
                and offer[3] == sel_C_to_C
            ):
                offer[9] = 1
            offer_dict = (
                offer[0],
                offer[1],
                offer[2],
                offer[3],
                offer[4],
                offer[5],
                offer[6],
                offer[7],
                offer[8],
                offer[9],
            )
            offers_dict[offer_dict] = offer_dict
        vars.update({"offers_dictionary": sorted(offers_dict.values())})
        return vars

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        session = player.session
        group = player.group
        for p in group.get_players():
            if p.position == "A":
                p.payoff = group.payoff_A * session.config["payoff_conversion"]
            if p.position == "B":
                p.payoff = group.payoff_B * session.config["payoff_conversion"]
            if p.position == "C":
                p.payoff = group.payoff_C * session.config["payoff_conversion"]


class Payoff(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        group = player.group
        if (
            participant.end_game == False
            and group.coalition_formed == True
            and participant.kicked == False
            and participant.leftover == False
        ):
            return True
        else:
            return False

    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        vars = vars_for_template(player)
        timers = session.config["timers"]
        vars.update({"timers": timers})
        return vars


class PhaseIII_Failure(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        group = player.group
        if (
            participant.end_game == False
            and group.coalition_formed == False
            and participant.kicked == False
            and participant.leftover == False
        ):
            return True
        else:
            return False

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        offers_dict = dict()
        vars = vars_for_template(player)
        prop_name_A = group.proposed_coalition_player_A
        prop_name_B = group.proposed_coalition_player_B
        prop_name_C = group.proposed_coalition_player_C
        prop_A_to_A = group.allocation_A_to_A
        prop_A_to_B = group.allocation_A_to_B
        prop_A_to_C = group.allocation_A_to_C
        prop_B_to_A = group.allocation_B_to_A
        prop_B_to_B = group.allocation_B_to_B
        prop_B_to_C = group.allocation_B_to_C
        prop_C_to_A = group.allocation_C_to_A
        prop_C_to_B = group.allocation_C_to_B
        prop_C_to_C = group.allocation_C_to_C
        sel_name_A = group.selected_coalition_name_player_A
        sel_name_B = group.selected_coalition_name_player_B
        sel_name_C = group.selected_coalition_name_player_C
        sel_A_to_A = group.selected_coalition_allocation_A_player_A
        sel_A_to_B = group.selected_coalition_allocation_B_player_A
        sel_A_to_C = group.selected_coalition_allocation_C_player_A
        sel_B_to_A = group.selected_coalition_allocation_A_player_B
        sel_B_to_B = group.selected_coalition_allocation_B_player_B
        sel_B_to_C = group.selected_coalition_allocation_C_player_B
        sel_C_to_A = group.selected_coalition_allocation_A_player_C
        sel_C_to_B = group.selected_coalition_allocation_B_player_C
        sel_C_to_C = group.selected_coalition_allocation_C_player_C
        proposed_by_A = 0
        proposed_by_B = 0
        proposed_by_C = 0
        selected_by_A = 0
        selected_by_B = 0
        selected_by_C = 0
        offer_A = [
            group.proposed_coalition_player_A,
            group.allocation_A_to_A,
            group.allocation_A_to_B,
            group.allocation_A_to_C,
            proposed_by_A,
            proposed_by_B,
            proposed_by_C,
            selected_by_A,
            selected_by_B,
            selected_by_C,
        ]
        offer_B = [
            group.proposed_coalition_player_B,
            group.allocation_B_to_A,
            group.allocation_B_to_B,
            group.allocation_B_to_C,
            proposed_by_A,
            proposed_by_B,
            proposed_by_C,
            selected_by_A,
            selected_by_B,
            selected_by_C,
        ]
        offer_C = [
            group.proposed_coalition_player_C,
            group.allocation_C_to_A,
            group.allocation_C_to_B,
            group.allocation_C_to_C,
            proposed_by_A,
            proposed_by_B,
            proposed_by_C,
            selected_by_A,
            selected_by_B,
            selected_by_C,
        ]
        offers = (offer_A, offer_B, offer_C)
        for offer in offers:
            if (
                offer[0] == prop_name_A
                and offer[1] == prop_A_to_A
                and offer[2] == prop_A_to_B
                and offer[3] == prop_A_to_C
            ):
                offer[4] = 1
            if (
                offer[0] == prop_name_B
                and offer[1] == prop_B_to_A
                and offer[2] == prop_B_to_B
                and offer[3] == prop_B_to_C
            ):
                offer[5] = 1
            if (
                offer[0] == prop_name_C
                and offer[1] == prop_C_to_A
                and offer[2] == prop_C_to_B
                and offer[3] == prop_C_to_C
            ):
                offer[6] = 1
            if (
                offer[0] == sel_name_A
                and offer[1] == sel_A_to_A
                and offer[2] == sel_A_to_B
                and offer[3] == sel_A_to_C
            ):
                offer[7] = 1
            if (
                offer[0] == sel_name_B
                and offer[1] == sel_B_to_A
                and offer[2] == sel_B_to_B
                and offer[3] == sel_B_to_C
            ):
                offer[8] = 1
            if (
                offer[0] == sel_name_C
                and offer[1] == sel_C_to_A
                and offer[2] == sel_C_to_B
                and offer[3] == sel_C_to_C
            ):
                offer[9] = 1
            offer_dict = (
                offer[0],
                offer[1],
                offer[2],
                offer[3],
                offer[4],
                offer[5],
                offer[6],
                offer[7],
                offer[8],
                offer[9],
            )
            offers_dict[offer_dict] = offer_dict
        vars.update({"offers_dictionary": sorted(offers_dict.values())})
        return vars

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config["timeout_time"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if timeout_happened:
            participant.kicked = True
        leftover_check(player)


class T3_A(Page):
    """
    Trust measurement page after the negotiation ends. The descriptions change according to the condition. Specific to each player.
    """

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        subsession = player.subsession
        group = player.group
        if (
            participant.end_game == False
            and group.coalition_formed == True
            and participant.kicked == False
            and participant.leftover == False
            and player.position == "A"
        ):
            return True
        elif (
            subsession.round_number == C.NUM_ROUNDS
            and participant.end_game == False
            and participant.kicked == False
            and participant.leftover == False
            and player.position == "A"
        ):
            return True
        else:
            return False

    form_model = "player"
    form_fields = [
        "trust_aft_1_A_to_B",
        "trust_aft_2_A_to_B",
        "trust_aft_3_A_to_B",
        "trust_aft_4_A_to_B",
        "trust_aft_5_A_to_B",
        "trust_aft_6_A_to_B",
        "trust_aft_7_A_to_B",
        "trust_aft_8_A_to_B",
        "trust_aft_1_A_to_C",
        "trust_aft_2_A_to_C",
        "trust_aft_3_A_to_C",
        "trust_aft_4_A_to_C",
        "trust_aft_5_A_to_C",
        "trust_aft_6_A_to_C",
        "trust_aft_7_A_to_C",
        "trust_aft_8_A_to_C",
    ]


class T3_B(Page):
    """
    Trust measurement page after the negotiation ends. The descriptions change according to the condition. Specific to each player.
    """

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        subsession = player.subsession
        group = player.group
        if (
            participant.end_game == False
            and group.coalition_formed == True
            and participant.kicked == False
            and participant.leftover == False
            and player.position == "B"
        ):
            return True
        elif (
            subsession.round_number == C.NUM_ROUNDS
            and participant.end_game == False
            and participant.kicked == False
            and participant.leftover == False
            and player.position == "B"
        ):
            return True
        else:
            return False

    form_model = "player"
    form_fields = [
        "trust_aft_1_B_to_A",
        "trust_aft_2_B_to_A",
        "trust_aft_3_B_to_A",
        "trust_aft_4_B_to_A",
        "trust_aft_5_B_to_A",
        "trust_aft_6_B_to_A",
        "trust_aft_7_B_to_A",
        "trust_aft_8_B_to_A",
        "trust_aft_1_B_to_C",
        "trust_aft_2_B_to_C",
        "trust_aft_3_B_to_C",
        "trust_aft_4_B_to_C",
        "trust_aft_5_B_to_C",
        "trust_aft_6_B_to_C",
        "trust_aft_7_B_to_C",
        "trust_aft_8_B_to_C",
    ]


class T3_C(Page):
    """
    Trust measurement page after the negotiation ends. The descriptions change according to the condition. Specific to each player.
    """

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        subsession = player.subsession
        group = player.group
        if (
            participant.end_game == False
            and group.coalition_formed == True
            and participant.kicked == False
            and participant.leftover == False
            and player.position == "C"
        ):
            return True
        elif (
            subsession.round_number == C.NUM_ROUNDS
            and participant.end_game == False
            and participant.kicked == False
            and participant.leftover == False
            and player.position == "C"
        ):
            return True
        else:
            return False

    form_model = "player"
    form_fields = [
        "trust_aft_1_C_to_A",
        "trust_aft_2_C_to_A",
        "trust_aft_3_C_to_A",
        "trust_aft_4_C_to_A",
        "trust_aft_5_C_to_A",
        "trust_aft_6_C_to_A",
        "trust_aft_7_C_to_A",
        "trust_aft_8_C_to_A",
        "trust_aft_1_C_to_B",
        "trust_aft_2_C_to_B",
        "trust_aft_3_C_to_B",
        "trust_aft_4_C_to_B",
        "trust_aft_5_C_to_B",
        "trust_aft_6_C_to_B",
        "trust_aft_7_C_to_B",
        "trust_aft_8_C_to_B",
    ]


class Leftover(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if (
            participant.grouped == False
            and participant.kicked == False
            and participant.end_game == False
            and player.round_number == 1
        ):
            return True
        elif (
            participant.leftover == True
            and participant.kicked == False
            and participant.end_game == False
            and player.round_number == 1
        ):
            return True
        elif (
            player.round_number == C.NUM_ROUNDS
            and participant.end_game == False
            and participant.leftover == True
            and participant.kicked == False
        ):
            return True
        else:
            return False

    @staticmethod
    def vars_for_template(player: Player):
        return vars_for_template(player)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        participant.leftover = True


class LastQuestions(Page):
    """
    Only for leftover participants, for a graceful ending.
    """

    form_model = "player"
    form_fields = [
        "competition",
        "gen_trust_1",
        "gen_trust_2",
        "gen_trust_3",
        "gen_trust_4",
    ]

    @staticmethod
    def is_displayed(player: Player):

        if (
            not player.participant.kicked
            and player.round_number == 1
            and player.participant.kicked == False
            and player.participant.leftover == True
        ):
            return True
        elif (
            player.round_number == C.NUM_ROUNDS
            and player.participant.end_game == False
            and player.participant.leftover == True
            and player.participant.kicked == False
        ):
            return True
        else:
            return False


class Funnel(Page):
    form_model = "player"
    form_fields = ["comment"]

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        subsession = player.subsession
        group = player.group
        if (
            participant.end_game == False
            and group.coalition_formed == True
            and participant.kicked == False
            and participant.leftover == False
        ):
            return True
        elif subsession.round_number == C.NUM_ROUNDS and participant.end_game == False:
            return True
        elif (
            participant.leftover == True
            and participant.kicked == False
            and participant.end_game == False
            and player.round_number == 1
        ):
            return True
        else:
            return False


class Debriefing(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        subsession = player.subsession
        group = player.group
        if (
            participant.end_game == False
            and group.coalition_formed == True
            and participant.kicked == False
            and participant.leftover == False
        ):
            return True
        elif subsession.round_number == C.NUM_ROUNDS and participant.end_game == False:
            return True
        elif (
            participant.leftover == True
            and participant.kicked == False
            and participant.end_game == False
            and player.round_number == 1
        ):
            return True
        else:
            return False

    def before_next_page(player: Player):
        participant = player.participant
        participant.end_game = True


class ID(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        subsession = player.subsession
        group = player.group
        if (
            participant.end_game == False
            and group.coalition_formed == True
            and participant.kicked == False
        ):
            return True
        elif (
            subsession.round_number == C.NUM_ROUNDS
            and participant.end_game == False
            and participant.kicked == False
        ):
            return True
        elif (
            participant.leftover == True
            and participant.kicked == False
            and participant.end_game == False
        ):
            return True
        else:
            return False

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        participant.end_game = True


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
    Waitforgroup,
    Groupingconfirmation,
    Waitforparticipants,
    SVO_Assigned,
    AssignedPosition,
    AssignedPosition2,
    ComprehensionCheck,
    ComprehensionCheck1,
    ComprehensionCheck2,
    ComprehensionCheck3,
    T2_A,
    T2_B,
    T2_C,
    NewRound,
    PhaseI,
    WaitForOffers,
    PhaseII,
    WaitForSelection,
    PhaseIII_Success,
    Payoff,
    PhaseIII_Failure,
    T3_A,
    T3_B,
    T3_C,
    Leftover,
    LastQuestions,
    Funnel,
    Debriefing,
    Kicked,
]
