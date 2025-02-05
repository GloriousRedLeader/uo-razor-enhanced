# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2025-02-04
# Use at your own risk. 

#from System.Collections.Generic import List
#import sys
#import re
#from System import Byte, Int32
#from Scripts.fm_core.core_player import find_first_in_container_by_ids
#from Scripts.fm_core.core_player import find_first_in_hands_by_id
#from Scripts.fm_core.core_player import move_all_items_from_container
#from Scripts.fm_core.core_player import move_item_to_container_by_id
#from Scripts.fm_core.core_player import find_in_container_by_id
#from Scripts.fm_core.core_player import find_first_in_container_by_name
#from Scripts.fm_core.core_player import find_all_in_container_by_id
#from Scripts.fm_core.core_mobiles import get_friends_by_names
#from Scripts.fm_core.core_rails import move
#from Scripts.fm_core.core_rails import go_to_tile
#from Scripts.fm_core.core_rails import get_tile_in_front
from Scripts.fm_core.core_items import AXE_STATIC_IDS
from Scripts.fm_core.core_items import LOG_STATIC_IDS
from Scripts.fm_core.core_items import TREE_STATIC_IDS
from Scripts.fm_core.core_items import DAGGER_STATIC_IDS
from Scripts.fm_core.core_items import BOARD_STATIC_IDS
from Scripts.fm_core.core_items import MINER_TOOLS_STATIC_IDS
from Scripts.fm_core.core_items import ORE_STATIC_IDS
from Scripts.fm_core.core_items import INGOT_STATIC_IDS
from Scripts.fm_core.core_items import STONE_STATIC_IDS
from Scripts.fm_core.core_items import REAGENT_STATIC_IDS
from Scripts.fm_core.core_items import ALCHEMY_TOOL_STATIC_IDS
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
from Scripts.fm_core.core_items import BLACKSMITHY_TOOL_STATIC_ID
from Scripts.fm_core.core_items import TINKERING_TOOL_STATIC_ID
from Scripts.fm_core.core_items import ALCHEMY_TOOL_STATIC_ID
from Scripts.fm_core.core_items import TAILORING_TOOL_STATIC_ID
from Scripts.fm_core.core_items import CARPENTRY_TOOL_STATIC_ID
from Scripts.fm_core.core_items import INSCRIPTION_TOOL_STATIC_ID
from Scripts.fm_core.core_items import BOD_STATIC_ID
from Scripts.fm_core.core_items import BOD_BOOK_STATIC_ID
from Scripts.fm_core.core_items import HUE_BLACKSMITHY
from Scripts.fm_core.core_items import HUE_TAILORING
from Scripts.fm_core.core_items import HUE_CARPENTRY
from Scripts.fm_core.core_items import HUE_ALCHEMY
from Scripts.fm_core.core_items import HUE_INSCRIPTION
from Scripts.fm_core.core_items import HUE_TINKERING

################## ################## ################## ##################
#
#   Restocker (InsaneUO specific)
#
################## ################## ################## ##################

# Restockable item that lives inside of a specialized resource container.
# Arguments are as follows:
# itemId: Refer to constants, but represents things like item ids for ingots, boards, etc.
# itemHue: Some items have the same id but use different hues (leather, ingots, boards)
# resourceBoxSerial: Inspect your resource box with razor, get the serial, plug it in
# resourceBoxButton: This is the button id of the gump. You can use gump inspector. Starts at 100 and increments up.
# amount: The number of items you want in your commodityDeedBox.
# resourceBoxPage: (Optional) The gump has multiple pages. Starts at 0. Most items are on page 0.
class RestockItem:
    def __init__(self, itemId, itemHue, resourceBoxSerial, resourceBoxButton, amount = 10000, resourceBoxPage = 0):
        self.itemId = itemId
        self.itemHue = itemHue
        self.resourceBoxSerial = resourceBoxSerial
        self.resourceBoxButton = resourceBoxButton
        self.amount = amount
        self.resourceBoxPage = resourceBoxPage
        
    def __str__(self):
        return f"RestockItem(itemId='{self.itemId}', itemHue={self.itemHue}, amount='{self.amount}', resourceBoxSerial='{self.resourceBoxSerial}', resourceBoxButton='{self.resourceBoxButton}', resourceBoxPage='{self.resourceBoxPage}')"        

