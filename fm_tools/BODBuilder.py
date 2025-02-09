# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2025-02-04
# Use at your own risk. 

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
from Scripts.fm_core.core_crafting import RECIPES
from Scripts.fm_core.core_crafting import run_bod_builder

# Automate bod building (both small and large). You just dump all your bods into the starting
# container and it will sort them, craft items, fill small bods, combine large bods, etc. 
#
# WARNING: OPERATES IN BACKPACK AND WILL SALVAGE BLACKSMITH AND TAILORING ITEMS. DO NOT HAVE
# ANYTHING GOOD IN YOUR BACKPACK WHILE YOU RUN THIS SCRIPT YOU RISK LOSING IT.
#
# Known quirks:
#   - For inscription, scrolls are stacked after crafting. The auto-add-to-sbod part may fail
#       if the stack has more than one. So, you'll have to stop the script and separate the items
#       into individual stacks of one and restart the script. Normally the item is added to the sbod
#       deed immediately. But internet fuzz and crashing in the middle of an inscription scroll sbod
#       may leave it in this state. Be aware.
#
# Requirements:
#   - You need a container of resources (ingots, etc.)
#   - You need a container of tools
#   - You need a forge and anvil nearby
#   - You need containers for incomplete (unsorted or not started bods), dump all bods here (large and small)
#   - You need a container for complete small bods (solo)
#   - You need containers for complete small bods (part of larger bods)
#   - You need a container for complete large bods
#
# You just need to specify a few containers, have a resource container fully stocked, 
# have a container of tools, and you are good to go. Supports: Blacksmithing, Tailoring,
# Alchemy, Inscription, Carpentry. Has these features:
#   - auto crafts items
#   - cleans up crafted items that dont meet requirements (non exceptional)
#   - puts completed large bods and solo small bods in containers for easy access and turn-in
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
#       5. attempt cleanup: salvage or dump waste into a container (trash bin recommended)
#   - Puts completed small bod in either completeSmallBodContainer or smallBodWaitingForLargeBodContainer
#   - (the above depends on whether this is a solo small bod or is part of a large bod)
#   - Note: Will attempt to meditate if mana is low for inscription
#
# 2. Large Bods
#   - Creates a database of all small bods
#   - Gets large bods from the incompleBodContainer, sorts them by "most complete"
#   - (the above happens so we focus on completion and dont spread too thin)
#   - Looks up small bods in db, transfers to backpack, attempts to combine
#   - If complete, moves to completeLargeBodContainer, otherwise back to incompleBodContainer
#
# Based on:
# https://github.com/matsamilla/Razor-Enhanced/blob/master/NoxBodFiles/Smithbodgod.py
run_bod_builder(

    # Array of serials for containers to put your bods in to start things off (both small and large).
    # You put your bods in here.
    incompleteBodContainers = [0x40251A02, 0x402519AE, 0x4025193E],
    
    # Array of serials for containers to store completed small bods
    # that are part of a large bod. This can take time. So store them here
    # until the can be combined.
    smallBodWaitingForLargeBodContainers = [0x40251A68, 0x4042D758, 0x4042D779],
    
    # Serial of container to put completed SOLO small bods. These
    # are small bods that do not have a corresponding large bod. They are ready
    # for turn-in.
    completeSmallBodContainer = 0x405DE401,
    
    # Serial of container for completed LBODs. This is where you can pick them
    # up and then go turn them in. 
    completeLargeBodContainer = 0x4042E137,
    
    # Stash a bunch of tools in here and let it rip. Serial of container.
    toolContainer = 0x4042E100,
    
    # Serial of regular container / commodity deed box (not a special resource box like insaneuo).
    # Fill this with ingots, reagents, etc. Use the run_restocker() function to help fill it up.
    resourceContainer = 0x408CC21E,
    
    # (Optional) Your salvage bag which is used for tailoring and blacksmithy rejects.
    # You get a little resource refund.
    salvageBag = 0x400E972D,
    
    # (Optional) Serial of a container to dump trash in that cant be salvaged. 
    # For non blacksmith/tailoring professions, dumps non-exceptional items here,
    # e.g. if you need exceptional footlockers and only get ordinary ones. Dont need that junk.
    # I think you can use a trash bin. Maybe place on next to you.
    # "I wish to place a trash barrel"
    trashContainer = 0x406766F3,
    
    # (Optional) Array of SmallBodRecipe. If not in this list, the bod will be skipped.
    # Only build bods that want these items. Can be of any profession.
    # Defaults to all the recipes I know about and was willing to implement.
    recipes = RECIPES,
    
    # (Optional) Array of colors that governs whether bods that require special materials are 
    # allowed (e.g. shadow iron, # frostwood, spined leather, etc.). Only this on this list will 
    # be crafted, otherwise those bods will be skipped. By default all special materials are allowed. 
    allowedResourceHues = [RESOURCE_HUE_DEFAULT, RESOURCE_HUE_COPPER, RESOURCE_HUE_SHADOW_IRON, RESOURCE_HUE_DULL_COPPER, RESOURCE_HUE_BRONZE, RESOURCE_HUE_GOLD, RESOURCE_HUE_AGAPITE, RESOURCE_HUE_VERITE, RESOURCE_HUE_VALORITE, RESOURCE_HUE_BARBED, RESOURCE_HUE_SPINED, RESOURCE_HUE_HORNED, RESOURCE_HUE_OAK, RESOURCE_HUE_ASH, RESOURCE_HUE_YEW, RESOURCE_HUE_HEARTWOOD, RESOURCE_HUE_BLOODWOOD, RESOURCE_HUE_FROSTWOOD ],
    
    # (Optional) Flag governs whether an exceptional small bod can be used to fill
    # a normal (non-exceptional) large bod. Its a real hassle trying to match these.
    # Default value is true which means exceptional small bods are incldued. Set to 
    # False to disable this.
    fillNormalLargeBodsWithExceptionalSmallBods = True,
    
    # Time to wait between item moves. Adjust with caution. Reducing this will increase speed
    # of the script, but you risk disconnects and other issues maintaining state
    itemMoveDelayMs = 1000,
    
    # (Optional) God save the queen
    gumpDelayMs = 250
)