# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2025-02-04
# Use at your own risk. 

import sys
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

# User would define something like this and pass it as an arg to the run_restocker() function.
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

# Helper that returns sum of all the stacks in a container, ideally there would just be one stack.
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
    
    # An array of RestockItem, the resources you want to stock. This is how you configure it.
    # Include only those resources you wish to stock, the hue, the amount, the  gump button id, and page.
    # Page is the page on the gump menu.
    resources,
    
    # Time to wait between item moves. Adjust with caution. Reducing this will increase speed
    # of the script, but you risk disconnects and other issues maintaining state
    itemMoveDelayMs = 1000,    
    
    # (Optional) Timeout between  gump button presses. Configure based on server latency.
    gumpDelayMs = 250
):
    RESOURCE_BOX_GUMP_ID = 0x23d0f169
    
    Items.UseItem(commodityBoxSerial)
    Misc.Pause(itemMoveDelayMs)
    
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
                    Misc.Pause(itemMoveDelayMs)

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

CAT_TAILORING_MATERIALS = 1
CAT_TAILORING_HATS = 8
CAT_TAILORING_SHIRTS_AND_PANTS = 15
CAT_TAILORING_MISCELLANEOUS = 22
CAT_TAILORING_FOOTWEAR = 29
CAT_TAILORING_LEATHER_ARMOR = 36
CAT_TAILORING_CLOTH_ARMOR = 43
CAT_TAILORING_STUDDED_ARMOR = 50
CAT_TAILORING_FEMALE_ARMOR = 57
CAT_TAILORING_BONE_ARMOR = 64

CAT_CARPENTRY_OTHER = 1
CAT_CARPENTRY_FURNITURE = 8
CAT_CARPENTRY_CONTAINERS = 15
CAT_CARPENTRY_WEAPONS = 22
CAT_CARPENTRY_ARMOR = 29
CAT_CARPENTRY_INSTRUMENTS = 36
CAT_CARPENTRY_MISC_ADDONS = 43
CAT_CARPENTRY_TAILORING_AND_COOKING = 50
CAT_CARPENTRY_ANVILS_AND_FORGES = 57
CAT_CARPENTRY_TRAINING = 64

CAT_ALCHEMY_HEALING_AND_CURATIVE = 1
CAT_ALCHEMY_ENHANCEMENT = 8
CAT_ALCHEMY_TOXIC = 15
CAT_ALCHEMY_EXPLOSIVE = 22
CAT_ALCHEMY_STRANGE_BREW = 29
CAT_ALCHEMY_INGREDIENTS = 36

CAT_INSCRIPTION_FIRST_SECOND = 1
CAT_INSCRIPTION_THIRD_FOURTH = 8
CAT_INSCRIPTION_FIFTH_SIXTH = 15
CAT_INSCRIPTION_SEVENTH_EIGTH = 22
CAT_INSCRIPTION_NECRO = 29
CAT_INSCRIPTION_OTHER = 36
CAT_INSCRIPTION_MYSTICISM = 43

# Internal data structure for storing ingredients for a recipe.
class SmallBodResource:
    def __init__(self, resourceId, amount = 100):
        self.resourceId = resourceId
        self.amount = amount
        
    def can_override_hue(self):
        return self.resourceId in [INGOT_STATIC_ID, BOARD_STATIC_ID, LEATHER_STATIC_ID ]
        
    def __str__(self):
        return f"SmallBodResource(resourceId='{self.resourceId}', amount={self.amount}, canOverrideHue='{self.can_override_hue()}')"        

# Recipe template. Pass an array of these to the run_bod_builder function.
# hasLarge: (NOT IMPLEMENTED) This small bod can be part of a large bod (several cannot)
# itemName: Lower case as it appears in the small bod (very bottom last line), e.g. mace
# gumpCategory: Represents a gump category button id. Use one of the constants above.
# gumpSelection: The create now button specific to an item. Goes in increments of 7.
# toolId: The tool item id you want to craft with to open the gump. See constants like BLACKSMITHY_TOOL_STATIC_ID
# resources: Array of SmallBodResource
class SmallBodRecipe:
    def __init__(self, itemName, gumpCategory, gumpSelection, toolId, resources):
        #self.hasLarge = hasLarge
        self.itemName = itemName
        self.gumpCategory = gumpCategory
        self.gumpSelection = gumpSelection
        self.toolId = toolId
        self.resources = resources
        
    def canSalvage(self):
        return self.toolId in [BLACKSMITHY_TOOL_STATIC_ID, TAILORING_TOOL_STATIC_ID]
        
    def __str__(self):
        return f"SmallBodRecipe(hasLarge={self.hasLarge},itemName='{self.itemName}', gumpCategory='{self.gumpCategory}', gumpSelection='{self.gumpSelection}', toolId='{self.toolId}', resources='{self.resources}')"        
        
# Internal data structure used in our main method. Represents a bod and its recipe. 
class SmallBod:
    def __init__(self, itemSerial, craftedItemName, amountMade, isExceptional, amountToMake, specialMaterialButton, specialMaterialHue, specialMaterialPropId, recipe):
        self.craftedItemName = craftedItemName
        self.amountMade = amountMade
        self.isExceptional = isExceptional
        self.amountToMake = amountToMake
        self.specialMaterialButton = specialMaterialButton
        self.specialMaterialHue = specialMaterialHue
        self.specialMaterialPropId = specialMaterialPropId
        self.recipe = recipe
        self.itemSerial = itemSerial
        
    def isComplete(self):
        return self.amountToMake == self.amountMade

    def __str__(self):
        return f"SmallBod(craftedItemName='{self.craftedItemName}', amountMade='{self.amountMade}', isExceptional={self.isExceptional}, amountToMake='{self.amountToMake}', specialMaterialButton='{self.specialMaterialButton}', specialMaterialHue='{self.specialMaterialHue}', specialMaterialPropId={self.specialMaterialPropId}, recipe={self.recipe})"        
        
# Internal data structure used for filling LBODS.
class LargeBod:
    def __init__(self, itemSerial, isExceptional, amountToMake, specialMaterialPropId, smallBodItems):
        self.isExceptional = isExceptional
        self.amountToMake = amountToMake
        self.specialMaterialPropId = specialMaterialPropId
        self.smallBodItems = smallBodItems
        self.itemSerial = itemSerial

    # Use this to identify similar bods (material, exceptional, and items required)
    # Need this to stort when filling large bods so we complete those with the most progress first
    def getId(self):
        part1 = "1" if self.isExceptional else "0"
        part2 = str(self.specialMaterialPropId) if self.specialMaterialPropId is not None else "0"
        part3 = "|".join(sorted(list(map(lambda smallBodItem: smallBodItem["name"], self.smallBodItems))))
        return part1 + "|" + part2 + "|" + part3
        
    def numComplete(self):
        numCompleted = 0
        for smallBodItem in self.smallBodItems:
            if smallBodItem['amountMade'] == self.amountToMake:
                numCompleted = numCompleted + 1
        return numCompleted
        
    def isComplete(self):
        isComplete = False
        numCompleted = 0
        for smallBodItem in self.smallBodItems:
            if smallBodItem['amountMade'] == self.amountToMake:
                numCompleted = numCompleted + 1
        return numCompleted == len(self.smallBodItems)

    def __str__(self):
        return f"LargeBod(isExceptional='{self.isExceptional}', amountToMake='{self.amountToMake}', specialMaterialPropId={self.specialMaterialPropId}, smallBodItems={self.smallBodItems}, isComplete={self.isComplete()}, numComplete={self.numComplete()})"                

# Just for reporting in conjunction with the report() function.
class BodReport:
    def __init__(self, name):
        self.name = name
        self.numIncompleteSmallBods = 0
        self.numCompleteSmallBods = 0
        self.numIncompleteLargeBods = 0
        self.numCompleteLargeBods = 0
        self.numInWrongContainer = 0
        self.numMissingRecipe = 0
        self.numMissingResources = 0

    def incrementNumIncompleteSmallBods(self):
        self.numIncompleteSmallBods = self.numIncompleteSmallBods + 1
        
    def incrementNumCompleteSmallBods(self):
        self.numCompleteSmallBods = self.numCompleteSmallBods + 1        
        
    def incrementNumIncompleteLargeBods(self):
        self.numIncompleteLargeBods = self.numIncompleteLargeBods + 1
        
    def incrementNumCompleteLargeBods(self):
        self.numCompleteLargeBods = self.numCompleteLargeBods + 1  
  
    def incrementNumInWrongContainer(self):
        self.numInWrongContainer = self.numInWrongContainer + 1
        
    def incrementNumMissingRecipe(self):
        self.numMissingRecipe = self.numMissingRecipe + 1
        
    def incrementNumMissingResources(self):
        self.numMissingResources = self.numMissingResources + 1
        
    def __str__(self):
        totalSmall = self.numIncompleteSmallBods + self.numCompleteSmallBods + self.numMissingRecipe
        totalLarge = self.numIncompleteLargeBods + self.numCompleteLargeBods
        #incompleteSmall = self.numIncompleteSmallBods - self.numMissingRecipe
        return "{}:\t\tSmall ({}/{})\t\tLarge ({}/{})\tWrong Container ({})\tNo Recipe ({})\tNo Resources ({})".format(self.name, self.numCompleteSmallBods, totalSmall, self.numCompleteLargeBods, totalLarge, self.numInWrongContainer, self.numMissingRecipe, self.numMissingResources)

