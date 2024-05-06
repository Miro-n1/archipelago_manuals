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

class ApAssignments(Range):
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

# This is called before any manual options are defined, in case you want to define your own with a clean slate or let Manual define over them
def before_options_defined(options: dict) -> dict:
    options["ap_assignments"] = ApAssignments
    options["easy_start"] = EasyStart
    options["nitra_remaining"] = NitraRemaining
    return options

# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: dict) -> dict:
    return options