#RESOURCES = [
#    RestockItem(BLACKPEARL, RESOURCE_HUE_DEFAULT, reagentResourceBoxSerial, 100, 10000, 0),
#    RestockItem(BLOODMOSS, RESOURCE_HUE_DEFAULT, reagentResourceBoxSerial, 101, 10000, 0),
#    RestockItem(GARLIC, RESOURCE_HUE_DEFAULT, reagentResourceBoxSerial, 102, 10000, 0),
#    RestockItem(GINSENG, RESOURCE_HUE_DEFAULT, reagentResourceBoxSerial, 103, 10000, 0),
#    RestockItem(MANDRAKEROOT, RESOURCE_HUE_DEFAULT, reagentResourceBoxSerial, 104, 10000, 0),
#    RestockItem(NIGHTSHADE, RESOURCE_HUE_DEFAULT, reagentResourceBoxSerial, 105, 10000, 0),
#    RestockItem(SULPHUROUSASH, RESOURCE_HUE_DEFAULT, reagentResourceBoxSerial, 106, 10000, 0),
#    RestockItem(SPIDERSILK, RESOURCE_HUE_DEFAULT, reagentResourceBoxSerial, 107, 10000, 0),
#    RestockItem(BATWING, RESOURCE_HUE_DEFAULT, reagentResourceBoxSerial, 108, 10000, 0),
#    RestockItem(GRAVEDUST, RESOURCE_HUE_DEFAULT, reagentResourceBoxSerial, 109, 10000, 0),
#    RestockItem(DAEMONBLOOD, RESOURCE_HUE_DEFAULT, reagentResourceBoxSerial, 110, 10000, 0),
#    RestockItem(NOXCRYSTAL, RESOURCE_HUE_DEFAULT, reagentResourceBoxSerial, 111, 10000, 0),
#    RestockItem(PIGIRON, RESOURCE_HUE_DEFAULT, reagentResourceBoxSerial, 112, 10000, 0),
#
#    RestockItem(BOARD_STATIC_ID, RESOURCE_HUE_DEFAULT, woodResourceBoxSerial, 107, 10000, 0),
#    RestockItem(BOARD_STATIC_ID, RESOURCE_HUE_OAK, woodResourceBoxSerial, 108, 10000, 0),
#    RestockItem(BOARD_STATIC_ID, RESOURCE_HUE_ASH, woodResourceBoxSerial, 109, 10000, 0),
#    RestockItem(BOARD_STATIC_ID, RESOURCE_HUE_YEW, woodResourceBoxSerial, 110, 10000, 0),
#    RestockItem(BOARD_STATIC_ID, RESOURCE_HUE_HEARTWOOD, woodResourceBoxSerial, 111, 10000, 0),
#    RestockItem(BOARD_STATIC_ID, RESOURCE_HUE_BLOODWOOD, woodResourceBoxSerial, 112, 10000, 0),
#    RestockItem(BOARD_STATIC_ID, RESOURCE_HUE_FROSTWOOD, woodResourceBoxSerial, 113, 10000, 0),
#
#    RestockItem(INGOT_STATIC_ID, RESOURCE_HUE_DEFAULT, ingotResourceBoxSerial, 101, 10000, 0),
#    RestockItem(INGOT_STATIC_ID, RESOURCE_HUE_DULL_COPPER, ingotResourceBoxSerial, 101, 10000, 0),
#    RestockItem(INGOT_STATIC_ID, RESOURCE_HUE_SHADOW_IRON, ingotResourceBoxSerial, 102, 10000, 0),
#    RestockItem(INGOT_STATIC_ID, RESOURCE_HUE_COPPER, ingotResourceBoxSerial, 103, 10000, 0),
#    RestockItem(INGOT_STATIC_ID, RESOURCE_HUE_BRONZE, ingotResourceBoxSerial, 104, 10000, 0),
#    RestockItem(INGOT_STATIC_ID, RESOURCE_HUE_GOLD, ingotResourceBoxSerial, 105, 10000, 0),
#    RestockItem(INGOT_STATIC_ID, RESOURCE_HUE_AGAPITE, ingotResourceBoxSerial, 106, 10000, 0),
#    RestockItem(INGOT_STATIC_ID, RESOURCE_HUE_VERITE, ingotResourceBoxSerial, 107, 10000, 0),
#    RestockItem(INGOT_STATIC_ID, RESOURCE_HUE_VALORITE, ingotResourceBoxSerial, 108, 10000, 0),
#
#    RestockItem(CLOTH_STATIC_ID, RESOURCE_HUE_DEFAULT, leatherResourceBoxSerial, 111, 10000, 0),
#    RestockItem(LEATHER_STATIC_ID, RESOURCE_HUE_DEFAULT, leatherResourceBoxSerial, 100, 10000, 0),
#    RestockItem(LEATHER_STATIC_ID, RESOURCE_HUE_SPINED, leatherResourceBoxSerial, 101, 10000, 0),
#    RestockItem(LEATHER_STATIC_ID, RESOURCE_HUE_HORNED, leatherResourceBoxSerial, 102, 10000, 0),
#    RestockItem(LEATHER_STATIC_ID, RESOURCE_HUE_BARBED, leatherResourceBoxSerial, 103, 10000, 0),
#]

