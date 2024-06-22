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

    locationNamesToRemove = []
    regions_to_remove = []

    # Add your code here to calculate which locations to remove

    game_mode_short = get_option_value(multiworld, player, "game_mode_short")
    
    if game_mode_short:
        #Select which regions aren't needed and remove their locations:
        assignment_count = get_option_value(multiworld, player, "short_assignment_count")
        while assignment_count < 8:
            assignment_count += 1
            regions_to_remove += [f"Assignment {assignment_count}"]
        #print(regions_to_remove)


    for region in multiworld.regions:
        if region.player != player:
            continue
        #print(region.name)
        if region.name in regions_to_remove:
            #print("region removed")
            for location in list(region.locations):
                region.locations.remove(location)
    
    
    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in locationNamesToRemove:
                    region.locations.remove(location)
    if hasattr(multiworld, "clear_location_cache"):
        multiworld.clear_location_cache()


# The item pool before starting items are processed, in case you want to see the raw item pool at that stage
def before_create_items_starting(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    
    locationNamesToRemove = []
    itemNamesToRemove = []
    regions_to_remove = []

    if get_option_value(multiworld, player, "game_mode_short"):
        #Randomly select AP assignments:
        assignment_count = get_option_value(multiworld, player, "short_assignment_count")
        missions = ["Mining Expedition", "Egg Hunt", "On-site Refining", "Salvage Operation", "Point Extraction", "Escort Duty", "Elimination", "Industrial Sabotage", "Deep Scan"]
        multiworld.random.shuffle(missions)
        missions_to_delete = missions[assignment_count:] #Deletes missions starting from index assignment_count
        for itemName in missions_to_delete: 
            delete_item = next(i for i in item_pool if i.name == itemName)
            item_pool.remove(delete_item)
        
        #Set assignment count item for logic:
        assignment_counter = next(item for item in item_pool if item.name == f"Logic-only item for {assignment_count} assignments")
        multiworld.push_precollected(assignment_counter)
        items_to_remove = ["Logic-only item for 4 assignments","Logic-only item for 5 assignments","Logic-only item for 6 assignments","Logic-only item for 7 assignments","Logic-only item for 8 assignments"]
        for itemName in items_to_remove:
            delete_item = next(i for i in item_pool if i.name == itemName)
            item_pool.remove(delete_item)
        
        #Start inventory and easy start yaml option:
        start_inventory_items = [missions[0]] #last 0-4 are deleted above, the first is never deleted
        classes = ["Driller", "Engineer", "Gunner", "Scout"]
        multiworld.random.shuffle(classes)
        start_inventory_items += [classes[0]]
        primary_weapons = ["Primary Weapon 1", "Primary Weapon 2", "Primary Weapon 3"]
        multiworld.random.shuffle(primary_weapons)
        start_inventory_items += [primary_weapons[0]]
        if get_option_value(multiworld, player, "short_easy_start"):
            start_inventory_items += ["Traversal Tool 1/4", "Special Equipment 1/4"]
            secondary_weapons = ["Secondary Weapon 1", "Secondary Weapon 2", "Secondary Weapon 3"]
            multiworld.random.shuffle(secondary_weapons)
            start_inventory_items += secondary_weapons[2:]
        for itemName in start_inventory_items: #precollect items, then delete from item pool.
            start_inventory = next(item for item in item_pool if item.name == itemName)
            multiworld.push_precollected(start_inventory)
            item_pool.remove(start_inventory)
    
    else:
        #Randomly select missions, remove unneeded locations and items:
        mission_count = get_option_value(multiworld, player, "long_mission_count")
        missions = ['Mining Expedition with Driller', 'Mining Expedition with Engineer', 'Mining Expedition with Gunner', 'Mining Expedition with Scout', 'Egg Hunt with Driller', 'Egg Hunt with Engineer', 'Egg Hunt with Gunner', 'Egg Hunt with Scout', 'On-site Refining with Driller', 'On-site Refining with Engineer', 'On-site Refining with Gunner', 'On-site Refining with Scout', 'Salvage Operation with Driller', 'Salvage Operation with Engineer', 'Salvage Operation with Gunner', 'Salvage Operation with Scout', 'Point Extraction with Driller', 'Point Extraction with Engineer', 'Point Extraction with Gunner', 'Point Extraction with Scout', 'Escort Duty with Driller', 'Escort Duty with Engineer', 'Escort Duty with Gunner', 'Escort Duty with Scout', 'Elimination with Driller', 'Elimination with Engineer', 'Elimination with Gunner', 'Elimination with Scout', 'Industrial Sabotage with Driller', 'Industrial Sabotage with Engineer', 'Industrial Sabotage with Gunner', 'Industrial Sabotage with Scout', 'Deep Scan with Driller', 'Deep Scan with Engineer', 'Deep Scan with Gunner', 'Deep Scan with Scout']
        multiworld.random.shuffle(missions)
        if hasattr(multiworld, "re_gen_passthrough") == False:
            missions_to_delete = missions[mission_count:] #Deletes missions starting from index mission_count
            #print(f"missions_to_delete: {missions_to_delete}")
            for itemName in missions_to_delete: 
                delete_item = next(i for i in item_pool if i.name == itemName)
                item_pool.remove(delete_item)
                #print(f"delete_item: {delete_item}")
                locationNamesToRemove += [f"{itemName} - Reward 1", f"{itemName} - Reward 2"]
            #print(f"locationNamesToRemove: {locationNamesToRemove}")
            missions = missions[:mission_count]

        #Start inventory missions: 
        starting_mission_count = get_option_value(multiworld, player, "long_starting_mission_count")
        if starting_mission_count > mission_count:
            starting_mission_count = mission_count
        start_inventory_items = missions[:starting_mission_count]
        for itemName in start_inventory_items: #precollect items, then delete from item pool.
            start_inventory = next(item for item in item_pool if item.name == itemName)
            multiworld.push_precollected(start_inventory)
            item_pool.remove(start_inventory)
        
        #Set missions required for goal:
        mission_completions_required = get_option_value(multiworld, player, "long_mission_completions_to_win")
        if mission_completions_required > mission_count:
            mission_completions_required = mission_count
        victory_locations = ['Complete 4 missions', 'Complete 5 missions', 'Complete 6 missions', 'Complete 7 missions', 'Complete 8 missions', 'Complete 9 missions', 'Complete 10 missions', 'Complete 11 missions', 'Complete 12 missions', 'Complete 13 missions', 'Complete 14 missions', 'Complete 15 missions', 'Complete 16 missions', 'Complete 17 missions', 'Complete 18 missions', 'Complete 19 missions', 'Complete 20 missions', 'Complete 21 missions', 'Complete 22 missions', 'Complete 23 missions', 'Complete 24 missions', 'Complete 25 missions', 'Complete 26 missions', 'Complete 27 missions', 'Complete 28 missions', 'Complete 29 missions', 'Complete 30 missions', 'Complete 31 missions', 'Complete 32 missions', 'Complete 33 missions', 'Complete 34 missions', 'Complete 35 missions', 'Complete 36 missions']
        victory_locations.remove(f'Complete {mission_completions_required} missions')
        #print(victory_locations)
        locationNamesToRemove += victory_locations

        #if trophies_required > trophies_total:
        #    trophies_required = trophies_total
        #index = trophies_required - 1
        #del trophy_locations[index] #or trophy_locations.remove(f'Collect {trophies_required} trophies')
        
        #include secondary objectives, warnings and/or anomalies:
        if get_option_value(multiworld, player, "long_secondary_objectives") == False:
            itemNamesToRemove += world.item_name_groups["(L) Secondary objectives"]
            locationNamesToRemove += world.location_name_groups["Secondary objectives"]
        if get_option_value(multiworld, player, "long_warnings") == False:
            itemNamesToRemove += world.item_name_groups["(L) Warning mutators"]
            locationNamesToRemove += world.location_name_groups["Warning mutators"]
        if get_option_value(multiworld, player, "long_anomalies") == False:
            itemNamesToRemove += world.item_name_groups["(L) Anomaly mutators"]
            locationNamesToRemove += world.location_name_groups["Anomaly mutators"]
            
        #include (elite) deep dives, weekly assignments and/or season challenges:
        deep_dive_count = get_option_value(multiworld, player, "long_deep_dive_count")
        itemNamesToRemove += ["Deep Dive"] * (6 - deep_dive_count)
        while deep_dive_count < 6:
            deep_dive_count += 1
            regions_to_remove += [f"DD{deep_dive_count}"]
        elite_deep_dive_count = get_option_value(multiworld, player, "long_elite_deep_dive_count")
        itemNamesToRemove += ["Elite Deep Dive"] * (6 - elite_deep_dive_count)
        while elite_deep_dive_count < 6:
            elite_deep_dive_count += 1
            regions_to_remove += [f"EDD{elite_deep_dive_count}"]
        weekly_assignment_count = get_option_value(multiworld, player, "long_weekly_assignment_count")
        itemNamesToRemove += ["Weekly Priority Assignment"] * (6 - weekly_assignment_count)
        itemNamesToRemove += ["Weekly Core Hunt"] * (6 - weekly_assignment_count)
        while weekly_assignment_count < 6:
            weekly_assignment_count += 1
            regions_to_remove += [f"WPA{weekly_assignment_count}"]
            regions_to_remove += [f"WCH{weekly_assignment_count}"]
        season_callenge_count = get_option_value(multiworld, player, "long_season_callenge_count")
        itemNamesToRemove += ["Season challenge"] * (30 - season_callenge_count)
        while season_callenge_count < 9:
            season_callenge_count += 1
            locationNamesToRemove += [f"Season Challenge 0{season_callenge_count}"]
        while season_callenge_count < 30:
            season_callenge_count += 1
            locationNamesToRemove += [f"Season Challenge {season_callenge_count}"]

    for region in multiworld.regions:
        if region.player != player:
            continue
        #print(region.name)
        if region.name in regions_to_remove:
            #print("region removed")
            for location in list(region.locations):
                region.locations.remove(location)

    #print(locationNamesToRemove)
    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in locationNamesToRemove:
                    region.locations.remove(location)
                    #print(f"remove location: {location}")
    if hasattr(multiworld, "clear_location_cache"):
        multiworld.clear_location_cache()

    #print(itemNamesToRemove)
    #print(item_pool)
    for itemName in itemNamesToRemove:
        item = next(i for i in item_pool if i.name == itemName)
        item_pool.remove(item)


    return item_pool

# The item pool after starting items are processed but before filler is added, in case you want to see the raw item pool at that stage
def before_create_items_filler(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:

    itemNamesToRemove = []

    # Because multiple copies of an item can exist, you need to add an item name
    # to the list multiple times if you want to remove multiple copies of it.

    game_mode_short = get_option_value(multiworld, player, "game_mode_short")

    #Place a victory item on the last ap assignment:
    if game_mode_short:
        assignment_count = get_option_value(multiworld, player, "short_assignment_count")
        last_assignment_location = f"Assignment {assignment_count}-3"
        #print(last_assignment_location)
        location = multiworld.get_location(last_assignment_location, player)
        item_to_place = next(i for i in item_pool if i.name == "Assignments Complete!")
        location.place_locked_item(item_to_place)
        item_pool.remove(item_to_place)

    for itemName in itemNamesToRemove:
        item = next(i for i in item_pool if i.name == itemName)
        item_pool.remove(item)

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
