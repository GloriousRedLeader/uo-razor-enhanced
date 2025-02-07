# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2025-02-04
# Use at your own risk. 

from Scripts.fm_core.core_items import BOD_STATIC_ID
from Scripts.fm_core.core_items import BOD_BOOK_STATIC_ID
from Scripts.fm_core.core_items import BLACKSMITHY_TOOL_STATIC_ID
from Scripts.fm_core.core_items import TINKERING_TOOL_STATIC_ID
from Scripts.fm_core.core_items import ALCHEMY_TOOL_STATIC_ID
from Scripts.fm_core.core_items import TAILORING_TOOL_STATIC_ID
from Scripts.fm_core.core_items import CARPENTRY_TOOL_STATIC_ID
from Scripts.fm_core.core_items import INSCRIPTION_TOOL_STATIC_ID
from Scripts.fm_core.core_items import INGOT_STATIC_ID 
from Scripts.fm_core.core_items import BOARD_STATIC_ID 
from Scripts.fm_core.core_items import CLOTH_STATIC_ID 
from Scripts.fm_core.core_items import LEATHER_STATIC_ID 
from Scripts.fm_core.core_items import EMPTY_BOTTLE_STATIC_ID
from Scripts.fm_core.core_items import BLANK_SCROLL
from Scripts.fm_core.core_items import MANDRAKEROOT
from Scripts.fm_core.core_items import BLOODMOSS
from Scripts.fm_core.core_items import SULPHUROUSASH
from Scripts.fm_core.core_items import NIGHTSHADE
from Scripts.fm_core.core_items import BLACKPEARL
from Scripts.fm_core.core_items import SPIDERSILK
from Scripts.fm_core.core_items import GINSENG
from Scripts.fm_core.core_items import GARLIC
from Scripts.fm_core.core_items import PIGIRON
from Scripts.fm_core.core_items import BATWING
from Scripts.fm_core.core_items import NOXCRYSTAL
from Scripts.fm_core.core_items import DAEMONBLOOD
from Scripts.fm_core.core_items import GRAVEDUST
from Scripts.fm_core.core_items import RESOURCE_HUE_DEFAULT
from Scripts.fm_core.core_items import RESOURCE_HUE_DULL_COPPER
from Scripts.fm_core.core_items import RESOURCE_HUE_SHADOW_IRON
from Scripts.fm_core.core_items import RESOURCE_HUE_COPPER
from Scripts.fm_core.core_items import RESOURCE_HUE_BRONZE
from Scripts.fm_core.core_items import RESOURCE_HUE_GOLD
from Scripts.fm_core.core_items import RESOURCE_HUE_AGAPITE
from Scripts.fm_core.core_items import RESOURCE_HUE_VERITE
from Scripts.fm_core.core_items import RESOURCE_HUE_VALORITE
from Scripts.fm_core.core_items import RESOURCE_HUE_BARBED
from Scripts.fm_core.core_items import RESOURCE_HUE_SPINED
from Scripts.fm_core.core_items import RESOURCE_HUE_HORNED
from Scripts.fm_core.core_items import RESOURCE_HUE_OAK
from Scripts.fm_core.core_items import RESOURCE_HUE_ASH
from Scripts.fm_core.core_items import RESOURCE_HUE_YEW
from Scripts.fm_core.core_items import RESOURCE_HUE_HEARTWOOD
from Scripts.fm_core.core_items import RESOURCE_HUE_BLOODWOOD
from Scripts.fm_core.core_items import RESOURCE_HUE_FROSTWOOD
from Scripts.fm_core.core_crafting import CAT_BLACKSMITHY_METAL_ARMOR
from Scripts.fm_core.core_crafting import CAT_BLACKSMITHY_HELMETS
from Scripts.fm_core.core_crafting import CAT_BLACKSMITHY_SHIELDS
from Scripts.fm_core.core_crafting import CAT_BLACKSMITHY_BLADED
from Scripts.fm_core.core_crafting import CAT_BLACKSMITHY_AXES
from Scripts.fm_core.core_crafting import CAT_BLACKSMITHY_POLEARMS
from Scripts.fm_core.core_crafting import CAT_BLACKSMITHY_BASHING
from Scripts.fm_core.core_crafting import SmallBodResource
from Scripts.fm_core.core_crafting import SmallBodRecipe
from Scripts.fm_core.core_crafting import RECIPES
from Scripts.fm_core.core_crafting import run_bod_builder