# Returns sum of all the stacks in a container, ideally there would just be one stack.
def get_amount_in_container(resource, containerSerial):
    amount = 0
    items = Items.FindAllByID(resource.itemId, resource.itemHue, containerSerial, 0)
    for item in items:
        amount = amount + item.Amount
    return amount
    
# Stand near resource boxes and load everything from a resource box into a real container.
# This is useful for use in conjunction with the BODBuilder.
# InsaneUO specific.
def run_restocker(
    # Green commodity deed box. Can be any container that can hold weight though.
    commodityBoxSerial,
    
    # (Optional) An array of RestockItem, the resources you want to stock. This is how you configure it.
    # Include only those resources you wish to stock, the hue, the amount, the  gump button id, and page.
    # Page is the page on the gump menu.
    resources,
    
    # (Optional) Timeout between  gump button presses. Configure based on server latency.
    gumpDelayMs = 250
):
    RESOURCE_BOX_GUMP_ID = 0x23d0f169
    
    Items.UseItem(commodityBoxSerial)
    Misc.Pause(1000)
    
    for resource in resources:
        print(resource)
        
        if Gumps.HasGump(RESOURCE_BOX_GUMP_ID):
            Gumps.CloseGump(RESOURCE_BOX_GUMP_ID)
                
        amountInBox = get_amount_in_container(resource, commodityBoxSerial)
        if amountInBox >= resource.amount:
            continue
        
        Items.UseItem(resource.resourceBoxSerial)
        Gumps.WaitForGump(RESOURCE_BOX_GUMP_ID, 3000)
        Misc.Pause(gumpDelayMs)
        
        for page in range(0, resource.resourceBoxPage):
            Gumps.SendAction(RESOURCE_BOX_GUMP_ID, 2)
            Gumps.WaitForGump(RESOURCE_BOX_GUMP_ID, 3000)
            Misc.Pause(gumpDelayMs)
            
        while True:
            
            amountInBox = get_amount_in_container(resource, commodityBoxSerial)
            if amountInBox >= resource.amount:
                break
            
            Gumps.SendAction(RESOURCE_BOX_GUMP_ID, resource.resourceBoxButton)
            Gumps.WaitForGump(RESOURCE_BOX_GUMP_ID, 3000)
            Misc.Pause(gumpDelayMs)

            runAgain = True if Items.FindByID(resource.itemId, resource.itemHue, Player.Backpack.Serial, 0) is not None else False
            for r in resources:
                items = Items.FindAllByID(r.itemId, r.itemHue, Player.Backpack.Serial, 0)
                for item in items:
                    Items.Move(item, commodityBoxSerial, item.Amount)
                    Misc.Pause(800)

            if not runAgain:
                break
                








################## ################## ################## ##################
#
#   run_bod_builder
#
################## ################## ################## ##################

# Crafting gump category button ids. Should be the same for all modern UO
# (hopefully) otherwise client may have a heart attack. I dunno.
CAT_BLACKSMITHY_METAL_ARMOR = 1
CAT_BLACKSMITHY_HELMETS = 8
CAT_BLACKSMITHY_SHIELDS = 15
CAT_BLACKSMITHY_BLADED = 22
CAT_BLACKSMITHY_AXES = 29
CAT_BLACKSMITHY_POLEARMS = 36
CAT_BLACKSMITHY_BASHING = 43
CAT_BLACKSMITHY_CANNONS = 50
CAT_BLACKSMITHY_THROWING = 57

