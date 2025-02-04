# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-03-26
# Use at your own risk. 


from System.Collections.Generic import List
import sys
from System import Byte, Int32
from Scripts.fm_core.core_player import find_first_in_container_by_ids
from Scripts.fm_core.core_player import find_first_in_hands_by_id
from Scripts.fm_core.core_player import move_all_items_from_container
from Scripts.fm_core.core_player import move_item_to_container_by_id
from Scripts.fm_core.core_player import find_in_container_by_id
from Scripts.fm_core.core_player import find_first_in_container_by_name
from Scripts.fm_core.core_player import find_all_in_container_by_id
from Scripts.fm_core.core_mobiles import get_friends_by_names
from Scripts.fm_core.core_rails import move
from Scripts.fm_core.core_rails import go_to_tile
from Scripts.fm_core.core_rails import get_tile_in_front
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

def craft_potion_and_fill_keg():
    Player.HeadMessage(48, "Crafting potion and filling keg")
    print("Select a keg")
    tool = find_first_in_container_by_ids(ALCHEMY_TOOL_STATIC_IDS, Player.Backpack.Serial)
    if tool is not None:
        Items.UseItem(tool)
        print(tool)
    else:
        Player.HeadMessage(38, "No tools found, quitting")
    return False
craft_potion_and_fill_keg()




#from Scripts.fm_core.core_mobiles import get_enemies
#from Scripts.fm_core.core_mobiles import get_pets
#from Scripts.fm_core.core_player import move_all_items_from_container
#from Scripts.fm_core.core_items import AXE_STATIC_IDS, LOG_STATIC_IDS, TREE_STATIC_IDS
#from Scripts.fm_core.core_player import find_in_container_by_id
#from Scripts.fm_core.core_player import move_item_to_container
#from Scripts.fm_core.core_spells import get_fc_delay
#from Scripts.fm_core.core_spells import SUMMON_FAMILIAR_DELAY
#from Scripts.fm_core.core_spells import FC_CAP_NECROMANCY
#from Scripts.fm_core.core_rails import go_to_tile
#from Scripts.fm_core.core_items import get_corpses
#from Scripts.fm_core.core_rails import get_tile_in_front

from System.Collections.Generic import List
from System import Byte, Int32
#from Scripts.fm_core.core_items import BOD_STATIC_ID
#from Scripts.fm_core.core_items import BOD_BOOK_STATIC_ID

#from System.Collections.Generic import List
import sys
#from System import Byte, Int32
#import time
import re
#import os

#https://github.com/matsamilla/Razor-Enhanced/blob/master/NoxBodFiles/Smithbodgod.py

# This stuff is used to detect keypresses like mouse for movement
#import ctypes
#from ctypes import wintypes
#user32 = ctypes.WinDLL('user32', use_last_error=True)
#user32.GetAsyncKeyState.restype = wintypes.SHORT
#user32.GetAsyncKeyState.argtypes = [wintypes.INT]

from Scripts.fm_core.core_player import find_first_in_container_by_ids

from Scripts.fm_core.core_items import BOD_STATIC_ID
from Scripts.fm_core.core_items import BOD_BOOK_STATIC_ID

#from Scripts.fm_core.core_items import INGOT_STATIC_IDS

#from Scripts.fm_core.core_items import BLACKSMITHY_TOOL_STATIC_IDS
#from Scripts.fm_core.core_items import TINKERING_TOOL_STATIC_IDS
#from Scripts.fm_core.core_items import ALCHEMY_TOOL_STATIC_IDS
#from Scripts.fm_core.core_items import TAILORING_TOOL_STATIC_IDS
#from Scripts.fm_core.core_items import CARPENTRY_TOOL_STATIC_IDS
#from Scripts.fm_core.core_items import INSCRIPTION_TOOL_STATIC_IDS

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


MACE_STATIC_ID = 0x0F5C
METAL_SHIELD_STATIC_ID = 0x1B7B

ALL_CRAFTED_ITEM_IDS = [MACE_STATIC_ID, METAL_SHIELD_STATIC_ID]
ALL_RESOURCES = [INGOT_STATIC_ID, BOARD_STATIC_ID, CLOTH_STATIC_ID, LEATHER_STATIC_ID, MANDRAKEROOT, BLOODMOSS, SULPHUROUSASH, NIGHTSHADE, BLACKPEARL, SPIDERSILK, GINSENG, GARLIC, PIGIRON, BATWING, NOXCRYSTAL, DAEMONBLOOD, GRAVEDUST ]