# Default list of recipes. See SmallBodRecipe. You can use these, edit these, or just define your own.
RECIPES = [
    
    ############################ Tailoring ############################
    
    SmallBodRecipe("skullcap", CAT_TAILORING_HATS, 2, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("bandana", CAT_TAILORING_HATS, 9, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("floppy hat", CAT_TAILORING_HATS, 16, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("cap", CAT_TAILORING_HATS, 23, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("wide-brim hat", CAT_TAILORING_HATS, 30, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("straw hat", CAT_TAILORING_HATS, 37, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("tall straw hat", CAT_TAILORING_HATS, 44, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("wizard's hat", CAT_TAILORING_HATS, 51, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ), # grr'
    SmallBodRecipe("bonnet", CAT_TAILORING_HATS, 58, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("feathered hat", CAT_TAILORING_HATS, 65, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("tricorne hat", CAT_TAILORING_HATS, 72, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ), # should be 72
    SmallBodRecipe("jester hat", CAT_TAILORING_HATS, 79, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("flower garland", CAT_TAILORING_HATS, 86, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    
    SmallBodRecipe("doublet", CAT_TAILORING_SHIRTS_AND_PANTS, 2, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("shirt", CAT_TAILORING_SHIRTS_AND_PANTS, 9, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("fancy shirt", CAT_TAILORING_SHIRTS_AND_PANTS, 16, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("tunic", CAT_TAILORING_SHIRTS_AND_PANTS, 23, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("surcoat", CAT_TAILORING_SHIRTS_AND_PANTS, 30, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("plain dress", CAT_TAILORING_SHIRTS_AND_PANTS, 37, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("fancy dress", CAT_TAILORING_SHIRTS_AND_PANTS, 44, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("cloak", CAT_TAILORING_SHIRTS_AND_PANTS, 51, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("robe", CAT_TAILORING_SHIRTS_AND_PANTS, 58, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("jester suit", CAT_TAILORING_SHIRTS_AND_PANTS, 65, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("fur cape", CAT_TAILORING_SHIRTS_AND_PANTS, 72, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_SHIRTS_AND_PANTS, 79, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_SHIRTS_AND_PANTS, 86, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_SHIRTS_AND_PANTS, 93, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("long pants", CAT_TAILORING_SHIRTS_AND_PANTS, 142, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("kilt", CAT_TAILORING_SHIRTS_AND_PANTS, 149, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("skirt", CAT_TAILORING_SHIRTS_AND_PANTS, 156, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    
    SmallBodRecipe("body sash", CAT_TAILORING_MISCELLANEOUS, 2, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("half apron", CAT_TAILORING_MISCELLANEOUS, 9, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("full apron", CAT_TAILORING_MISCELLANEOUS, 16, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_TAILORING_MISCELLANEOUS, 23, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_TAILORING_MISCELLANEOUS, 30, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_TAILORING_MISCELLANEOUS, 37, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_TAILORING_MISCELLANEOUS, 44, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_TAILORING_MISCELLANEOUS, 51, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_TAILORING_MISCELLANEOUS, 58, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_TAILORING_MISCELLANEOUS, 65, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_TAILORING_MISCELLANEOUS, 72, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_TAILORING_MISCELLANEOUS, 79, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_TAILORING_MISCELLANEOUS, 86, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_TAILORING_MISCELLANEOUS, 93, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    
    SmallBodRecipe("elven boots", CAT_TAILORING_FOOTWEAR, 2, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    SmallBodRecipe("fur boots", CAT_TAILORING_FOOTWEAR, 9, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_FOOTWEAR, 16, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_FOOTWEAR, 23, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("sandals", CAT_TAILORING_FOOTWEAR, 30, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    SmallBodRecipe("shoes", CAT_TAILORING_FOOTWEAR, 37, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    SmallBodRecipe("boots", CAT_TAILORING_FOOTWEAR, 44, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    SmallBodRecipe("thigh boots", CAT_TAILORING_FOOTWEAR, 51, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_FOOTWEAR, 58, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    SmallBodRecipe("jester shoes", CAT_TAILORING_FOOTWEAR, 65, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_FOOTWEAR, 72, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_FOOTWEAR, 79, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_FOOTWEAR, 86, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_FOOTWEAR, 93, TAILORING_TOOL_STATIC_ID, [SmallBodResource(CLOTH_STATIC_ID)] ),
    
    #SmallBodRecipe("00000000", CAT_TAILORING_LEATHER_ARMOR, 2, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_LEATHER_ARMOR, 9, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_LEATHER_ARMOR, 16, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    SmallBodRecipe("leather gorget", CAT_TAILORING_LEATHER_ARMOR, 23, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    SmallBodRecipe("leather cap", CAT_TAILORING_LEATHER_ARMOR, 30, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    SmallBodRecipe("leather gloves", CAT_TAILORING_LEATHER_ARMOR, 37, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    SmallBodRecipe("leather sleeves", CAT_TAILORING_LEATHER_ARMOR, 44, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    SmallBodRecipe("leather leggings", CAT_TAILORING_LEATHER_ARMOR, 51, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    SmallBodRecipe("leather tunic", CAT_TAILORING_LEATHER_ARMOR, 58, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_LEATHER_ARMOR, 65, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_LEATHER_ARMOR, 72, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_LEATHER_ARMOR, 79, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_LEATHER_ARMOR, 86, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_LEATHER_ARMOR, 93, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    
    SmallBodRecipe("studded gorget", CAT_TAILORING_STUDDED_ARMOR, 2, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    SmallBodRecipe("studded gloves", CAT_TAILORING_STUDDED_ARMOR, 9, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    SmallBodRecipe("studded sleeves", CAT_TAILORING_STUDDED_ARMOR, 16, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    SmallBodRecipe("studded leggings", CAT_TAILORING_STUDDED_ARMOR, 23, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    SmallBodRecipe("studded tunic", CAT_TAILORING_STUDDED_ARMOR, 30, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_STUDDED_ARMOR, 37, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_STUDDED_ARMOR, 44, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_STUDDED_ARMOR, 51, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_STUDDED_ARMOR, 58, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_STUDDED_ARMOR, 65, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_STUDDED_ARMOR, 72, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_STUDDED_ARMOR, 79, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_STUDDED_ARMOR, 86, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_STUDDED_ARMOR, 93, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    
    SmallBodRecipe("leather shorts", CAT_TAILORING_FEMALE_ARMOR, 2, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    SmallBodRecipe("leather skirt", CAT_TAILORING_FEMALE_ARMOR, 9, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    SmallBodRecipe("leather bustier", CAT_TAILORING_FEMALE_ARMOR, 16, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    SmallBodRecipe("studded bustier", CAT_TAILORING_FEMALE_ARMOR, 23, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    SmallBodRecipe("female leather armor", CAT_TAILORING_FEMALE_ARMOR, 30, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    SmallBodRecipe("studded armor", CAT_TAILORING_FEMALE_ARMOR, 37, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_FEMALE_ARMOR, 44, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_FEMALE_ARMOR, 51, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_FEMALE_ARMOR, 58, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_FEMALE_ARMOR, 65, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_FEMALE_ARMOR, 72, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_FEMALE_ARMOR, 79, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_FEMALE_ARMOR, 86, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),
    #SmallBodRecipe("00000000", CAT_TAILORING_FEMALE_ARMOR, 93, TAILORING_TOOL_STATIC_ID, [SmallBodResource(LEATHER_STATIC_ID)] ),

    ############################ Alchemy ############################
    
    SmallBodRecipe("Refresh potion", CAT_ALCHEMY_HEALING_AND_CURATIVE, 2, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(BLACKPEARL, 1) ] ),
    SmallBodRecipe("Greater Refreshment potion", CAT_ALCHEMY_HEALING_AND_CURATIVE, 9, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(BLACKPEARL, 5) ] ),
    SmallBodRecipe("Lesser Heal potion", CAT_ALCHEMY_HEALING_AND_CURATIVE, 16, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(GINSENG, 1) ] ),
    SmallBodRecipe("Heal potion", CAT_ALCHEMY_HEALING_AND_CURATIVE, 23, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(GINSENG, 3) ] ),
    SmallBodRecipe("Greater Heal potion", CAT_ALCHEMY_HEALING_AND_CURATIVE, 30, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(GINSENG, 7) ] ),
    SmallBodRecipe("Lesser Cure ", CAT_ALCHEMY_HEALING_AND_CURATIVE, 37, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(GARLIC, 1) ] ),
    SmallBodRecipe("Cure potion", CAT_ALCHEMY_HEALING_AND_CURATIVE, 44, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(GARLIC, 3) ] ),
    SmallBodRecipe("Greater Cure potion", CAT_ALCHEMY_HEALING_AND_CURATIVE, 51, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(GARLIC, 6) ] ),
    #SmallBodRecipe("00000000", CAT_ALCHEMY_HEALING_AND_CURATIVE, 58, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(00000000000000, 1) ] ),
    #SmallBodRecipe("00000000", CAT_ALCHEMY_HEALING_AND_CURATIVE, 65, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(00000000000000, 1) ] ),
    #SmallBodRecipe("00000000", CAT_ALCHEMY_HEALING_AND_CURATIVE, 72, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(00000000000000, 1) ] ),
    #SmallBodRecipe("00000000", CAT_ALCHEMY_HEALING_AND_CURATIVE, 79, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(00000000000000, 1) ] ),
    #SmallBodRecipe("00000000", CAT_ALCHEMY_HEALING_AND_CURATIVE, 86, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID)], SmallBodResource(00000000000000, 1)  ),
    #SmallBodRecipe("00000000", CAT_ALCHEMY_HEALING_AND_CURATIVE, 93, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(00000000000000, 1) ] ),
    #SmallBodRecipe("00000000", CAT_ALCHEMY_HEALING_AND_CURATIVE, 142, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(00000000000000, 1) ] ),
    #SmallBodRecipe("00000000", CAT_ALCHEMY_HEALING_AND_CURATIVE, 149, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID), SmallBodResource(00000000000000, 1) ] ),
    #SmallBodRecipe("00000000", CAT_ALCHEMY_HEALING_AND_CURATIVE, 156, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID), SmallBodResource(00000000000000, 1) ] ),

    SmallBodRecipe("Agility potion", CAT_ALCHEMY_ENHANCEMENT, 2, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(BLOODMOSS, 1) ] ),
    SmallBodRecipe("Greater Agility potion", CAT_ALCHEMY_ENHANCEMENT, 9, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(BLOODMOSS, 3) ] ),
    SmallBodRecipe("Night Sight potion", CAT_ALCHEMY_ENHANCEMENT, 16, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(SPIDERSILK, 1) ] ),
    SmallBodRecipe("Strength potion", CAT_ALCHEMY_ENHANCEMENT, 23, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(MANDRAKEROOT, 2) ] ),
    SmallBodRecipe("Greater Strength potion", CAT_ALCHEMY_ENHANCEMENT, 30, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(MANDRAKEROOT, 5) ] ),
    SmallBodRecipe("Invisibility potion", CAT_ALCHEMY_ENHANCEMENT, 37, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(BLOODMOSS, 4), SmallBodResource(NIGHTSHADE, 3) ] ),
    #SmallBodRecipe("00000000", CAT_ALCHEMY_ENHANCEMENT, 44, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(00000000000000, 1) ] ),
    #SmallBodRecipe("00000000", CAT_ALCHEMY_ENHANCEMENT, 51, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(00000000000000, 1) ] ),
    #SmallBodRecipe("00000000", CAT_ALCHEMY_ENHANCEMENT, 58, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(00000000000000, 1) ] ),
    #SmallBodRecipe("00000000", CAT_ALCHEMY_ENHANCEMENT, 65, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(00000000000000, 1) ] ),
    #SmallBodRecipe("00000000", CAT_ALCHEMY_ENHANCEMENT, 72, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(00000000000000, 1) ] ),
    #SmallBodRecipe("00000000", CAT_ALCHEMY_ENHANCEMENT, 79, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(00000000000000, 1) ] ),
    #SmallBodRecipe("00000000", CAT_ALCHEMY_ENHANCEMENT, 86, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID)], SmallBodResource(00000000000000, 1)  ),
    #SmallBodRecipe("00000000", CAT_ALCHEMY_ENHANCEMENT, 93, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(00000000000000, 1) ] ),
    #SmallBodRecipe("00000000", CAT_ALCHEMY_ENHANCEMENT, 142, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(00000000000000, 1) ] ),
    #SmallBodRecipe("00000000", CAT_ALCHEMY_ENHANCEMENT, 149, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID), SmallBodResource(00000000000000, 1) ] ),
    #SmallBodRecipe("00000000", CAT_ALCHEMY_ENHANCEMENT, 156, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID), SmallBodResource(00000000000000, 1) ] ),    

    SmallBodRecipe("Lesser Poison potion", CAT_ALCHEMY_TOXIC, 2, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(NIGHTSHADE, 1) ] ),
    SmallBodRecipe("Poison potion", CAT_ALCHEMY_TOXIC, 9, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(NIGHTSHADE, 2) ] ),
    SmallBodRecipe("Greater Poison potion", CAT_ALCHEMY_TOXIC, 16, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(NIGHTSHADE, 4) ] ),
    SmallBodRecipe("Deadly Poison potion", CAT_ALCHEMY_TOXIC, 23, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(NIGHTSHADE, 8) ] ),
    #SmallBodRecipe("00000000", CAT_ALCHEMY_TOXIC, 30, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(00000000000000, 1) ] ),
    #SmallBodRecipe("00000000", CAT_ALCHEMY_TOXIC, 37, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(00000000000000, 1), SmallBodResource(NIGHTSHADE, 3) ] ),
    #SmallBodRecipe("00000000", CAT_ALCHEMY_TOXIC, 44, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(00000000000000, 1) ] ),
    #SmallBodRecipe("00000000", CAT_ALCHEMY_TOXIC, 51, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(00000000000000, 1) ] ),
    #SmallBodRecipe("00000000", CAT_ALCHEMY_TOXIC, 58, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(00000000000000, 1) ] ),
  
    SmallBodRecipe("Lesser Explosion potion", CAT_ALCHEMY_EXPLOSIVE, 2, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(SULPHUROUSASH, 3) ] ),
    SmallBodRecipe("Explosion potion", CAT_ALCHEMY_EXPLOSIVE, 9, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(SULPHUROUSASH, 5) ] ),
    SmallBodRecipe("Greater Explosion potion", CAT_ALCHEMY_EXPLOSIVE, 16, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(SULPHUROUSASH, 10) ] ),
    SmallBodRecipe("Conflagaration potion", CAT_ALCHEMY_EXPLOSIVE, 23, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(GRAVEDUST, 5) ] ),
    SmallBodRecipe("Greater Conflagaration potion", CAT_ALCHEMY_EXPLOSIVE, 30, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(GRAVEDUST, 10) ] ),
    SmallBodRecipe("Confusion Blast potion", CAT_ALCHEMY_EXPLOSIVE, 37, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(PIGIRON, 5) ] ),
    SmallBodRecipe("Greater Confusion Blast potion", CAT_ALCHEMY_EXPLOSIVE, 44, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(PIGIRON, 10) ] ),
    #SmallBodRecipe("00000000", CAT_ALCHEMY_EXPLOSIVE, 51, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(00000000000000, 1) ] ),
    #SmallBodRecipe("00000000", CAT_ALCHEMY_EXPLOSIVE, 58, ALCHEMY_TOOL_STATIC_ID, [SmallBodResource(EMPTY_BOTTLE_STATIC_ID, 1), SmallBodResource(00000000000000, 1) ] ),
    
    #CAT_INSCRIPTION_FIRST_SECOND = 1
    #CAT_INSCRIPTION_THIRD_FOURTH = 8
    #CAT_INSCRIPTION_FIFTH_SIXTH = 15
    #CAT_INSCRIPTION_SEVENTH_EIGTH = 22
    #CAT_INSCRIPTION_NECRO = 29
    #CAT_INSCRIPTION_OTHER = 36
    #CAT_INSCRIPTION_MYSTICISM = 43    
        
    #SmallBodResource(MANDRAKEROOT, 10)
    #SmallBodResource(BLOODMOSS, 10)
    #SmallBodResource(SULPHUROUSASH, 10)
    #SmallBodResource(NIGHTSHADE, 10)
    #SmallBodResource(BLACKPEARL, 10)
    #SmallBodResource(SPIDERSILK, 10)
    #SmallBodResource(GINSENG, 10)
    #SmallBodResource(GARLIC, 10)
    #SmallBodResource(PIGIRON, 10)
    #SmallBodResource(BATWING, 10)
    #SmallBodResource(NOXCRYSTAL, 10)
    #SmallBodResource(DAEMONBLOOD, 10)
    #SmallBodResource(GRAVEDUST, 10)
    
    ############################ Inscription ############################
    
    SmallBodRecipe("00000000", CAT_INSCRIPTION_FIRST_SECOND, 2, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("Clumsy", CAT_INSCRIPTION_FIRST_SECOND, 9, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(BLOODMOSS, 1), SmallBodResource(NIGHTSHADE, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_FIRST_SECOND, 16, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("Feeblemind", CAT_INSCRIPTION_FIRST_SECOND, 23, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(NIGHTSHADE, 1), SmallBodResource(GINSENG, 1) ] ),
    SmallBodRecipe("Heal", CAT_INSCRIPTION_FIRST_SECOND, 30, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(GARLIC, 1), SmallBodResource(GINSENG, 1), SmallBodResource(SPIDERSILK, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_FIRST_SECOND, 37, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1), SmallBodResource(00000000, 3) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_FIRST_SECOND, 44, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("Weaken", CAT_INSCRIPTION_FIRST_SECOND, 51, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(NIGHTSHADE, 1), SmallBodResource(GARLIC, 1) ] ),
    SmallBodRecipe("Agility", CAT_INSCRIPTION_FIRST_SECOND, 58, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(BLOODMOSS, 1), SmallBodResource(MANDRAKEROOT, 1) ] ),
    SmallBodRecipe("Cunning", CAT_INSCRIPTION_FIRST_SECOND, 65, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(NIGHTSHADE, 1), SmallBodResource(MANDRAKEROOT, 1) ] ),
    SmallBodRecipe("Cure", CAT_INSCRIPTION_FIRST_SECOND, 72, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(GARLIC, 1), SmallBodResource(GARLIC, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_FIRST_SECOND, 79, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(GARLIC, 1), SmallBodResource(GINSENG, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_FIRST_SECOND, 86, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(NIGHTSHADE, 1), SmallBodResource(MANDRAKEROOT, 1) ]  ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_FIRST_SECOND, 93, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_FIRST_SECOND, 100, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("Strength", CAT_INSCRIPTION_FIRST_SECOND, 107, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(NIGHTSHADE, 1), SmallBodResource(MANDRAKEROOT, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_FIRST_SECOND, 114, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_FIRST_SECOND, 121, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_FIRST_SECOND, 128, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_FIRST_SECOND, 142, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_FIRST_SECOND, 149, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_FIRST_SECOND, 156, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),  
    
    SmallBodRecipe("00000000", CAT_INSCRIPTION_THIRD_FOURTH, 2, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_THIRD_FOURTH, 9, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_THIRD_FOURTH, 16, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_THIRD_FOURTH, 23, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_THIRD_FOURTH, 30, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_THIRD_FOURTH, 37, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1), SmallBodResource(NIGHTSHADE, 3) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_THIRD_FOURTH, 44, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_THIRD_FOURTH, 51, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_THIRD_FOURTH, 58, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_THIRD_FOURTH, 65, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("Curse", CAT_INSCRIPTION_THIRD_FOURTH, 72, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(GARLIC, 1), SmallBodResource(NIGHTSHADE, 1), SmallBodResource(SULPHUROUSASH, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_THIRD_FOURTH, 79, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("Greater Heal", CAT_INSCRIPTION_THIRD_FOURTH, 86, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(GARLIC, 1), SmallBodResource(SPIDERSILK, 1), SmallBodResource(MANDRAKEROOT, 1), SmallBodResource(GINSENG, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_THIRD_FOURTH, 93, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_THIRD_FOURTH, 100, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("Recall", CAT_INSCRIPTION_THIRD_FOURTH, 107, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(BLACKPEARL, 1), SmallBodResource(BLOODMOSS, 1), SmallBodResource(MANDRAKEROOT, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_THIRD_FOURTH, 114, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_THIRD_FOURTH, 121, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_THIRD_FOURTH, 128, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_THIRD_FOURTH, 142, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_THIRD_FOURTH, 149, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_THIRD_FOURTH, 156, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ), 
    
    #SmallBodResource(MANDRAKEROOT, 10)
    #SmallBodResource(BLOODMOSS, 10)
    #SmallBodResource(SULPHUROUSASH, 10)
    #SmallBodResource(NIGHTSHADE, 10)
    #SmallBodResource(BLACKPEARL, 10)
    #SmallBodResource(SPIDERSILK, 10)
    #SmallBodResource(GINSENG, 10)
    #SmallBodResource(GARLIC, 10)
    #SmallBodResource(PIGIRON, 10)
    #SmallBodResource(BATWING, 10)
    #SmallBodResource(NOXCRYSTAL, 10)
    #SmallBodResource(DAEMONBLOOD, 10)
    #SmallBodResource(GRAVEDUST, 10)
    
    SmallBodRecipe("Blade Spirits", CAT_INSCRIPTION_FIFTH_SIXTH, 2, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(BLACKPEARL, 1), SmallBodResource(NIGHTSHADE, 1), SmallBodResource(MANDRAKEROOT, 1) ] ),
    SmallBodRecipe("Dispel Field", CAT_INSCRIPTION_FIFTH_SIXTH, 9, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(BLACKPEARL, 1), SmallBodResource(GARLIC, 1), SmallBodResource(SPIDERSILK, 1), SmallBodResource(SULPHUROUSASH, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_FIFTH_SIXTH, 16, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("Magic Reflection", CAT_INSCRIPTION_FIFTH_SIXTH, 23, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(GARLIC, 1), SmallBodResource(MANDRAKEROOT, 1), SmallBodResource(SPIDERSILK, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_FIFTH_SIXTH, 30, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("Paralyze", CAT_INSCRIPTION_FIFTH_SIXTH, 37, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(GARLIC, 1), SmallBodResource(MANDRAKEROOT, 1), SmallBodResource(SPIDERSILK, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_FIFTH_SIXTH, 44, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("Summon Creature", CAT_INSCRIPTION_FIFTH_SIXTH, 51, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(BLOODMOSS, 1), SmallBodResource(MANDRAKEROOT, 1), SmallBodResource(SPIDERSILK, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_FIFTH_SIXTH, 58, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_FIFTH_SIXTH, 65, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_FIFTH_SIXTH, 72, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_FIFTH_SIXTH, 79, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_FIFTH_SIXTH, 86, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_FIFTH_SIXTH, 93, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_FIFTH_SIXTH, 100, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_FIFTH_SIXTH, 107, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_FIFTH_SIXTH, 114, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_FIFTH_SIXTH, 121, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_FIFTH_SIXTH, 128, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_FIFTH_SIXTH, 142, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_FIFTH_SIXTH, 149, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_FIFTH_SIXTH, 156, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ), 

    SmallBodRecipe("00000000", CAT_INSCRIPTION_SEVENTH_EIGTH, 2, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_SEVENTH_EIGTH, 9, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_SEVENTH_EIGTH, 16, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_SEVENTH_EIGTH, 23, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_SEVENTH_EIGTH, 30, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_SEVENTH_EIGTH, 37, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1), SmallBodResource(NIGHTSHADE, 3) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_SEVENTH_EIGTH, 44, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_SEVENTH_EIGTH, 51, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_SEVENTH_EIGTH, 58, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_SEVENTH_EIGTH, 65, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_SEVENTH_EIGTH, 72, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_SEVENTH_EIGTH, 79, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_SEVENTH_EIGTH, 86, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_SEVENTH_EIGTH, 93, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_SEVENTH_EIGTH, 100, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_SEVENTH_EIGTH, 107, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_SEVENTH_EIGTH, 114, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_SEVENTH_EIGTH, 121, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_SEVENTH_EIGTH, 128, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_SEVENTH_EIGTH, 142, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_SEVENTH_EIGTH, 149, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_SEVENTH_EIGTH, 156, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ), 

    #SmallBodResource(MANDRAKEROOT, 10)
    #SmallBodResource(BLOODMOSS, 10)
    #SmallBodResource(SULPHUROUSASH, 10)
    #SmallBodResource(NIGHTSHADE, 10)
    #SmallBodResource(BLACKPEARL, 10)
    #SmallBodResource(SPIDERSILK, 10)
    #SmallBodResource(GINSENG, 10)
    #SmallBodResource(GARLIC, 10)
    #SmallBodResource(PIGIRON, 10)
    #SmallBodResource(BATWING, 10)
    #SmallBodResource(NOXCRYSTAL, 10)
    #SmallBodResource(DAEMONBLOOD, 10)
    #SmallBodResource(GRAVEDUST, 10)
    
    SmallBodRecipe("Animate Dead", CAT_INSCRIPTION_NECRO, 2, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(GRAVEDUST, 1), SmallBodResource(DAEMONBLOOD, 1) ] ),
    SmallBodRecipe("Blood Oath", CAT_INSCRIPTION_NECRO, 9, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(DAEMONBLOOD, 1) ] ),
    SmallBodRecipe("Corpse Skin", CAT_INSCRIPTION_NECRO, 16, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(BATWING, 1), SmallBodResource(GRAVEDUST, 1) ] ),
    SmallBodRecipe("Curse Weapon", CAT_INSCRIPTION_NECRO, 23, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(PIGIRON, 1) ] ),
    SmallBodRecipe("Evil Omen", CAT_INSCRIPTION_NECRO, 30, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(BATWING, 1), SmallBodResource(NOXCRYSTAL, 1) ] ),
    SmallBodRecipe("Horrific Beast", CAT_INSCRIPTION_NECRO, 37, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(BATWING, 1), SmallBodResource(DAEMONBLOOD, 3) ] ),
    SmallBodRecipe("Mind Rot", CAT_INSCRIPTION_NECRO, 44, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(BATWING, 1), SmallBodResource(DAEMONBLOOD, 1), SmallBodResource(PIGIRON, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_NECRO, 51, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("Pain Spike", CAT_INSCRIPTION_NECRO, 58, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(GRAVEDUST, 1), SmallBodResource(PIGIRON, 1) ] ),
    SmallBodRecipe("Poison Strike", CAT_INSCRIPTION_NECRO, 65, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(NOXCRYSTAL, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_NECRO, 72, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("Summon Familiar", CAT_INSCRIPTION_NECRO, 79, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(BATWING, 1), SmallBodResource(GRAVEDUST, 1), SmallBodResource(PIGIRON, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_NECRO, 86, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_NECRO, 93, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("Wither", CAT_INSCRIPTION_NECRO, 100, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(GRAVEDUST, 1), SmallBodResource(NOXCRYSTAL, 1), SmallBodResource(PIGIRON, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_NECRO, 107, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_NECRO, 114, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_NECRO, 121, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_NECRO, 128, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_NECRO, 142, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_NECRO, 149, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_NECRO, 156, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ), 

    SmallBodRecipe("00000000", CAT_INSCRIPTION_OTHER, 2, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_OTHER, 9, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_OTHER, 16, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_OTHER, 23, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_OTHER, 30, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_OTHER, 37, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1), SmallBodResource(NIGHTSHADE, 3) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_OTHER, 44, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_OTHER, 51, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_OTHER, 58, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_OTHER, 65, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_OTHER, 72, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_OTHER, 79, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_OTHER, 86, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_OTHER, 93, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_OTHER, 100, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_OTHER, 107, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_OTHER, 114, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_OTHER, 121, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_OTHER, 128, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_OTHER, 142, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_OTHER, 149, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),
    SmallBodRecipe("00000000", CAT_INSCRIPTION_OTHER, 156, INSCRIPTION_TOOL_STATIC_ID, [SmallBodResource(BLANK_SCROLL, 1), SmallBodResource(00000000000000, 1) ] ),     
    
    #CAT_CARPENTRY_OTHER = 1
    #CAT_CARPENTRY_FURNITURE = 8
    #CAT_CARPENTRY_CONTAINERS = 15
    #CAT_CARPENTRY_WEAPONS = 22
    #CAT_CARPENTRY_ARMOR = 29
    #CAT_CARPENTRY_INSTRUMENTS = 36
    #CAT_CARPENTRY_MISC_ADDONS = 43
    #CAT_CARPENTRY_TAILORING_AND_COOKING = 50
    #CAT_CARPENTRY_ANVILS_AND_FORGES = 57
    #CAT_CARPENTRY_TRAINING = 64    

    ############################ Carpentry ############################
    
    SmallBodRecipe("foot stool", CAT_CARPENTRY_FURNITURE, 2, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("stool", CAT_CARPENTRY_FURNITURE, 9, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("straw chair", CAT_CARPENTRY_FURNITURE, 16, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("wooden chair", CAT_CARPENTRY_FURNITURE, 23, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_FURNITURE, 30, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_FURNITURE, 37, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("wooden bench", CAT_CARPENTRY_FURNITURE, 44, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("wooden throne", CAT_CARPENTRY_FURNITURE, 51, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_FURNITURE, 58, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("smal table", CAT_CARPENTRY_FURNITURE, 65, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_FURNITURE, 72, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_FURNITURE, 79, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("large table", CAT_CARPENTRY_FURNITURE, 86, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_FURNITURE, 93, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    
    SmallBodRecipe("wooden box", CAT_CARPENTRY_CONTAINERS, 2, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("Small Crate", CAT_CARPENTRY_CONTAINERS, 9, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("medium crate", CAT_CARPENTRY_CONTAINERS, 16, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("large crate", CAT_CARPENTRY_CONTAINERS, 23, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("wooden chest", CAT_CARPENTRY_CONTAINERS, 30, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("wooden shelf", CAT_CARPENTRY_CONTAINERS, 37, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_CONTAINERS, 44, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("armoire", CAT_CARPENTRY_CONTAINERS, 51, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("plain wooden chest", CAT_CARPENTRY_CONTAINERS, 58, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_CONTAINERS, 65, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_CONTAINERS, 72, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_CONTAINERS, 79, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_CONTAINERS, 86, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_CONTAINERS, 93, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    
    SmallBodRecipe("shelpherd's crook", CAT_CARPENTRY_WEAPONS, 2, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ), #'
    SmallBodRecipe("quarter staff", CAT_CARPENTRY_WEAPONS, 9, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("gnarled staff", CAT_CARPENTRY_WEAPONS, 16, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("bokuto", CAT_CARPENTRY_WEAPONS, 23, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_WEAPONS, 30, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_WEAPONS, 37, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("wild staff", CAT_CARPENTRY_WEAPONS, 44, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_WEAPONS, 51, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("arcanist's wild staff", CAT_CARPENTRY_WEAPONS, 58, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ), # '
    SmallBodRecipe("ancient wild staff", CAT_CARPENTRY_WEAPONS, 65, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("thorned wild staff", CAT_CARPENTRY_WEAPONS, 72, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("hardened wild staff", CAT_CARPENTRY_WEAPONS, 79, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_WEAPONS, 86, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_WEAPONS, 93, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    
    SmallBodRecipe("00000000", CAT_CARPENTRY_ARMOR, 2, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_ARMOR, 9, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_ARMOR, 16, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_ARMOR, 23, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_ARMOR, 30, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_ARMOR, 37, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_ARMOR, 44, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_ARMOR, 51, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_ARMOR, 58, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_ARMOR, 65, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_ARMOR, 72, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_ARMOR, 79, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_ARMOR, 86, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_ARMOR, 93, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    
    SmallBodRecipe("00000000", CAT_CARPENTRY_INSTRUMENTS, 2, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_INSTRUMENTS, 9, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_INSTRUMENTS, 16, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_INSTRUMENTS, 23, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_INSTRUMENTS, 30, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_INSTRUMENTS, 37, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_INSTRUMENTS, 44, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_INSTRUMENTS, 51, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_INSTRUMENTS, 58, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_INSTRUMENTS, 65, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_INSTRUMENTS, 72, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_INSTRUMENTS, 79, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_INSTRUMENTS, 86, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    SmallBodRecipe("00000000", CAT_CARPENTRY_INSTRUMENTS, 93, CARPENTRY_TOOL_STATIC_ID, [SmallBodResource(BOARD_STATIC_ID)] ),
    
    ############################ Blacksmith ############################
    
    # Metal Armor
    SmallBodRecipe("ringmail gloves", CAT_BLACKSMITHY_METAL_ARMOR, 2, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("ringmail leggings", CAT_BLACKSMITHY_METAL_ARMOR, 9, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("ringmail sleeves", CAT_BLACKSMITHY_METAL_ARMOR, 16, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("ringmail tunic", CAT_BLACKSMITHY_METAL_ARMOR, 23, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("chainmail coif", CAT_BLACKSMITHY_METAL_ARMOR, 30, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("chainmail leggings", CAT_BLACKSMITHY_METAL_ARMOR, 37, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("chainmail tunic", CAT_BLACKSMITHY_METAL_ARMOR, 44, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("platemail arms", CAT_BLACKSMITHY_METAL_ARMOR, 51, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("platemail gloves", CAT_BLACKSMITHY_METAL_ARMOR, 58, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("platemail gorget", CAT_BLACKSMITHY_METAL_ARMOR, 65, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("platemail legs", CAT_BLACKSMITHY_METAL_ARMOR, 72, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("platemail tunic", CAT_BLACKSMITHY_METAL_ARMOR, 79, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("female plate", CAT_BLACKSMITHY_METAL_ARMOR, 86, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    
    # Helmets
    SmallBodRecipe("bascinet", CAT_BLACKSMITHY_HELMETS, 2, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("close helmet", CAT_BLACKSMITHY_HELMETS, 9, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("helmet", CAT_BLACKSMITHY_HELMETS, 16, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("norse helm", CAT_BLACKSMITHY_HELMETS, 23, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("plate helm", CAT_BLACKSMITHY_HELMETS, 30, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    
    # Shields
    SmallBodRecipe("buckler", CAT_BLACKSMITHY_SHIELDS, 2, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("bronze shield", CAT_BLACKSMITHY_SHIELDS, 9, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("heater shield", CAT_BLACKSMITHY_SHIELDS, 16, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("metal shield", CAT_BLACKSMITHY_SHIELDS, 23, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("metal kite shield", CAT_BLACKSMITHY_SHIELDS, 30, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("tear kite shield", CAT_BLACKSMITHY_SHIELDS, 37, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("chaos shield", CAT_BLACKSMITHY_SHIELDS, 44, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("order shield", CAT_BLACKSMITHY_SHIELDS, 51, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("small plate shield", CAT_BLACKSMITHY_SHIELDS, 58, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("large plate shield", CAT_BLACKSMITHY_SHIELDS, 72, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("medium plate shield", CAT_BLACKSMITHY_SHIELDS, 79, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    
    # Bladed
    SmallBodRecipe("broadsword", CAT_BLACKSMITHY_BLADED, 9, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("cutlass", CAT_BLACKSMITHY_BLADED, 23, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("dagger", CAT_BLACKSMITHY_BLADED, 30, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("katana", CAT_BLACKSMITHY_BLADED, 37, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("kryss", CAT_BLACKSMITHY_BLADED, 44, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("longsword", CAT_BLACKSMITHY_BLADED, 51, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("scimitar", CAT_BLACKSMITHY_BLADED, 58, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("viking sword", CAT_BLACKSMITHY_BLADED, 65, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    
    # Axes
    SmallBodRecipe("axe", CAT_BLACKSMITHY_AXES, 2, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("battle axe", CAT_BLACKSMITHY_AXES, 9, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("double axe", CAT_BLACKSMITHY_AXES, 16, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("executioner's axe", CAT_BLACKSMITHY_AXES, 23, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ), #'
    SmallBodRecipe("large battle axe", CAT_BLACKSMITHY_AXES, 30, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("two handed axe", CAT_BLACKSMITHY_AXES, 37, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("war axe", CAT_BLACKSMITHY_AXES, 44, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    
    # Polearms
    SmallBodRecipe("bardiche", CAT_BLACKSMITHY_POLEARMS, 2, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("bladed staff", CAT_BLACKSMITHY_POLEARMS, 9, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("double bladed staff", CAT_BLACKSMITHY_POLEARMS, 16, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("halberd", CAT_BLACKSMITHY_POLEARMS, 23, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("lance", CAT_BLACKSMITHY_POLEARMS, 30, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("pike", CAT_BLACKSMITHY_POLEARMS, 37, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("short spear", CAT_BLACKSMITHY_POLEARMS, 44, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("scythe", CAT_BLACKSMITHY_POLEARMS, 51, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("spear", CAT_BLACKSMITHY_POLEARMS, 58, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("war fork", CAT_BLACKSMITHY_POLEARMS, 65, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    
    # Bashing
    SmallBodRecipe("hammer pick", CAT_BLACKSMITHY_BASHING, 2, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("mace", CAT_BLACKSMITHY_BASHING, 9, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("maul", CAT_BLACKSMITHY_BASHING, 16, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("scepter", CAT_BLACKSMITHY_BASHING, 23, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("war mace", CAT_BLACKSMITHY_BASHING, 30, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
    SmallBodRecipe("war hammer", CAT_BLACKSMITHY_BASHING, 37, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID)] ),
]

# Item property Number for important props within a bod item in game
PROD_ID_LARGE_BULK_ORDER = 1060655
PROP_ID_SMALL_BULK_ORDER = 1060654 
PROP_ID_AMOUNT_TO_MAKE = 1060656
PROP_ID_EXCEPTIONAL = 1045141
PROP_ID_ITEM_TEXT = 1060658

# This goes prop.Number -> { gump button id, special resource hue }
# ServUO\Scripts\Services\BulkOrders\SmallBODs\SmallBODGump.cs
# Tried doing a regex by special material name, e.g. All items must be made
# with Dull Copper Ingots, but it didnt follow that convetion for carpenty.
# It just said "Oak". So, I got mad and just did an exact match for the 
# Propert.Number. Whatever.
SPECIAL_PROP_MATERIAL_MAP = {
    1045142: { "button": 13, "hue": RESOURCE_HUE_DULL_COPPER,   "name": "dull copper" },    # Dull Copper
    1045143: { "button": 20, "hue": RESOURCE_HUE_SHADOW_IRON,   "name": "shadow iron" },    # Shadow Iron
    1045144: { "button": 27, "hue": RESOURCE_HUE_COPPER,        "name": "copper" },         # Copper
    1045145: { "button": 34, "hue": RESOURCE_HUE_BRONZE,        "name": "bronze" },         # Bronze
    1045146: { "button": 41, "hue": RESOURCE_HUE_GOLD,          "name": "gold" },           # Gold
    1045147: { "button": 48, "hue": RESOURCE_HUE_AGAPITE,       "name": "agapite" },        # Agapite
    1045148: { "button": 55, "hue": RESOURCE_HUE_VERITE,        "name": "verite" },         # Verite
    1045149: { "button": 62, "hue": RESOURCE_HUE_VALORITE,      "name": "valorite" },       # Valorite
    1049348: { "button": 13, "hue": RESOURCE_HUE_SPINED,        "name": "spined" },         # Spined
    1049349: { "button": 20, "hue": RESOURCE_HUE_HORNED,        "name": "horned" },         # Horned
    1049350: { "button": 27, "hue": RESOURCE_HUE_BARBED,        "name": "barbed" },         # Barbed
    1071428: { "button": 13, "hue": RESOURCE_HUE_OAK,           "name": None },             # Oak
    1071429: { "button": 20, "hue": RESOURCE_HUE_ASH,           "name": None },             # Ash
    1071430: { "button": 27, "hue": RESOURCE_HUE_YEW,           "name": None },             # Yew
    1071431: { "button": 34, "hue": RESOURCE_HUE_HEARTWOOD,     "name": None },       # Heartwood
    1071432: { "button": 41, "hue": RESOURCE_HUE_BLOODWOOD,     "name": None },       # Bloodwood
    1071433: { "button": 48, "hue": RESOURCE_HUE_FROSTWOOD,     "name": None },       # Frostwood
}
    
# Internal: Helper method to generate a small bod data structure.
def parse_small_bod(bod, recipes, alertMissingRecipe = False):
    isExceptional = False
    amountToMake = 0
    amountMade = 0
    recipe = None
    isSmallBod = False
    specialMaterialButton = 6 if bod.Color in [HUE_BLACKSMITHY, HUE_TAILORING, HUE_CARPENTRY, HUE_TINKERING] else 0
    specialMaterialHue = RESOURCE_HUE_DEFAULT
    specialMaterialPropId = None
    specialMaterialName = None
    for prop in bod.Properties:
        if prop.Number == PROP_ID_SMALL_BULK_ORDER:
            isSmallBod = True
        if prop.Number == PROP_ID_EXCEPTIONAL:
            isExceptional = True
        if prop.Number == PROP_ID_AMOUNT_TO_MAKE:
            amountToMake = int(prop.Args)
        if prop.Number in SPECIAL_PROP_MATERIAL_MAP:
            specialMaterialPropId = prop.Number
            specialMaterialButton = SPECIAL_PROP_MATERIAL_MAP[prop.Number]["button"]
            specialMaterialHue = SPECIAL_PROP_MATERIAL_MAP[prop.Number]["hue"]
            specialMaterialName = SPECIAL_PROP_MATERIAL_MAP[prop.Number]["name"]
        if prop.Number == PROP_ID_ITEM_TEXT:
            propList = prop.ToString().split(": ")
            itemName = propList[0].strip() # buckler looks like "buckler : <amount>" instead of "buckler: <amount>"
            amountMade = int(propList[1])
            if itemName in recipes:
                recipe = recipes[itemName]
                
    if recipe is not None and isSmallBod:
        craftedItemName = specialMaterialName + " " + recipe.itemName if specialMaterialName is not None else recipe.itemName
        return SmallBod(bod.Serial, craftedItemName, amountMade, isExceptional, amountToMake, specialMaterialButton, specialMaterialHue, specialMaterialPropId, recipe)
    elif isSmallBod == True and alertMissingRecipe:
        print("Warning: Skipping because not in recipe list")
        for prop in bod.Properties:
            print("\t", prop.ToString(), "(", prop.Number, ")")

# Internal: Build a data structure to check progress and get dependencies of large bod
def parse_large_bod(bod):
    isLargeBod = False
    smallBodItems = []
    specialMaterialPropId = None
    isExceptional = False
    amountToMake = 0
    for prop in bod.Properties:
        if prop.Number == PROD_ID_LARGE_BULK_ORDER:
            isLargeBod = True
        if prop.Number == PROP_ID_EXCEPTIONAL:
            isExceptional = True
        if prop.Number == PROP_ID_AMOUNT_TO_MAKE:
            amountToMake = int(prop.Args)
        if prop.Number in SPECIAL_PROP_MATERIAL_MAP:
            specialMaterialPropId = prop.Number
        if prop.Number in range(PROP_ID_ITEM_TEXT, PROP_ID_ITEM_TEXT + 6):    
            propList = prop.ToString().split(": ")
            itemName = propList[0].strip() # buckler looks like "buckler : <amount>" instead of "buckler: <amount>"
            amountMade = int(propList[1])
            smallBodItems.append({ "name": itemName, "amountMade": amountMade })
    if isLargeBod:
        return LargeBod(bod.Serial, isExceptional, amountToMake, specialMaterialPropId, smallBodItems)

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
            hue = smallBod.specialMaterialHue if resource.can_override_hue() and smallBod.specialMaterialHue is not None else RESOURCE_HUE_DEFAULT    
            items = Items.FindAllByID(resource.resourceId, hue, Player.Backpack.Serial, 0)

            amount = 0
            for item in items:
                amount = amount + item.Amount
            
            if amount >= resource.amount:
                break
        
            #print("Resources: {}/{}, getting more...".format(amount, resource.amount))
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
        items = Items.FindAllByID(resourceId, -1, Player.Backpack.Serial, 0)
        for item in items:
            keep = False
            for resource in smallBod.recipe.resources:
                hue = smallBod.specialMaterialHue if resource.can_override_hue() and smallBod.specialMaterialHue is not None else RESOURCE_HUE_DEFAULT    
                if item.ItemID == resource.resourceId and item.Color == hue:
                    keep = True
                    break
            if not keep:
                Items.Move(item, resourceContainer, item.Amount)    
                Misc.Pause(800)
    return True
    
# Internal: Helper method to salvage stuff.
def recycle(salvageBag, smallBod):
    if salvageBag is None or not smallBod.recipe.canSalvage():
        return None
    
    found = False        
    while True:
        item = Items.FindByName(smallBod.craftedItemName, -1, Player.Backpack.Serial, 0)
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
    
# Internal: Build database of small bods using itemName (not craftedItemName as PK)
# Data is structed as:
# "kryss": [ { "smallBod": 123, "smallBod": SmallBod }, ... ],
# "cutlass": [ { "smallBod": 123, "smallBod": SmallBod }, ... ],
def build_complete_small_bod_db(completeSmallBodContainers, recipes):
    db = {}
    itemsInDb = 0
    for completeSmallBodContainer in completeSmallBodContainers:
        bods = Items.FindAllByID(BOD_STATIC_ID, -1, completeSmallBodContainer, 1)
        for bod in bods:
            smallBod = parse_small_bod(bod, recipes)
            if smallBod is not None and smallBod.isComplete():
                if smallBod.recipe.itemName not in db:
                    db[smallBod.recipe.itemName] = []
                #db[smallBod.recipe.itemName].append({ "Serial": bod.Serial, "smallBod": smallBod })
                db[smallBod.recipe.itemName].append(smallBod)
                itemsInDb = itemsInDb + 1    
                    
    print("Database built with {} complete small bods".format(itemsInDb))
    return db

# Internal: Search our DB for a completed small bod
def search_complete_small_bod_db(db, largeBod):
    # smallBodItems.append({ "name": itemName, "amountMade": amountMade })
    entries = []
    for smallBodItem in largeBod.smallBodItems:
        if smallBodItem["amountMade"] == largeBod.amountToMake:
            continue
        if smallBodItem["name"] in db:
            index = 0
            found = False
            for smallBod in db[smallBodItem["name"]]:
                #if entry["smallBod"].isExceptional == largeBod.isExceptional and entry["smallBod"].amountMade == largeBod.amountToMake and entry["smallBod"].specialMaterialPropId == largeBod.specialMaterialPropId:
                if smallBod.isExceptional == largeBod.isExceptional and smallBod.amountMade == largeBod.amountToMake and smallBod.specialMaterialPropId == largeBod.specialMaterialPropId:
                    entries.append(smallBod)
                    found = True
                    break
                index = index + 1
            if found:
                del db[smallBodItem["name"]][index]
    return entries

# Internal: Helper that summarizes final state of bods
def report_final_metrics(reports, recipes, incompleteBodContainers, completeSmallBodContainers, completeLargeBodContainer):
    for incompleteBodContainer in incompleteBodContainers:
        bods = Items.FindAllByID(BOD_STATIC_ID, -1, incompleteBodContainer, 1)
        for bod in bods:
            smallBod = parse_small_bod(bod, recipes)
            if smallBod is not None:
                if smallBod.isComplete():
                    reports[bod.Color].incrementNumCompleteSmallBods()
                    reports[bod.Color].incrementNumInWrongContainer()
                    print("Warning: This small bod should not be in the incomplete container! {}".format(smallBod))
                else:
                    reports[bod.Color].incrementNumIncompleteSmallBods()
                continue
            
            largeBod = parse_large_bod(bod)
            if largeBod is not None:
                if largeBod.isComplete():
                    reports[bod.Color].incrementNumCompleteLargeBods()
                    reports[bod.Color].incrementNumInWrongContainer()
                    print("Warning: This large bod should not be in the incomplete container! {}".format(largeBod))
                else:
                    reports[bod.Color].incrementNumIncompleteLargeBods()
                continue

            reports[bod.Color].incrementNumMissingRecipe()
                    
    for completeSmallBodContainer in completeSmallBodContainers:
        bods = Items.FindAllByID(BOD_STATIC_ID, -1, completeSmallBodContainer, 1)
        for bod in bods:
            smallBod = parse_small_bod(bod, recipes)
            if smallBod is not None:
                if smallBod.isComplete():
                    reports[bod.Color].incrementNumCompleteSmallBods()
                else:
                    reports[bod.Color].incrementNumIncompleteSmallBods()
                    reports[bod.Color].incrementNumInWrongContainer()
                    print("Warning: This small bod should not be in the complete small bod container! {}".format(smallBod))
                continue
            
            largeBod = parse_large_bod(bod)
            if largeBod is not None:
                if largeBod.isComplete():
                    reports[bod.Color].incrementNumCompleteLargeBods()
                    reports[bod.Color].incrementNumInWrongContainer()
                    print("Warning: This large bod should not be in the complete small bod container! {}".format(largeBod))
                else:
                    reports[bod.Color].incrementNumIncompleteLargeBods()                    
                    reports[bod.Color].incrementNumInWrongContainer()
                    print("Warning: This large bod should not be in the complete small bod container! {}".format(largeBod))
                continue

            reports[bod.Color].incrementNumMissingRecipe()
                    
    bods = Items.FindAllByID(BOD_STATIC_ID, -1, completeLargeBodContainer, 1)
    for bod in bods:
        smallBod = parse_small_bod(bod, recipes)
        if smallBod is not None:
            if smallBod.isComplete():
                reports[bod.Color].incrementNumCompleteSmallBods()
                reports[bod.Color].incrementNumInWrongContainer()
                print("Warning: This small bod should not be in the complete large bod container! {}".format(smallBod))
            else:
                reports[bod.Color].incrementNumIncompleteSmallBods()
                reports[bod.Color].incrementNumInWrongContainer()
                print("Warning: This small bod should not be in the complete large bod container! {}".format(smallBod))
            continue
        
        largeBod = parse_large_bod(bod)
        if largeBod is not None:
            if largeBod.isComplete():
                reports[bod.Color].incrementNumCompleteLargeBods()
            else:
                reports[bod.Color].incrementNumIncompleteLargeBods()                    
                reports[bod.Color].incrementNumInWrongContainer()                    
                print("Warning: This large bod should not be in the complete large bod container! {}".format(largeBod))
            continue
                            
        reports[bod.Color].incrementNumMissingRecipe()                
        
    print("\n**************** Final Report ***************")        
    for k in reports:
        print(reports[k])
        
# Internal: Need this to stort when filling large bods so we complete those with the most progress first
def sort_large_bods(incompleteBodContainers):
    largeBods = []
    for incompleteBodContainer in incompleteBodContainers:
        bods = Items.FindAllByID(BOD_STATIC_ID, -1, incompleteBodContainer, 1)
        for bod in bods:
            largeBod = parse_large_bod(bod)
            if largeBod is not None: 
                largeBods.append(largeBod)
    
    largeBods = sorted(largeBods, key = lambda largeBod: (largeBod.getId(), -ord(str(largeBod.numComplete()))))
    for largeBod in largeBods:
        print(largeBod.getId(), " (", largeBod.numComplete(), ")")
    return largeBods
                
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
def run_bod_builder(
    
    # Array of serials for containers to put your bods in to start things off (both small and large).
    # You put your bods in here.
    incompleteBodContainers,
    
    # Array of serials of containers to put completed small bods.
    # The script will store completed small bods in these.
    completeSmallBodContainers,
    
    # Serial of container for completed LBODs. This is where you can pick them
    # up and then go turn them in. 
    completeLargeBodContainer,
    
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
    
    # Time to wait between item moves. Adjust with caution. Reducing this will increase speed
    # of the script, but you risk disconnects and other issues maintaining state
    itemMoveDelayMs = 1000,
    
    # (Optional) God save the queen
    gumpDelayMs = 250
):
    # Open containers because we may not have that item data yet.
    for incompleteBodContainer in incompleteBodContainers:
        Items.UseItem(incompleteBodContainer)
        Misc.Pause(itemMoveDelayMs)
    for completeSmallBodContainer in completeSmallBodContainers:
        Items.UseItem(completeSmallBodContainer)
        Misc.Pause(itemMoveDelayMs)
    Items.UseItem(toolContainer)
    Misc.Pause(itemMoveDelayMs)
    Items.UseItem(resourceContainer)
    Misc.Pause(itemMoveDelayMs)    
    
    CRAFTING_GUMP_ID = 0x38920abd
    SMALL_BOD_GUMP_ID = 0x5afbd742
    LARGE_BOD_GUMP_ID = 0xa125b54a
    
    # Turn this array into a dictionary keyed on item name. Its just easier that way.
    # So instead of [SmallBodRecipe, SmallBodRecipe...] we get:
    # { "cutlass": SmallBodRecipe, "platemail helm": SmallBodRecipe...
    x = {}
    for recipe in recipes:
        x[recipe.itemName] = recipe
    recipes = x
    
    # Just for tracking, can remove this crap.
    reports = {
        HUE_BLACKSMITHY:    BodReport("Blacksmithy"),
        HUE_TAILORING:      BodReport("Tailoring  "),
        HUE_CARPENTRY:      BodReport("Carpentry  "),
        HUE_ALCHEMY:        BodReport("Alchemy    "),
        HUE_INSCRIPTION:    BodReport("Inscription"),
        HUE_TINKERING:      BodReport("Tinkering  ")
    }    
        
    print("****** Start Small BOD ******")
    for incompleteBodContainer in incompleteBodContainers:
        bods = Items.FindAllByID(BOD_STATIC_ID, -1, incompleteBodContainer, 1)
        for bod in bods:
            while True:
                # Get fresh version of bod
                freshBod = Items.FindBySerial(bod.Serial)
                smallBod = parse_small_bod(freshBod, recipes, True)
                
                if smallBod is not None:
                    if smallBod.specialMaterialHue not in allowedResourceHues:
                        print("Warning: Skipping because material is not in allowed list: {}".format(smallBod.craftedItemName))
                        break
                        
                    if freshBod.Container != Player.Backpack.Serial:
                        Items.Move(freshBod, Player.Backpack.Serial, freshBod.Amount)
                        Misc.Pause(itemMoveDelayMs)                
                        
                    if smallBod.isComplete():
                        print("Filled small BOD!")
                        print
                        for completeSmallBodContainer in completeSmallBodContainers:
                            container = Items.FindBySerial(completeSmallBodContainer)
                            if container.Contains.Count < 125:
                                Items.Move(freshBod, completeSmallBodContainer, freshBod.Amount)
                                Misc.Pause(itemMoveDelayMs)                
                                break
                        break
                    else:
                        print("Bod progress: {} {}/{}".format(smallBod.craftedItemName, smallBod.amountMade, smallBod.amountToMake))
                        
                        tool = get_tool(smallBod, toolContainer)
                        
                        if tool is None:
                            print("Error: Cannot find tool")
                            sys.exit()
                            
                        if not check_resources(smallBod, resourceContainer):
                            print("Warning: Out of resources, skipping {}".format(smallBod.craftedItemName))
                            Items.Move(freshBod, incompleteBodContainer, freshBod.Amount)
                            Misc.Pause(itemMoveDelayMs)
                            reports[freshBod.Color].incrementNumMissingResources()
                            break

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
                        recycle(salvageBag, smallBod)         

                else:
                    break
                    
                Misc.Pause(1000)
                recycle(salvageBag, smallBod)         

    db = build_complete_small_bod_db(completeSmallBodContainers, recipes)
    
    print("****** Start Large BOD ******")
    largeBods = sort_large_bods(incompleteBodContainers)
    for largeBod in largeBods:
        if largeBod is not None: 
           
            bod = Items.FindBySerial(largeBod.itemSerial)
            if largeBod.isComplete() and bod.Container in incompleteBodContainers:
                print("Found a misplaced (but complete) large bod, moving to right container! :))")
                Items.Move(largeBod.itemSerial, completeLargeBodContainer, 1)
                Misc.Pause(itemMoveDelayMs)
                continue
            
            smallBods = search_complete_small_bod_db(db, largeBod)
            
            if len(smallBods) > 0:
                print("Found matches for a small bod, attempting to complete...")
                for smallBodItem in largeBod.smallBodItems:
                    print("\tsmallBodItem: {} - ({})".format(smallBodItem["name"], smallBodItem["amountMade"]))
                    
                Items.Move(largeBod.itemSerial, Player.Backpack.Serial, 1)
                Misc.Pause(itemMoveDelayMs)
                for smallBod in smallBods:
                    #Items.Move(entry["Serial"], Player.Backpack.Serial, 1)
                    print("\tso moving {}".format(smallBod))
                    Items.Move(smallBod.itemSerial, Player.Backpack.Serial, 1)
                    Misc.Pause(itemMoveDelayMs)
                   
                # Open Large bod gump
                Target.Cancel()
                Items.UseItem(largeBod.itemSerial)
                Gumps.WaitForGump(LARGE_BOD_GUMP_ID, 3000)
                Target.Cancel()
                Misc.Pause(1000)
                
                # Combine with contained items (backpack)
                Gumps.SendAction(LARGE_BOD_GUMP_ID, 4) 
                Target.WaitForTarget(5000)
                Target.TargetExecute(Player.Backpack.Serial)
                Gumps.WaitForGump(LARGE_BOD_GUMP_ID, 3000)
                Misc.Pause(1500)
                Target.Cancel()
                Gumps.CloseGump(LARGE_BOD_GUMP_ID)
                
                bod = Items.FindBySerial(largeBod.itemSerial)
                freshLargeBod = parse_large_bod(bod)
                
                if freshLargeBod.isComplete():
                    print("\t...large BOD filled! :)")
                    Items.Move(largeBod.itemSerial, completeLargeBodContainer, 1)
                    Misc.Pause(itemMoveDelayMs)
                else:
                    print("\t...large BOD back to incompleteBodContainer :(")
                    Items.Move(largeBod.itemSerial, incompleteBodContainer, 1)
                    Misc.Pause(itemMoveDelayMs)
                   
    report_final_metrics(reports, recipes, incompleteBodContainers, completeSmallBodContainers, completeLargeBodContainer)
