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

# Automate small bod building. You just need to specify a few containers,
# have a container fully stocked, have a container of tools, and you are good to go.
# Supports these skills: Blacksmithy, Tailoring
# Features: 
#   - automatically adds items to small bod
#   - salvages wasted (non exceptional items) with a salvage bag
#   
# General flow:
#   - selects bods from incompleSmallBodContainer
#   - filters for only those that match your list of recipes (see recipes param below)
#   - One craft cycle includes:
#       1. getting resources from resourceContainer
#       2. getting / using tool, setting resource in gump, setting category in gump
#       3. attempting craft
#       4. attempting to add crafted item to small bod
#       5. recycle all items in bag that remain (everything in list of recipes)
#
# Based on:
# https://github.com/matsamilla/Razor-Enhanced/blob/master/NoxBodFiles/Smithbodgod.py
run_bod_builder(
    
    # Serial of container to put your small bods in. The script will start with these.
    incompleteSmallBodContainer = 0x4025193E,
    
    # Serial of container to put completed small bods.
    completeSmallBodContainer = 0x402519AE,
    
    # Stash a bunch of tools in here and let it rip. Serial of container.
    toolContainer = 0x40251A02,
    
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
    allowedResourceHues = [RESOURCE_HUE_DEFAULT, RESOURCE_HUE_COPPER, RESOURCE_HUE_SHADOW_IRON, RESOURCE_HUE_DULL_COPPER, RESOURCE_HUE_BRONZE, RESOURCE_HUE_GOLD, RESOURCE_HUE_AGAPITE, RESOURCE_HUE_VERITE, RESOURCE_HUE_VALORITE],
    
    # (Optional) God save the queen
    gumpDelayMs = 250
)