Player.HeadMessage(455, "start")

PROP_ID_AMOUNT_TO_MAKE = 1060656
PROP_ID_EXCEPTIONAL = 1045141
PROP_ID_SHADOW_IRON = 1045143
PROP_ID_ITEM_TEXT = 1060658

# 1023932
# mace_id = 0x0F5C
#mace_id = 1023932
#feathered_hat_id = 1025914


#DEFAULT_BLACKSMITHY_MATERIAL = 6

# Default
RESOURCE_HUE_DEFAULT = 0x0000

# Ingots
#RESOURCE_HUE_IRON = 0x0000
RESOURCE_HUE_DULL_COPPER = 0x0415
RESOURCE_HUE_SHADOW_IRON = 0x0455
RESOURCE_HUE_COPPER = 0x045f
RESOURCE_HUE_BRONZE = 0x06d8
RESOURCE_HUE_GOLD = 0x06b7
RESOURCE_HUE_AGAPITE = 0x097e
RESOURCE_HUE_VERITE = 0x07d2
RESOURCE_HUE_VALORITE = 0x0544

# Leather
RESOURCE_HUE_BARBED = 0x059d
RESOURCE_HUE_SPINED = 0x05e4
RESOURCE_HUE_HORNED = 0x0900

# Wood
RESOURCE_HUE_OAK = 0x07da
RESOURCE_HUE_ASH = 0x04a7
RESOURCE_HUE_YEW = 0x04a8
RESOURCE_HUE_HEARTWOOD = 0x04a9
RESOURCE_HUE_BLOODWOOD = 0x04aa
RESOURCE_HUE_FROSTWOOD = 0x047f


# This goes prop.Number -> { gump button id, special resource hue }
# ServUO\Scripts\Services\BulkOrders\SmallBODs\SmallBODGump.cs
# Tried doing a regex by special material name, e.g. All items must be made
# with Dull Copper Ingots, but it didnt follow that convetion for carpenty.
# It just said "Oak". So, I got mad and just did an exact match for the 
# Propert.Number. Whatever.
SPECIAL_PROP_MATERIAL_MAP = {
    #1045142: { "button": 13, "hue": RESOURCE_HUE_DULL_COPPER }, # Dull Copper
    #1045143: { "button": 20, "hue": RESOURCE_HUE_SHADOW_IRON }, # Shadow Iron
    
    1045142: { "button": 13, "hue": RESOURCE_HUE_DULL_COPPER },    # Dull Copper
    1045143: { "button": 20, "hue": RESOURCE_HUE_SHADOW_IRON },    # Shadow Iron
    1045144: { "button": 27, "hue": RESOURCE_HUE_DULL_COPPER },    # Copper
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
    
#    "dull copper ingots": { "button": 13, "hue": RESOURCE_HUE_DULL_COPPER }, 
#    "copper ingots": { "button": 27, "hue": RESOURCE_HUE_DULL_COPPER }, 
#    "shadow iron ingots": { "button": 20, "hue": RESOURCE_HUE_SHADOW_IRON }, 
#    "bronze ingots": { "button": 34, "hue": RESOURCE_HUE_BRONZE }, 
#    "gold ingots": { "button": 41, "hue": RESOURCE_HUE_GOLD }, 
#    "agapite ingots": { "button": 48, "hue": RESOURCE_HUE_AGAPITE },
#    "verite ingots": { "button": 55, "hue": RESOURCE_HUE_VERITE }, 
#    "valorite ingots": { "button": 62, "hue": RESOURCE_HUE_VALORITE },
#
#    "spined leather": { "button": 13, "hue": RESOURCE_HUE_SPINED }, 
#    "horned leather": { "button": 20, "hue": RESOURCE_HUE_HORNED }, 
#    "barbed leather": { "button": 27, "hue": RESOURCE_HUE_BARBED }, 
#    
#    "oak": { "button": 13, "hue": RESOURCE_HUE_DEFAULT }, 
#    "ash": { "button": 20, "hue": RESOURCE_HUE_DEFAULT }, 
#    "yes": { "button": 27, "hue": RESOURCE_HUE_DEFAULT }, 
#    "heartwood": { "button": 34, "hue": RESOURCE_HUE_DEFAULT }, 
#    "bloodwood": { "button": 41, "hue": RESOURCE_HUE_DEFAULT }, 
#    "frostwood": { "button": 48, "hue": RESOURCE_HUE_DEFAULT }, 
}

