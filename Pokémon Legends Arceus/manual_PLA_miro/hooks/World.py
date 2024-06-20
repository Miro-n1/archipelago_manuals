# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from worlds.AutoWorld import World
from BaseClasses import MultiWorld, CollectionState

# Object classes from Manual -- extending AP core -- representing items and locations that are used in generation
from ..Items import ManualItem
from ..Locations import ManualLocation

# Raw JSON data from the Manual apworld, respectively:
#          data/game.json, data/items.json, data/locations.json, data/regions.json
#
from ..Data import game_table, item_table, location_table, region_table

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value

# calling logging.info("message") anywhere below in this file will output the message to both console and log file
import logging

########################################################################################
## Order of method calls when the world generates:
##    1. create_regions - Creates regions and locations
##    2. create_items - Creates the item pool
##    3. set_rules - Creates rules for accessing regions and locations
##    4. generate_basic - Runs any post item pool options, like place item/category
##    5. pre_fill - Creates the victory location
##
## The create_item method is used by plando and start_inventory settings to create an item from an item name.
## The fill_slot_data method will be used to send data to the Manual client for later use, like deathlink.
########################################################################################



# Called before regions and locations are created. Not clear why you'd want this, but it's here. Victory location is included, but Victory event is not placed yet.
def before_create_regions(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after regions and locations are created, in case you want to see or modify that information. Victory location is included.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to remove locations from the world
    locationNamesToRemove = []

    fish_locations = get_option_value(multiworld, player, "fish_locations") #all = 1, only_not_fish = 2, only_fish_and_related = 3, only_fish = 4
    alpha_locations = get_option_value(multiworld, player, "alpha_locations") #85 locations (n65/a6/f14), all filler
    shiny_locations = get_option_value(multiworld, player, "shiny_locations") #0-10 locations + items, no filler

    #Choose which locations to remove for fishing mode:
    if fish_locations == 2:
        #locationNamesToRemove += [loc["name"] for loc in location_table if "fish" or "fishadjacent" in loc.get("category", [])]
        locationNamesToRemove += world.location_name_groups["fish"]
        locationNamesToRemove += world.location_name_groups["fishadjacent"]
    if fish_locations == 3:
        locationNamesToRemove += world.location_name_groups["notfish"]
    if fish_locations == 4:
        locationNamesToRemove += world.location_name_groups["notfish"]
        locationNamesToRemove += world.location_name_groups["fishadjacent"]

    if not alpha_locations: #Disable alpha locations
        locationNamesToRemove += world.location_name_groups["Alpha Locations"]

    while shiny_locations < 10: #Disable shiny locations
        shiny_locations += 1
        locationNamesToRemove.append(f'Shiny {shiny_locations}')

    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in locationNamesToRemove:
                    region.locations.remove(location)
    if hasattr(multiworld, "clear_location_cache"):
        multiworld.clear_location_cache()

# The item pool before starting items are processed, in case you want to see the raw item pool at that stage
def before_create_items_starting(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:

    #Start inventory:
    start_inventory_items = []
    regions = ["Obsidian Fieldlands (OF)", "Crimson Mirelands (CM)", "Cobalt Coastlands (CC)", "Coronet Highlands (CH)", "Alabaster Icelands (AI)"]
    multiworld.random.shuffle(regions)
    start_inventory_items += [regions[0]]
    base_OF = ["Fieldland Camp (OF)", "Heights Camp (OF)"]
    multiworld.random.shuffle(base_OF)
    start_inventory_items += [base_OF[0]]
    base_CM = ["Mirelands Camp (CM)", "Bogbound Camp (CM)"]
    multiworld.random.shuffle(base_CM)
    start_inventory_items += [base_CM[0]]
    base_CC = ["Beachside Camp (CC)", "Coastland Camp (CC)"]
    multiworld.random.shuffle(base_CC)
    start_inventory_items += [base_CC[0]]
    base_CH = ["Highlands Camp (CH)", "Mountain Camp (CH)", "Summit Camp (CH)"]
    multiworld.random.shuffle(base_CH)
    start_inventory_items += [base_CH[0]]
    base_AI = ["Snowfield Camp (AI)", "Icepeak Camp (AI)"]
    multiworld.random.shuffle(base_AI)
    start_inventory_items += [base_AI[0]]
    progressive_poke_balls = ["Progressive Poké Ball", "Progressive Heavy Ball", "Progressive Feather Ball"]
    multiworld.random.shuffle(progressive_poke_balls)
    start_inventory_items += [progressive_poke_balls[0]]

    #logging.info(f"start_inventory_items: {start_inventory_items}")
    for itemName in start_inventory_items: #precollect items, then delete from item pool.
        start_inventory = next(item for item in item_pool if item.name == itemName)
        multiworld.push_precollected(start_inventory)
        item_pool.remove(start_inventory)

    return item_pool

# The item pool after starting items are processed but before filler is added, in case you want to see the raw item pool at that stage
def before_create_items_filler(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:

    itemNamesToRemove = [] # List of item names
    locationNamesToRemove = ["Repair Odd Keystone with 1 wisp", "Repair Odd Keystone with 2 wisps", "Repair Odd Keystone with 3 wisps", "Repair Odd Keystone with 4 wisps", "Repair Odd Keystone with 5 wisps", "Repair Odd Keystone with 6 wisps", "Repair Odd Keystone with 7 wisps", "Repair Odd Keystone with 8 wisps", "Repair Odd Keystone with 9 wisps", "Repair Odd Keystone with 10 wisps", "Repair Odd Keystone with 11 wisps", "Repair Odd Keystone with 12 wisps", "Repair Odd Keystone with 13 wisps", "Repair Odd Keystone with 14 wisps", "Repair Odd Keystone with 15 wisps", "Repair Odd Keystone with 16 wisps", "Repair Odd Keystone with 17 wisps", "Repair Odd Keystone with 18 wisps", "Repair Odd Keystone with 19 wisps", "Repair Odd Keystone with 20 wisps", "Repair Odd Keystone with 21 wisps", "Repair Odd Keystone with 22 wisps", "Repair Odd Keystone with 23 wisps", "Repair Odd Keystone with 24 wisps", "Repair Odd Keystone with 25 wisps", "Repair Odd Keystone with 26 wisps", "Repair Odd Keystone with 27 wisps", "Repair Odd Keystone with 28 wisps", "Repair Odd Keystone with 29 wisps", "Repair Odd Keystone with 30 wisps", "Repair Odd Keystone with 31 wisps", "Repair Odd Keystone with 32 wisps", "Repair Odd Keystone with 33 wisps", "Repair Odd Keystone with 34 wisps", "Repair Odd Keystone with 35 wisps", "Repair Odd Keystone with 36 wisps", "Repair Odd Keystone with 37 wisps", "Repair Odd Keystone with 38 wisps", "Repair Odd Keystone with 39 wisps", "Repair Odd Keystone with 40 wisps", "Repair Odd Keystone with 41 wisps", "Repair Odd Keystone with 42 wisps", "Repair Odd Keystone with 43 wisps", "Repair Odd Keystone with 44 wisps", "Repair Odd Keystone with 45 wisps", "Repair Odd Keystone with 46 wisps", "Repair Odd Keystone with 47 wisps", "Repair Odd Keystone with 48 wisps", "Repair Odd Keystone with 49 wisps", "Repair Odd Keystone with 50 wisps", "Repair Odd Keystone with 51 wisps", "Repair Odd Keystone with 52 wisps", "Repair Odd Keystone with 53 wisps", "Repair Odd Keystone with 54 wisps", "Repair Odd Keystone with 55 wisps", "Repair Odd Keystone with 56 wisps", "Repair Odd Keystone with 57 wisps", "Repair Odd Keystone with 58 wisps", "Repair Odd Keystone with 59 wisps", "Repair Odd Keystone with 60 wisps", "Repair Odd Keystone with 61 wisps", "Repair Odd Keystone with 62 wisps", "Repair Odd Keystone with 63 wisps", "Repair Odd Keystone with 64 wisps", "Repair Odd Keystone with 65 wisps", "Repair Odd Keystone with 66 wisps", "Repair Odd Keystone with 67 wisps", "Repair Odd Keystone with 68 wisps", "Repair Odd Keystone with 69 wisps", "Repair Odd Keystone with 70 wisps", "Repair Odd Keystone with 71 wisps", "Repair Odd Keystone with 72 wisps", "Repair Odd Keystone with 73 wisps", "Repair Odd Keystone with 74 wisps", "Repair Odd Keystone with 75 wisps", "Repair Odd Keystone with 76 wisps", "Repair Odd Keystone with 77 wisps", "Repair Odd Keystone with 78 wisps", "Repair Odd Keystone with 79 wisps", "Repair Odd Keystone with 80 wisps", "Repair Odd Keystone with 81 wisps", "Repair Odd Keystone with 82 wisps", "Repair Odd Keystone with 83 wisps", "Repair Odd Keystone with 84 wisps", "Repair Odd Keystone with 85 wisps", "Repair Odd Keystone with 86 wisps", "Repair Odd Keystone with 87 wisps", "Repair Odd Keystone with 88 wisps", "Repair Odd Keystone with 89 wisps", "Repair Odd Keystone with 90 wisps", "Repair Odd Keystone with 91 wisps", "Repair Odd Keystone with 92 wisps", "Repair Odd Keystone with 93 wisps", "Repair Odd Keystone with 94 wisps", "Repair Odd Keystone with 95 wisps", "Repair Odd Keystone with 96 wisps", "Repair Odd Keystone with 97 wisps", "Repair Odd Keystone with 98 wisps", "Repair Odd Keystone with 99 wisps", "Repair Odd Keystone with 100 wisps", "Repair Odd Keystone with 101 wisps", "Repair Odd Keystone with 102 wisps", "Repair Odd Keystone with 103 wisps", "Repair Odd Keystone with 104 wisps", "Repair Odd Keystone with 105 wisps", "Repair Odd Keystone with 106 wisps", "Repair Odd Keystone with 107 wisps", "Repair Odd Keystone with 108 wisps"] # List of location names

    # Because multiple copies of an item can exist, you need to add an item name
    # to the list multiple times if you want to remove multiple copies of it.

    wisps_total = get_option_value(multiworld, player, "wisps_total") #1-108
    wisps_required = get_option_value(multiworld, player, "wisps_required") #1-108
    fish_locations = get_option_value(multiworld, player, "fish_locations") #all = 1, only_not_fish = 2, only_fish_and_related = 3, only_fish = 4
    alpha_locations = get_option_value(multiworld, player, "alpha_locations") #85 locations (n65/a6/f14), all filler

    #logging.info(f'wisps_total: {wisps_total}')
    #logging.info(f'wisps_required: {wisps_required}')
    #logging.info(f'fish_locations: {fish_locations}')
    #logging.info(f'alpha_locations: {alpha_locations}')

    #Code to remove items for fishing mode, precollect some items to free up locations, and determine max wisps:

    location_count = 231 #177 notfish, 36 fish, 18 fishadjacent. Without victory and preplaced. Without alpha.
    item_count = 81 #minimum unique items, 1 wisp

    if fish_locations == 2:
        location_count = 177
        if alpha_locations:
            location_count += 65
    if fish_locations == 3:
        itemNamesToRemove += world.item_name_groups["notfish"] #removes unnecessary evolution items
        location_count = 54
        item_count = 59
        if alpha_locations:
            location_count += 20
    if fish_locations == 4:
        itemNamesToRemove += world.item_name_groups["notfish"]
        location_count = 36
        item_count = 59
        if alpha_locations:
            location_count += 6

    spare_locations = location_count - item_count #only matters if <108, no calculation required for fish_locations == 1.

    if spare_locations < 9:
        precollect_items = []
        precollect_items += world.item_name_groups["warp"]
        precollect_items += ["Water Stone"]
        #logging.info(f'precollect_items: {precollect_items}')
        for itemName in precollect_items: #precollect items, then delete from item pool. Some are already in start_inventory, so try/continue.
            try:
                start_inventory = next(item for item in item_pool if item.name == itemName)
                multiworld.push_precollected(start_inventory)
                item_pool.remove(start_inventory)
            except StopIteration:
                continue
        spare_locations += 14
    if spare_locations < 9:
        precollect_items = []
        precollect_items += world.item_name_groups["outbreak"]
        precollect_items += world.item_name_groups["outbreak"]
        precollect_items += world.item_name_groups["Ride Pokémon"]
        #logging.info(f'precollect_items 2: {precollect_items}')
        for itemName in precollect_items:
            start_inventory = next(item for item in item_pool if item.name == itemName)
            multiworld.push_precollected(start_inventory)
            item_pool.remove(start_inventory)
        spare_locations += 15

    #logging.info(f'location_count: {location_count}')
    #logging.info(f'item_count: {item_count}')
    #logging.info(f'spare_locations: {spare_locations}')

    if spare_locations+1 < wisps_total: #+1! 1 wisp already included in items
        wisps_total = spare_locations+1
        #also change in locations

    #logging.info(f'wisps_total, final: {wisps_total}')

    if wisps_required > wisps_total:
        wisps_required = wisps_total
    index = wisps_required - 1
    del locationNamesToRemove[index]

    #print(locationNamesToRemove)

    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in locationNamesToRemove:
                    region.locations.remove(location)
    if hasattr(multiworld, "clear_location_cache"):
        multiworld.clear_location_cache()

    wisps_to_delete = 108 - wisps_total

    itemNamesToRemove += ["Wisp"] * wisps_to_delete


    shiny_locations = get_option_value(multiworld, player, "shiny_locations") #0-10 locations + items
    itemNamesToRemove += ["Shiny Charm Fragment"] * (10-shiny_locations)

    #print(itemNamesToRemove)

    for itemName in itemNamesToRemove:
        item = next(i for i in item_pool if i.name == itemName)
        item_pool.remove(item)

    #print(item_pool)

    return item_pool

    # Some other useful hook options:

    ## Place an item at a specific location
    # location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == "Location Name")
    # item_to_place = next(i for i in item_pool if i.name == "Item Name")
    # location.place_locked_item(item_to_place)
    # item_pool.remove(item_to_place)

# The complete item pool prior to being set for generation is provided here, in case you want to make changes to it
def after_create_items(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

# Called before rules for accessing regions and locations are created. Not clear why you'd want this, but it's here.
def before_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after rules for accessing regions and locations are created, in case you want to see or modify that information.
def after_set_rules(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to modify the access rules for a given location

    def Example_Rule(state: CollectionState) -> bool:
        # Calculated rules take a CollectionState object and return a boolean
        # True if the player can access the location
        # CollectionState is defined in BaseClasses
        return True

    ## Common functions:
    # location = world.get_location(location_name, player)
    # location.access_rule = Example_Rule

    ## Combine rules:
    # old_rule = location.access_rule
    # location.access_rule = lambda state: old_rule(state) and Example_Rule(state)
    # OR
    # location.access_rule = lambda state: old_rule(state) or Example_Rule(state)

# The item name to create is provided before the item is created, in case you want to make changes to it
def before_create_item(item_name: str, world: World, multiworld: MultiWorld, player: int) -> str:
    return item_name

# The item that was created is provided after creation, in case you want to modify the item
def after_create_item(item: ManualItem, world: World, multiworld: MultiWorld, player: int) -> ManualItem:
    return item

# This method is run towards the end of pre-generation, before the place_item options have been handled and before AP generation occurs
def before_generate_basic(world: World, multiworld: MultiWorld, player: int) -> list:
    pass

# This method is run at the very end of pre-generation, once the place_item options have been handled and before AP generation occurs
def after_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This is called before slot data is set and provides an empty dict ({}), in case you want to modify it before Manual does
def before_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called after slot data is set and provides the slot data at the time, in case you want to check and modify it after Manual is done with it
def after_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called right at the end, in case you want to write stuff to the spoiler log
def before_write_spoiler(world: World, multiworld: MultiWorld, spoiler_handle) -> None:
    pass