# Internal data structure of storing ingredients for a recipe.
class SmallBodResource:
    def __init__(self, resourceId, amount = 100, canOverrideHue = True, hue = RESOURCE_HUE_DEFAULT):
        self.resourceId = resourceId
        self.amount = amount
        self.canOverrideHue = canOverrideHue
        self.hue = hue
        
    def __str__(self):
        return f"SmallBodResource(resourceId='{self.resourceId}', amount={self.amount}, canOverrideHue='{self.canOverrideHue}', hue='{self.hue}')"        

# Recipe template. Pass an array of these to the run_bod_builder function.
# itemName: Lower case as it appears in the small bod (very bottom last line), e.g. mace
# gumpCategory: Represents a gump category button id. Use one of the constants above.
# gumpSelection: The create now button specific to an item. Goes in increments of 7.
# toolId: The tool item id you want to craft with to open the gump. See constants like BLACKSMITHY_TOOL_STATIC_ID
# resources: Array of SmallBodResource
class SmallBodRecipe:
    def __init__(self, itemName, gumpCategory, gumpSelection, toolId, resources):
        self.itemName = itemName
        self.gumpCategory = gumpCategory
        self.gumpSelection = gumpSelection
        self.toolId = toolId
        self.resources = resources
        
    def __str__(self):
        return f"SmallBodRecipe(itemName='{self.itemName}', gumpCategory='{self.gumpCategory}', gumpSelection='{self.gumpSelection}', toolId='{self.toolId}', resources='{self.resources}')"        
        
# Internal data structure used in our main method. Represents a bod and its recipe. 
class SmallBod:
    def __init__(self, itemName, amountMade, isExceptional, amountToMake, specialMaterialButton, specialMaterialHue, recipe):
        self.itemName = itemName
        self.amountMade = amountMade
        self.isExceptional = isExceptional
        self.amountToMake = amountToMake
        self.specialMaterialButton = specialMaterialButton
        self.specialMaterialHue = specialMaterialHue
        self.recipe = recipe
    def __str__(self):
        return f"SmallBod(itemName='{self.itemName}', amountMade='{self.amountMade}', isExceptional={self.isExceptional}, amountToMake='{self.amountToMake}', specialMaterialButton='{self.specialMaterialButton}', specialMaterialHue='{self.specialMaterialHue}', recipe={self.recipe})"        