HUE_BLACKSMITHY = 0x044e
HUE_TAILORING = 0x0483
HUE_CARPENTRY = 0x05e8
HUE_ALCHEMY = 0x09c9
HUE_INSCRIPTION = 0x0a26
HUE_TINKERING = 0x0455

DEFAULT_MATERIAL_BY_HUE_MAP = {
    HUE_BLACKSMITHY: { "button": 6, "hue": RESOURCE_HUE_DEFAULT },    # Iron Ingots
    HUE_TAILORING: { "button": 6, "hue": RESOURCE_HUE_DEFAULT },       # Leather
    HUE_CARPENTRY: { "button": 6, "hue": RESOURCE_HUE_DEFAULT },       # Wood
    HUE_TINKERING: { "button": 6, "hue": RESOURCE_HUE_DEFAULT },       # Iron Ingots
    HUE_ALCHEMY: { "button": 0, "hue": RESOURCE_HUE_DEFAULT },          # None
    HUE_INSCRIPTION: { "button": 0, "hue": RESOURCE_HUE_DEFAULT }      # None
}

CAT_BLACKSMITHY_METAL_ARMOR = 1
CAT_BLACKSMITHY_HELMETS = 8
CAT_BLACKSMITHY_SHIELDS = 15
CAT_BLACKSMITHY_BLADED = 22
CAT_BLACKSMITHY_AXES = 29
CAT_BLACKSMITHY_POLEARMS = 36
CAT_BLACKSMITHY_BASHING = 43
CAT_BLACKSMITHY_CANNONS = 50
CAT_BLACKSMITHY_THROWING = 57

CRAFTING_GUMP_ID = 0x38920abd
SMALL_BOD_GUMP_ID =  0x5afbd742
# carp = 0x38920abd
 #0x38920abd


#HUE_TOOL_MAP = {
#    HUE_BLACKSMITHY: BLACKSMITHY_TOOL_STATIC_IDS,
#    HUE_TAILORING: TAILORING_TOOL_STATIC_IDS,
#    HUE_CARPENTRY: CARPENTRY_TOOL_STATIC_IDS,
#    HUE_ALCHEMY: ALCHEMY_TOOL_STATIC_IDS,
#    HUE_INSCRIPTION: INSCRIPTION_TOOL_STATIC_IDS,
#    HUE_TINKERING: TINKERING_TOOL_STATIC_IDS
#}

class SmallBodResource:
    def __init__(self, resourceId, amount = 100, canOverrideHue = True, hue = RESOURCE_HUE_DEFAULT):
        self.resourceId = resourceId
        self.amount = amount
        self.canOverrideHue = canOverrideHue
        self.hue = hue
        
    def __str__(self):
        return f"SmallBodResource(resourceId='{self.resourceId}', amount={self.amount}, canOverrideHue='{self.canOverrideHue}', hue='{self.hue}')"        

class SmallBodTemplate:
    def __init__(self, bodHue, craftedItemId, gumpCategory, gumpSelection, toolId, resources):
        self.bodHue = bodHue
        self.craftedItemId = craftedItemId
        self.gumpCategory = gumpCategory
        self.gumpSelection = gumpSelection
        self.toolId = toolId
        self.resources = resources
        
    def __str__(self):
        return f"SmallBodTemplate(bodHue='{self.bodHue}', craftedItemId={self.craftedItemId}, gumpCategory='{self.gumpCategory}', gumpSelection='{self.gumpSelection}', toolId='{self.toolId}', resources='{self.resources}')"        
        
class SmallBod:
    def __init__(self, itemName, amountMade, isExceptional, amountToMake, specialMaterialButton, specialMaterialHue, template):
        self.itemName = itemName
        self.amountMade = amountMade
        self.isExceptional = isExceptional
        self.amountToMake = amountToMake
        self.specialMaterialButton = specialMaterialButton
        self.specialMaterialHue = specialMaterialHue
        self.template = template
    def __str__(self):
        return f"SmallBod(itemName='{self.itemName}', amountMade='{self.amountMade}', isExceptional={self.isExceptional}, amountToMake='{self.amountToMake}', specialMaterialButton='{self.specialMaterialButton}', specialMaterialHue='{self.specialMaterialHue}', template={self.template})"        