# Automate bod building (both small and large). You just dump all your bods into the starting
# container and it will sort them, craft items, fill small bods, combine large bods, etc. 
#
# WARNING: OPERATES IN BACKPACK AND WILL SALVAGE BLACKSMITH AND TAILORING ITEMS. DO NOT HAVE
# ANYTHING GOOD IN YOUR BACKPACK WHILE YOU RUN THIS SCRIPT YOU RISK LOSING IT.
#
# Requirements:
#   - You need a container of resources (ingots, etc.)
#   - You need a container of tools
#   - You need a forge and anvil nearby
#   - You need containers for incomplete (unsorted or not started bods), if you arent sure, dump here
#   - You need a container for filled small bods
#   - You need a container for filled large bods
#
# You just need to specify a few containers, have a resource container fully stocked, 
# have a container of tools, and you are good to go. Supports all crafting skills (allegedly), 
# but currently only has recipes for Blacksmithy. Some other features include: 
#   - automatically adds items to small bod
#   - salvages wasted (non exceptional items) with a salvage bag
#   
# General flow:
# 1. Small Bods
#   - selects small bods from incompleBodContainer
#   - filters for only those that match your list of recipes (see recipes param below)
#   - One craft cycle includes:
#       1. getting resources from resourceContainer
#       2. getting / using tool, setting resource in gump, setting category in gump
#       3. attempting craft
#       4. attempting to add crafted item to small bod
#       5. recycle all items in bag that remain (everything in list of recipes)
#   - Puts completed small bod in either incompleteBodContainer or completeSmallBodContainer
#
# 2. Large Bods
#   - Creates a database of all small bods
#   - Gets large bods from the incompleBodContainer, sorts them by "most complete"
#   - Looks up small bods in db, transfers to backpack, attempts to combine
#   - If complete, moves to completeLargeBodContainer, otherwise back to incompleBodContainer
#
# Based on:
# https://github.com/matsamilla/Razor-Enhanced/blob/master/NoxBodFiles/Smithbodgod.py
run_bod_builder(
    
    # Array of serials for containers to put your bods in to start things off (both small and large).
    # You put your bods in here.
    incompleteBodContainers = [0x40251A02, 0x402519AE, 0x4025193E],
    
    # Array of serials of containers to put completed small bods.
    # The script will store completed small bods in these.
    completeSmallBodContainers = [0x40251A68, 0x4042D758, 0x4042D779],
    
    # Serial of container for completed LBODs. This is where you can pick them
    # up and then go turn them in. 
    completeLargeBodContainer = 0x4042E137,
    
    # Stash a bunch of tools in here and let it rip. Serial of container.
    toolContainer = 0x4042E100,
    
    # Serial of regular container / commodity deed box (not a special resource box like insaneuo).
    # Fill this with ingots, reagents, etc. Use the run_restocker() function to help fill it up.
    resourceContainer = 0x408CC21E,
    
    # (Optional) Your salvage bag
    salvageBag = 0x400E972D,
    
    # (Optional) Array of SmallBodRecipe. If not in this list, the bod will be skipped.
    # Only build bods that want these items. Can be of any profession.
    # Defaults to all the recipes I know about and was willing to implement.
    recipes = RECIPES,
    
    # (Optional) By default only regular materials are allowed (Iron, Leather). If you want
    # to add others like copper, spined leather, etc. then you need to explicitly add them here.
    # This is just an array of color ids. I have constants for them (see imports)
    allowedResourceHues = [RESOURCE_HUE_DEFAULT, RESOURCE_HUE_COPPER, RESOURCE_HUE_SHADOW_IRON, RESOURCE_HUE_DULL_COPPER, RESOURCE_HUE_BRONZE, RESOURCE_HUE_GOLD, RESOURCE_HUE_AGAPITE, RESOURCE_HUE_VERITE, RESOURCE_HUE_VALORITE, RESOURCE_HUE_BARBED, RESOURCE_HUE_SPINED, RESOURCE_HUE_HORNED, RESOURCE_HUE_OAK, RESOURCE_HUE_ASH, RESOURCE_HUE_YEW, RESOURCE_HUE_HEARTWOOD, RESOURCE_HUE_BLOODWOOD, RESOURCE_HUE_FROSTWOOD ],
    
    # Time to wait between item moves. Adjust with caution. Reducing this will increase speed
    # of the script, but you risk disconnects and other issues maintaining state
    itemMoveDelayMs = 1000,    

    # (Optional) God save the queen
    gumpDelayMs = 250
)