# Default list of recipes. See SmallBodRecipe. You can use these, edit these, or just define your own.
RECIPES = [
    SmallBodRecipe("war hammer", CAT_BLACKSMITHY_BASHING, 37, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("kryss", CAT_BLACKSMITHY_BLADED, 44, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("heater shield", CAT_BLACKSMITHY_SHIELDS, 16, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("small plate shield", CAT_BLACKSMITHY_SHIELDS, 58, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("bladed staff", CAT_BLACKSMITHY_POLEARMS, 9, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("axe", CAT_BLACKSMITHY_AXES, 2, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("chaos shield", CAT_BLACKSMITHY_SHIELDS, 44, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("maul", CAT_BLACKSMITHY_BASHING, 16, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("medium plate shield", CAT_BLACKSMITHY_SHIELDS, 79, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("platemail legs", CAT_BLACKSMITHY_METAL_ARMOR, 72, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("viking sword", CAT_BLACKSMITHY_BLADED, 65, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("double bladed staff", CAT_BLACKSMITHY_POLEARMS, 16, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("hammer pick", CAT_BLACKSMITHY_BASHING, 2, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("scythe", CAT_BLACKSMITHY_POLEARMS, 51, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("ringmail gloves", CAT_BLACKSMITHY_METAL_ARMOR, 2, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("metal kite shield", CAT_BLACKSMITHY_SHIELDS, 30, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("tear kite shield", CAT_BLACKSMITHY_SHIELDS, 37, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("female plate", CAT_BLACKSMITHY_METAL_ARMOR, 86, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("chainmail leggings", CAT_BLACKSMITHY_METAL_ARMOR, 37, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("ringmail leggings", CAT_BLACKSMITHY_METAL_ARMOR, 9, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("close helmet", CAT_BLACKSMITHY_HELMETS, 9, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("double axe", CAT_BLACKSMITHY_AXES, 16, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("katana", CAT_BLACKSMITHY_BLADED, 37, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("halberd", CAT_BLACKSMITHY_POLEARMS, 23, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("lance", CAT_BLACKSMITHY_POLEARMS, 30, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("war mace", CAT_BLACKSMITHY_BASHING, 30, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("chainmail coif", CAT_BLACKSMITHY_METAL_ARMOR, 30, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("mace", CAT_BLACKSMITHY_BASHING, 9, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("metal shield", CAT_BLACKSMITHY_SHIELDS, 23, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("war fork", CAT_BLACKSMITHY_POLEARMS, 65, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("scepter", CAT_BLACKSMITHY_BASHING, 23, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("chainmail tunic", CAT_BLACKSMITHY_METAL_ARMOR, 44, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("platemail arms", CAT_BLACKSMITHY_METAL_ARMOR, 51, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("broadsword", CAT_BLACKSMITHY_BLADED, 9, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("longsword", CAT_BLACKSMITHY_BLADED, 51, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("executioner's axe", CAT_BLACKSMITHY_AXES, 23, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("two handed axe", CAT_BLACKSMITHY_AXES, 37, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("bascinet", CAT_BLACKSMITHY_HELMETS, 2, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("pike", CAT_BLACKSMITHY_POLEARMS, 37, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("spear", CAT_BLACKSMITHY_POLEARMS, 58, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("ringmail tunic", CAT_BLACKSMITHY_METAL_ARMOR, 23, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("plate helm", CAT_BLACKSMITHY_HELMETS, 30, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("large plate shield", CAT_BLACKSMITHY_SHIELDS, 72, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("large battle axe", CAT_BLACKSMITHY_AXES, 30, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("war axe", CAT_BLACKSMITHY_AXES, 44, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("platemail gorget", CAT_BLACKSMITHY_METAL_ARMOR, 65, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("ringmail sleeves", CAT_BLACKSMITHY_METAL_ARMOR, 16, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("platemail tunic", CAT_BLACKSMITHY_METAL_ARMOR, 79, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("buckler", CAT_BLACKSMITHY_SHIELDS, 2, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("bronze shield", CAT_BLACKSMITHY_SHIELDS, 9, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("short spear", CAT_BLACKSMITHY_POLEARMS, 44, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("bardiche", CAT_BLACKSMITHY_POLEARMS, 2, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("scimitar", CAT_BLACKSMITHY_BLADED, 58, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("platemail gloves", CAT_BLACKSMITHY_METAL_ARMOR, 58, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("helmet", CAT_BLACKSMITHY_HELMETS, 16, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("norse helm", CAT_BLACKSMITHY_HELMETS, 23, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("dagger", CAT_BLACKSMITHY_BLADED, 30, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("cutlass", CAT_BLACKSMITHY_BLADED, 23, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("battle axe", CAT_BLACKSMITHY_AXES, 9, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("order shield", CAT_BLACKSMITHY_SHIELDS, 51, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
]

# Helper method to salvage stuff.
def recycle(salvageBag, recipes):
    if salvageBag is None:
        return None
        
    found = False
    for itemName in recipes:
        while True:
            item = Items.FindByName(itemName, -1, Player.Backpack.Serial, 0)
            if item is None:
                break
            found = True
            Items.Move(item, salvageBag, item.Amount)
            Misc.Pause(800)

    if found:
        Misc.WaitForContext(salvageBag, 10000)
        Misc.ContextReply(salvageBag, 2)   
        Misc.Pause(1000)
    return None

# Helper method to generate a small bod data structure.
def get_small_bod(bod, recipes):
    
    PROP_ID_AMOUNT_TO_MAKE = 1060656
    PROP_ID_EXCEPTIONAL = 1045141
    PROP_ID_SHADOW_IRON = 1045143
    PROP_ID_ITEM_TEXT = 1060658
    
    DEFAULT_MATERIAL_BY_HUE_MAP = {
        HUE_BLACKSMITHY: { "button": 6, "hue": RESOURCE_HUE_DEFAULT },    # Iron Ingots
        HUE_TAILORING: { "button": 6, "hue": RESOURCE_HUE_DEFAULT },       # Leather
        HUE_CARPENTRY: { "button": 6, "hue": RESOURCE_HUE_DEFAULT },       # Wood
        HUE_TINKERING: { "button": 6, "hue": RESOURCE_HUE_DEFAULT },       # Iron Ingots
        HUE_ALCHEMY: { "button": 0, "hue": RESOURCE_HUE_DEFAULT },          # None
        HUE_INSCRIPTION: { "button": 0, "hue": RESOURCE_HUE_DEFAULT }      # None
    }    
    
    # This goes prop.Number -> { gump button id, special resource hue }
    # ServUO\Scripts\Services\BulkOrders\SmallBODs\SmallBODGump.cs
    # Tried doing a regex by special material name, e.g. All items must be made
    # with Dull Copper Ingots, but it didnt follow that convetion for carpenty.
    # It just said "Oak". So, I got mad and just did an exact match for the 
    # Propert.Number. Whatever.
    SPECIAL_PROP_MATERIAL_MAP = {
        1045142: { "button": 13, "hue": RESOURCE_HUE_DULL_COPPER },    # Dull Copper
        1045143: { "button": 20, "hue": RESOURCE_HUE_SHADOW_IRON },    # Shadow Iron
        1045144: { "button": 27, "hue": RESOURCE_HUE_COPPER },         # Copper
        1045145: { "button": 34, "hue": RESOURCE_HUE_BRONZE },         # Bronze
        1045146: { "button": 41, "hue": RESOURCE_HUE_GOLD },           # Gold
        1045147: { "button": 48, "hue": RESOURCE_HUE_AGAPITE },        # Agapite
        1045148: { "button": 55, "hue": RESOURCE_HUE_VERITE },         # Verite
        1045149: { "button": 62, "hue": RESOURCE_HUE_VALORITE },       # Valorite

        1049348: { "button": 13, "hue": RESOURCE_HUE_SPINED },         # Spined
        1049349: { "button": 20, "hue": RESOURCE_HUE_HORNED },         # Horned
        1049350: { "button": 27, "hue": RESOURCE_HUE_BARBED },         # Barbed
        
        1071428: { "button": 13, "hue": RESOURCE_HUE_OAK },             # Oak
        1071429: { "button": 20, "hue": RESOURCE_HUE_ASH },             # Ash
        1071430: { "button": 27, "hue": RESOURCE_HUE_YEW },             # Yew
        1071431: { "button": 34, "hue": RESOURCE_HUE_HEARTWOOD },       # Heartwood
        1071432: { "button": 41, "hue": RESOURCE_HUE_BLOODWOOD },       # Bloodwood
        1071433: { "button": 48, "hue": RESOURCE_HUE_FROSTWOOD },       # Frostwood
    }    
    
    isExceptional = False
    amountToMake = 0
    specialMaterial = DEFAULT_MATERIAL_BY_HUE_MAP[bod.Color]
    itemText = None
    amountMade = 0
    recipe = None
    for prop in bod.Properties:
        if prop.Number == PROP_ID_EXCEPTIONAL:
            isExceptional = True
        if prop.Number == PROP_ID_AMOUNT_TO_MAKE:
            amountToMake = int(prop.Args)
            
        if prop.Number in SPECIAL_PROP_MATERIAL_MAP:
            specialMaterial = SPECIAL_PROP_MATERIAL_MAP[prop.Number]
            
        if prop.Number == PROP_ID_ITEM_TEXT:
            print("PROP STRING:", prop.ToString())
            propList = prop.ToString().split(": ")
            itemName = propList[0]
            amountMade = int(propList[1])
            if itemName in recipes:
                recipe = recipes[itemName]
            
    if recipe is not None:
        return SmallBod(itemName, amountMade, isExceptional, amountToMake, specialMaterial["button"], specialMaterial["hue"], recipe)
    else:
        print("Warning: Could not find static info for:")
        for prop in bod.Properties:
            #print("\t", prop.ToString(), prop.Args.ToString(), prop.Number)
            print("\t", prop.ToString(), "(", prop.Number, ")")
            #print("\t", prop.ToString())
      
# Helper method to get a tool from the toolContainer. You dont need to worry about this.  
def get_tool(smallBod, toolContainer):
    tool = Items.FindByID(smallBod.recipe.toolId, -1, Player.Backpack.Serial, -1)
    if tool is not None:
        return tool
        
    tool = Items.FindByID(smallBod.recipe.toolId, -1, toolContainer, -1)
    if tool is not None:
        Items.Move(tool, Player.Backpack.Serial, tool.Amount)
        Misc.Pause(1000)
        return tool
    
# Helper method to get resources from the resourceContainer. Ignore me.
def check_resources(smallBod, resourceContainer):
    for resource in smallBod.recipe.resources:
        while True:
            hue = smallBod.specialMaterialHue if resource.canOverrideHue else resource.hue 
            items = Items.FindAllByID(resource.resourceId, hue, Player.Backpack.Serial, 0)
            
            
            amount = 0
            for item in items:
                amount = amount + item.Amount
                
            print("we have {}/{}".format(amount, resource.amount))
            
            if amount >= resource.amount:
                break
        
            item = Items.FindByID(resource.resourceId, hue, resourceContainer, -1)
            if item is not None:
                amountNeeded = resource.amount - amount
                amountRequested = item.Amount if item.Amount <= amountNeeded else amountNeeded
                Items.Move(item, Player.Backpack.Serial, amountRequested)
                Misc.Pause(1000)
            else:
                return False
                
    # Probably a better way to move all this junk back to the resource container
    # Intent is to keep backpack lightweight and clean. This is sort of a nuclear
    # explosion and doesnt account for people doing other bods that I dont
    # have predefined in RECIPES template above.
    ALL_RESOURCES = [INGOT_STATIC_ID, BOARD_STATIC_ID, CLOTH_STATIC_ID, LEATHER_STATIC_ID, MANDRAKEROOT, BLOODMOSS, SULPHUROUSASH, NIGHTSHADE, BLACKPEARL, SPIDERSILK, GINSENG, GARLIC, PIGIRON, BATWING, NOXCRYSTAL, DAEMONBLOOD, GRAVEDUST ]
    
    # Cleanup nonessentials, move to resource crate
    for resourceId in ALL_RESOURCES:
        keep = False
        for resource in smallBod.recipe.resources:
            if resourceId == resource.resourceId:
                keep = True
                break
        if not keep:
            items = Items.FindAllByID(resourceId, -1, Player.Backpack.Serial, -1)
            for item in items:
                Items.Move(item, resourceContainer, item.Amount)
        
    return True

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
def run_bod_builder(
    
    # Serial of container to put your small bods in. The script will start with these.
    incompleteSmallBodContainer,
    
    # Serial of container to put completed small bods.
    completeSmallBodContainer,
    
    # Stash a bunch of tools in here and let it rip. Serial of container.
    toolContainer,
    
    # Serial of regular container / commodity deed box (not a special resource box like insaneuo).
    # Fill this with ingots, reagents, etc. Use the run_restocker() function to help fill it up.
    resourceContainer,
    
    # (Optional) Your salvage bag
    salvageBag,
    
    # (Optional) Array of SmallBodRecipe. If not in this list, the bod will be skipped.
    # Only build bods that want these items. Can be of any profession.
    # Defaults to all the recipes I know about and was willing to implement.
    recipes = RECIPES,
    
    # (Optional) By default only regular materials are allowed (Iron, Leather). If you want
    # to add others like copper, spined leather, etc. then you need to explicitly add them here.
    # This is just an array of color ids. I have constants for them (see imports)
    allowedResourceHues = [RESOURCE_HUE_DEFAULT],
    
    # (Optional) God save the queen
    gumpDelayMs = 250
):
    # Open containers because we may not have that item data yet.
    Items.UseItem(completeSmallBodContainer)
    Misc.Pause(1000)
    Items.UseItem(incompleteSmallBodContainer)
    Misc.Pause(1000)
    Items.UseItem(toolContainer)
    Misc.Pause(1000)
    Items.UseItem(resourceContainer)
    Misc.Pause(1000)    
    
    CRAFTING_GUMP_ID = 0x38920abd
    SMALL_BOD_GUMP_ID =  0x5afbd742
    
    # Turn this array into a dictionary keyed on item name. Its just easier that way.
    # So instead of [SmallBodRecipe, SmallBodRecipe...] we get:
    # { "cutlass": SmallBodRecipe, "platemail helm": SmallBodRecipe...
    x = {}
    for recipe in recipes:
        x[recipe.itemName] = recipe
    recipes = x
        
    print("-------=======------________-------=======------")
    bods = Items.FindAllByID(BOD_STATIC_ID, -1, incompleteSmallBodContainer, 1)
    for bod in bods:
        while True:
            # Get fresh version of bod
            freshBod = Items.FindBySerial(bod.Serial)
            smallBod = get_small_bod(freshBod, recipes)
            
            if smallBod is not None:
                if smallBod.specialMaterialHue not in allowedResourceHues:
                    print("Warning: Skipping because material is not in allowed list: {}".format(smallBod))
                    break
                    
                if freshBod.Container != Player.Backpack.Serial:
                    Items.Move(freshBod, Player.Backpack.Serial, freshBod.Amount)
                    Misc.Pause(1000)                
                    
                print(smallBod)
                
                if smallBod.amountToMake == smallBod.amountMade:
                    print("All done with this one")
                    Items.Move(freshBod, completeSmallBodContainer, freshBod.Amount)
                    Misc.Pause(1000)                
                    break
                else:
                    print("{} {}/{}".format(smallBod.itemName, smallBod.amountMade, smallBod.amountToMake))
                    
                    tool = get_tool(smallBod, toolContainer)
                    
                    if tool is None:
                        print("Error: Cannot find tool")
                        sys.exit()
                        
                    if not check_resources(smallBod, resourceContainer):
                        print("Error: Out of resources")
                        sys.exit()

                    Items.UseItem(tool)
                    Gumps.WaitForGump(CRAFTING_GUMP_ID, 5000)
                    Misc.Pause(gumpDelayMs)
                    if not Gumps.HasGump(CRAFTING_GUMP_ID):
                        continue
                        
                    # Set material (not every profession has it, e.g. alchemy)
                    if smallBod.specialMaterialButton > 0:
                        # The menu button to select material
                        Gumps.SendAction(CRAFTING_GUMP_ID, 7)
                        Gumps.WaitForGump(CRAFTING_GUMP_ID, 5000)
                        Misc.Pause(gumpDelayMs)
                        if not Gumps.HasGump(CRAFTING_GUMP_ID):
                            continue                    
                            
                        # The actual special material button
                        Gumps.SendAction(CRAFTING_GUMP_ID, smallBod.specialMaterialButton)
                        Gumps.WaitForGump(CRAFTING_GUMP_ID, 5000)
                        Misc.Pause(gumpDelayMs)
                        if not Gumps.HasGump(CRAFTING_GUMP_ID):
                            continue     
                    
                    # Sets category
                    Gumps.SendAction(CRAFTING_GUMP_ID, smallBod.recipe.gumpCategory)
                    Gumps.WaitForGump(CRAFTING_GUMP_ID, 5000)
                    Misc.Pause(gumpDelayMs)
                    if not Gumps.HasGump(CRAFTING_GUMP_ID):
                        continue
                            
                    # Actually does crafting
                    Gumps.SendAction(CRAFTING_GUMP_ID, smallBod.recipe.gumpSelection)                    
                    Gumps.WaitForGump(CRAFTING_GUMP_ID, 5000)
                    Misc.Pause(1000)
                    if not Gumps.HasGump(CRAFTING_GUMP_ID):
                        continue                    
   
                    # Open small bod gump
                    Items.UseItem(freshBod)
                    Gumps.WaitForGump(SMALL_BOD_GUMP_ID, 5000)
                    Misc.Pause(gumpDelayMs)
                    Target.Cancel()
                    
                    # Combine with contained items (backpack)
                    Gumps.SendAction(SMALL_BOD_GUMP_ID, 4) 
                    Target.WaitForTarget(5000)
                    Target.TargetExecute(Player.Backpack.Serial)
                    Gumps.WaitForGump(SMALL_BOD_GUMP_ID, 3000)
                    Misc.Pause(1000)
                    Target.Cancel()
                    Gumps.CloseGump(SMALL_BOD_GUMP_ID)
                
                if Player.MaxWeight - Player.Weight < 100:
                    recycle(salvageBag, recipes)         

            else:
                break
                
            recycle(salvageBag, recipes)                     