# The final buttons in the crafting gumps, based on the value of a property
# called PROP_ID_ITEM_NAME. A metal shield for example has a property like:
# Propery.Number = 1060658, and the value is a string = #1027035  0
# We are dealing with that second part (stripping the hashbrown)
#PROP_TEXT_INFO_MAP = {
#    "1023932": SmallBodStaticInfo(HUE_BLACKSMITHY, MACE_STATIC_ID, CAT_BLACKSMITHY_BASHING, 9, BLACKSMITHY_TOOL_STATIC_IDS, INGOT_STATIC_IDS), # Mace
#}

TEMPLATES = {
    "mace": SmallBodTemplate(HUE_BLACKSMITHY, MACE_STATIC_ID, CAT_BLACKSMITHY_BASHING, 9, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID, 6)] ),
    "metal shield": SmallBodTemplate(HUE_BLACKSMITHY, METAL_SHIELD_STATIC_ID, CAT_BLACKSMITHY_SHIELDS, 23, BLACKSMITHY_TOOL_STATIC_ID, [SmallBodResource(INGOT_STATIC_ID, 14)] ),
}

def recycle(salvageBag):
    items = Items.FindAllByID(ALL_CRAFTED_ITEM_IDS, -1, Player.Backpack.Serial, -1)
    for item in items:
        Items.Move(item, salvageBag, item.Amount)
        Misc.Pause(800)
    Misc.WaitForContext(salvageBag, 10000)
    Misc.ContextReply(salvageBag, 2)   
    Misc.Pause(1000)
    return None

def get_small_bod(bod):
    isExceptional = False
    amountToMake = 0
    specialMaterial = DEFAULT_MATERIAL_BY_HUE_MAP[bod.Color]
    itemText = None
    amountMade = 0
    template = None
    for prop in bod.Properties:
        if prop.Number == PROP_ID_EXCEPTIONAL:
            isExceptional = True
        if prop.Number == PROP_ID_AMOUNT_TO_MAKE:
            amountToMake = int(prop.Args)
            
        #match = re.match(r"All Items Must Be Made With (.*){1}\.", prop.ToString(), re.IGNORECASE)
        #if match:
        #    print("MATCH FOUND!", match.group(0))
        #    print("MATCH FOUND!", match.group(1))
            
        if prop.Number in SPECIAL_PROP_MATERIAL_MAP:
            specialMaterial = SPECIAL_PROP_MATERIAL_MAP[prop.Number]
            
        if prop.Number == PROP_ID_ITEM_TEXT:
            print("PROP STRING:", prop.ToString())
            #propList = prop.Args.ToString().replace('#', '').split('\t')
            propList = prop.ToString().split(": ")
            itemName = propList[0]
            #itemText = propList[0]
            amountMade = int(propList[1])
            if itemName in TEMPLATES:
                template = TEMPLATES[itemName]
            
    if template is not None:
        return SmallBod(itemName, amountMade, isExceptional, amountToMake, specialMaterial["button"], specialMaterial["hue"], template)
    else:
        #print("Warning: Could not find static info for: itemText", itemText, "amountMade", amountMade, "isExceptional", isExceptional, "amountToMake", amountToMake, "material", material)
        print("Warning: Could not find static info for:")
        for prop in bod.Properties:
            #print("\t", prop.ToString(), prop.Args.ToString(), prop.Number)
            print("\t", prop.ToString(), "(", prop.Number, ")")
            #print("\t", prop.ToString())
        
def get_tool(smallBod, toolContainer):
    #print(HUE_TOOL_MAP[smallBodInfo.staticInfo.bodHue])
    #tool = find_first_in_container_by_ids(HUE_TOOL_MAP[smallBodInfo.staticInfo.bodHue], Player.Backpack.Serial)
    #tool = find_first_in_container_by_ids(smallBod.template.toolIds, Player.Backpack.Serial)
    tool = Items.FindByID(smallBod.template.toolId, -1, Player.Backpack.Serial, -1)
    if tool is not None:
        return tool
        
    tool = Items.FindByID(smallBod.template.toolId, -1, toolContainer, -1)
    #tool = find_first_in_container_by_ids(smallBodInfo.staticInfo.toolIds, toolContainer)
    if tool is not None:
        Items.Move(tool, Player.Backpack.Serial, tool.Amount)
        Misc.Pause(1000)
        return tool

    
