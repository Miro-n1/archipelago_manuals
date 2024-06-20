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

#class Victory(Choice):
#    """Choose the victory condition."""
#    display_name = "Victory condition"
#    option_wisp_hunt = 1
#    option_2 = 2
#    default = 1

class WispsTotal(Range):
    """Choose the number of Spiritomb wisps (macguffin hunt goal item) in the pool.
    This gets reduced automatically if there are too few locations due to fish_locations."""
    display_name = "Number of wisps in the pool"
    range_start = 1
    range_end = 108
    default = 108

class WispsRequired(Range):
    """Choose the number of Spiritomb wisps required to win.
    If this is set higher than wisps_total, it is reduced to match."""
    display_name = "Number of wisps required to win"
    range_start = 1
    range_end = 108
    default = 100

class Fishing(Choice):
    """For themed multiworlds: Choose if non-fish, fish and fish-related locations are active.
    Wisp maximum per setting, listed with / without alpha_locations:
    all: 108 / 108
    only_not_fish: 108 / 97
    only_fish_and_related: 16 / 10. May precollect some items to free up locations.
    only_fish: 13 / 7. Precollects more items to free up locations."""
    display_name = "Fish locations"
    option_all = 1
    option_only_not_fish = 2
    option_only_fish_and_related = 3
    option_only_fish = 4
    default = 1

class AlphaLocations(Toggle): #add setting for only alpha?
    """Enable locations for each static alpha Pokémon."""
    display_name = "Alpha locations"
    default = True

class ShinyLocations(Range):
    """Set the number of shiny locations in the pool, logically locked by shiny charm fragments.
    Not recommended with location count reduced by fishing mode. May require grinding, recommended: 5."""
    display_name = "Number of AP assignments"
    range_start = 0
    range_end = 10
    default = 0
    option_5 = 1

# This is called before any manual options are defined, in case you want to define your own with a clean slate or let Manual define over them
def before_options_defined(options: dict) -> dict:
    options["wisps_total"] = WispsTotal
    options["wisps_required"] = WispsRequired
    options["fish_locations"] = Fishing
    options["alpha_locations"] = AlphaLocations
    options["shiny_locations"] = ShinyLocations
    return options

# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: dict) -> dict:
    return options