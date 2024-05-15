# Object classes from AP that represent different types of options that you can create
from Options import FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, NamedRange

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value



####################################################################
# NOTE: At the time that options are created, Manual has no concept of the multiworld or its own world.
#       Options are defined before the world is even created.
#
# Example of creating your own option:
#
#   class MakeThePlayerOP(Toggle):
#       """Should the player be overpowered? Probably not, but you can choose for this to do... something!"""
#       display_name = "Make me OP"
#
#   options["make_op"] = MakeThePlayerOP
#
#
# Then, to see if the option is set, you can call is_option_enabled or get_option_value.
#####################################################################


# To add an option, use the before_options_defined hook below and something like this:
#   options["total_characters_to_win_with"] = TotalCharactersToWinWith

class Mode(Toggle):
    """Choose the game mode.
    Short (True): 4-8 assignments with weapon and equipment upgrades for difficulty logic. Skill based logic skips.
    Long (False): 4-32 missions without difficulty logic. Items unlock missions, similar to muse dash songs."""
    display_name = "Game mode short"
    default = True

class AssignmentCount(Range):
    """Choose the number of different assignments to complete."""
    display_name = "Number of AP assignments"
    range_start = 4
    range_end = 8
    default = 4

class EasyStart(Toggle):
    """Start with a unlocked secondary weapon, traversal tool and special equipment."""
    display_name = "Easy Start"

class NitraRemaining(Toggle):
    """Unlock checks with amount of Nitra remaining at the end of the mission, instead of with the amount of Nitra mined (resupplies called)."""
    display_name = "Remaining Nitra Checks"

class MissionCount(Range):
    """Choose the number of missions in the pool. Complete pool: 8 mission types * 4 classes = 32."""
    display_name = "Number of missions"
    range_start = 4
    range_end = 32
    default = 16

class StartingMissionCount(Range):
    """Choose the number of starting missions."""
    display_name = "Number of starting missions"
    range_start = 0
    range_end = 16
    default = 4

class long_mission_completions_to_win(Range):
    """Choose the number of mission completions required for victory."""
    display_name = "Number of missions to win"
    range_start = 4
    range_end = 32
    default = 16

#class long_trophies_count(Range):
    #"""Choose the number of trophies in the item pool."""
    #display_name = "Number of trophies"
    #range_start = 0
    #range_end = 32
    #default = 0

#class long_trophies_to_win(Range):
    #"""Choose the number of trophies required for victory."""
    #display_name = "Number of trophies to win"
    #range_start = 0
    #range_end = 32
    #default = 0

class SecondaryObjectives(Toggle):
    """Adds locations for 8 secondary objectives."""
    display_name = "Secondary objectives"
    default = True

class Warnings(Toggle):
    """Adds locations for 13 warning mutators."""
    display_name = "Warnings"

class Anomalies(Toggle):
    """Adds locations for 8 anomaly mutators."""
    display_name = "Anomalies"

class DeepDiveCount(Range):
    """Choose the number of deep dives to complete.
    Deep dive seeds refresh weekly."""
    display_name = "Number of deep dives"
    range_start = 0
    range_end = 4
    default = 1

class EliteDeepDiveCount(Range):
    """Choose the number of elite deep dives to complete.
    Deep dive seeds refresh weekly."""
    display_name = "Number of elite deep dives"
    range_start = 0
    range_end = 4
    default = 0

class WeeklyAssignmentCount(Range):
    """Choose the number of weekly priority assignments and weekly core hunts to complete.
    The assignments refresh weekly, consider the planned async length."""
    display_name = "Number of weekly assignments"
    range_start = 0
    range_end = 4
    default = 0

class SeasonChallengeCount(Range):
    """Choose the number of season challenges to complete.
    These refresh daily and require you to complete multiple missions each, 
    so consider the planned async length. Recommended: not more than 1/4 of mission count."""
    display_name = "Number of season challenges"
    range_start = 0
    range_end = 30
    default = 0

# This is called before any manual options are defined, in case you want to define your own with a clean slate or let Manual define over them
def before_options_defined(options: dict) -> dict:
    options["game_mode_short"] = Mode
    options["short_assignment_count"] = AssignmentCount
    options["short_easy_start"] = EasyStart
    options["short_nitra_remaining"] = NitraRemaining
    options["long_mission_count"] = MissionCount
    options["long_starting_mission_count"] = StartingMissionCount
    options["long_mission_completions_to_win"] = long_mission_completions_to_win
    options["long_secondary_objectives"] = SecondaryObjectives
    options["long_warnings"] = Warnings
    options["long_anomalies"] = Anomalies
    options["long_deep_dive_count"] = DeepDiveCount
    options["long_elite_deep_dive_count"] = EliteDeepDiveCount
    options["long_weekly_assignment_count"] = WeeklyAssignmentCount
    options["long_season_callenge_count"] = SeasonChallengeCount
    return options

# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: dict) -> dict:
    return options