def check_resources(smallBod, resourceContainer):
    for resource in smallBod.template.resources:
        while True:
            hue = smallBod.specialMaterialHue if resource.canOverrideHue else resource.hue 
            items = Items.FindAllByID(resource.resourceId, hue, Player.Backpack.Serial, -1)
            
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
                #return check_resources(smallBod, resourceContainer)
                
    # Cleanup nonessentials, move to resource crate
    for resourceId in ALL_RESOURCES:
        keep = False
        for resource in smallBod.template.resources:
            if resourceId == resource.resourceId:
                keep = True
                break
        if not keep:
            items = Items.FindAllByID(resourceId, -1, Player.Backpack.Serial, -1)
            for item in items:
                Items.Move(item, resourceContainer, item.Amount)
            
    return True


gumpDelayMs = 250
incompleteSmallBodContainer = 0x4025193E
completeSmallBodContainer = 0x402519AE
toolContainer = 0x40251A02
resourceContainer = 0x408CC21E
salvageBag = 0x400E972D
allowedResourceHues = [RESOURCE_HUE_DEFAULT]  

Items.UseItem(completeSmallBodContainer)
Misc.Pause(1000)
Items.UseItem(incompleteSmallBodContainer)
Misc.Pause(1000)
Items.UseItem(toolContainer)
Misc.Pause(1000)
Items.UseItem(resourceContainer)
Misc.Pause(1000)

bods = Items.FindAllByID(BOD_STATIC_ID, -1, Player.Backpack.Serial, 1)
for bod in bods:
    Items.Move(bod, incompleteSmallBodContainer, bod.Amount)
    Misc.Pause(1000)  
    
print("-------=======---******---*_*_*_*_---------====-----")
bods = Items.FindAllByID(BOD_STATIC_ID, -1, incompleteSmallBodContainer, 1)
for bod in bods:
    configureGump = True
    oldTool = None
    while True:
        # Get fresh version of bod
        freshBod = Items.FindBySerial(bod.Serial)
        smallBod = get_small_bod(freshBod)
        
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
                    
                if tool != oldTool:
                    oldTool = tool
                    configureGump = True                    
                    
                configureGump = True
                
                if configureGump:
                    # Opens crafting gump
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
                            
                        Gumps.SendAction(CRAFTING_GUMP_ID, smallBod.specialMaterialButton)
                        Gumps.WaitForGump(CRAFTING_GUMP_ID, 5000)
                        Misc.Pause(gumpDelayMs)
                        if not Gumps.HasGump(CRAFTING_GUMP_ID):
                            continue     
             
                    # Sets category
                    Gumps.SendAction(CRAFTING_GUMP_ID, smallBod.template.gumpCategory)
                    Gumps.WaitForGump(CRAFTING_GUMP_ID, 5000)
                    Misc.Pause(gumpDelayMs)
                    if not Gumps.HasGump(CRAFTING_GUMP_ID):
                        continue
                        
                    configureGump = False                        
                    
                # Actually does crafting
                Gumps.SendAction(CRAFTING_GUMP_ID, smallBod.template.gumpSelection)                    
                Gumps.WaitForGump(CRAFTING_GUMP_ID, 5000)
                Misc.Pause(3000)
                if not Gumps.HasGump(CRAFTING_GUMP_ID):
                    continue                    
                
                # Add item to small bod
                #craftedItems = Items.FindAllByID(smallBod.template.craftedItemId, smallBod.specialMaterialHue, Player.Backpack.Serial, -1)
                #for craftedItem in craftedItems:
                #    isAllowed = False
                #    if smallBod.isExceptional:
                #        for prop in craftedItem.Properties:
                #            if prop.ToString() == "exceptional":
                #                isAllowed = True
                #                break
                #    else:
                #        isAllowed = True

                 #   if isAllowed:
                Items.UseItem(freshBod)
                Gumps.WaitForGump(SMALL_BOD_GUMP_ID, 5000)
                Misc.Pause(gumpDelayMs)
                
                Target.Cancel()
                Gumps.SendAction(SMALL_BOD_GUMP_ID, 4) # Combine with contained items
                Target.WaitForTarget(5000)
                Target.TargetExecute(Player.Backpack.Serial)
                Gumps.WaitForGump(SMALL_BOD_GUMP_ID, 1000)
                Misc.Pause(1000)
                Target.Cancel()
                Gumps.CloseGump(SMALL_BOD_GUMP_ID)
                    
            
            
            recycle(salvageBag)         

        else:
            break
        
            

            


