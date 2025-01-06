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
from Scripts.fm_core.core_player import move_item_to_container
from Scripts.fm_core.core_player import find_in_container_by_id
from Scripts.fm_core.core_player import find_first_in_container_by_name
from Scripts.fm_core.core_player import find_all_in_container_by_id
from Scripts.fm_core.core_player import find_all_in_container_by_ids
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
from Scripts.fm_core.core_items import SAND_STATIC_IDS
from Scripts.fm_core.core_items import FISH_STATIC_IDS

# Lumberjacking original author: https://github.com/hampgoodwin/razorenhancedscripts/blob/master/LumberjackingScanTile.py
# Mining original author: https://github.com/getoldgaming/razor-enhanced-/blob/master/autoMiner.py
# Note I did modify these and make them much worse. Use the one linked above.

# Pastrami
CHOP_DELAY = 2000
PAUSE_DELAY_MS = 650

# Variabili Sistema
tileinfo = List[Statics.TileInfo]
treeposx = []
treeposy = []
treeposz = []
treegfx = []
treenumber = 0
blockcount = 0

def RangeTree( spotnumber ):
    global tileinfo, treenumber, treeposx, treeposy, treeposz, treegfx, blockcount, TREE_STATIC_IDS, AXE_STATIC_IDS, CHOP_DELAY
    if (Player.Position.X - 1) == treeposx[spotnumber] and (Player.Position.Y + 1) == treeposy[spotnumber]:
        return True
    elif (Player.Position.X - 1) == treeposx[spotnumber] and (Player.Position.Y - 1) == treeposy[spotnumber]:
        return True
    elif (Player.Position.X + 1) == treeposx[spotnumber] and (Player.Position.Y + 1) == treeposy[spotnumber]:
        return True
    elif (Player.Position.X + 1) == treeposx[spotnumber] and (Player.Position.Y - 1) == treeposy[spotnumber]:
        return True
    elif Player.Position.X == treeposx[spotnumber] and (Player.Position.Y - 1) == treeposy[spotnumber]:
        return True    
    elif Player.Position.X == treeposx[spotnumber] and (Player.Position.Y + 1) == treeposy[spotnumber]:   
        return True     
    elif Player.Position.Y == treeposy[spotnumber] and (Player.Position.X - 1) == treeposx[spotnumber]:
        return True    
    elif Player.Position.Y == treeposy[spotnumber] and (Player.Position.X + 1) == treeposx[spotnumber]:   
        return True    
    else:
        return False
    
def ScanStatic(tileRange): 
    global tileinfo, treenumber, treeposx, treeposy, treeposz, treegfx, blockcount, TREE_STATIC_IDS, AXE_STATIC_IDS, CHOP_DELAY
    
    treeposx.Clear()
    treeposy.Clear()
    treeposz.Clear()
    treegfx.Clear()
    
    Misc.SendMessage("--> Inizio Scansione Tile", 77)
    minx = Player.Position.X - tileRange
    maxx = Player.Position.X + tileRange
    miny = Player.Position.Y - tileRange
    maxy = Player.Position.Y + tileRange

    while miny <= maxy:
        while minx <= maxx:
            tileinfo = Statics.GetStaticsTileInfo(minx, miny, Player.Map)
            if tileinfo.Count > 0:
                for tile in tileinfo:
                    for staticid in TREE_STATIC_IDS:
                        if staticid == tile.StaticID:
                            Misc.SendMessage('--> Albero X: %i - Y: %i - Z: %i - GFX: %i' % (minx, miny, tile.StaticZ, tile.StaticID), 66)
                            treeposx.Add(minx)
                            treeposy.Add(miny)
                            treeposz.Add(tile.StaticZ)
                            treegfx.Add(tile.StaticID)
            else:
                Misc.NoOperation()
            minx = minx + 1
        minx = Player.Position.X - tileRange            
        miny = miny + 1
    treenumber = treeposx.Count    
    Misc.SendMessage('--> Totale Alberi: %i' % (treenumber), 77)
    
def CutTree( spotnumber, axe, weightLimit ):
    global tileinfo, treenumber, treeposx, treeposy, treeposz, treegfx, blockcount, TREE_STATIC_IDS, AXE_STATIC_IDS, CHOP_DELAY
    Target.Cancel()
    Misc.Pause(1000)
    
    if Target.HasTarget():
        Misc.SendMessage("--> Blocco rilevato target residuo, cancello!", 77)
        Target.Cancel()
        Misc.Pause(500)
    else:
        Misc.NoOperation()    
    if (Player.Weight >= weightLimit):
        Misc.Pause(1500)
        Misc.SendMessage("You are too heavy!", 38)
        sys.exit()
    else:
        Misc.NoOperation()
    Journal.Clear()
    Items.UseItem(axe)
    Target.WaitForTarget(4000)
    print(spotnumber, treeposx[spotnumber], treeposy[spotnumber], treeposz[spotnumber], treegfx[spotnumber])
    Target.TargetExecute(treeposx[spotnumber], treeposy[spotnumber], treeposz[spotnumber], treegfx[spotnumber])
    
    Misc.Pause(CHOP_DELAY)
    
#    cut_drop_and_move_boards(axe, cutLogsToBoards = False, dropOnGround = False, packAnimalNames = []):
    
    
    #if Journal.Search("not enough wood"):
    if Journal.Search("There's not enough wood here to harvest."):
        # '
        Misc.SendMessage("--> Cambio albero", 77)
    elif Journal.Search("That is too far away"):
        blockcount = blockcount + 1
        Journal.Clear()
        if (blockcount > 15):
            blockcount = 0
            Misc.SendMessage("--> Possibile blocco rilevato cambio albero", 77)
        else:
            CutTree(spotnumber, axe, weightLimit)
    else:
        Misc.SendMessage("Recursive Call on this tree")
        CutTree(spotnumber, axe, weightLimit)
        
# Too heavy. Turn to boards. Praise Be.
def logs_to_boards(container, axe):
    global tileinfo, treenumber, treeposx, treeposy, treeposz, treegfx, blockcount, TREE_STATIC_IDS, AXE_STATIC_IDS, CHOP_DELAY
    #logs = find_first_item_by_id(LOG_STATIC_IDS, Player.Backpack)
    log = find_in_container_by_id(LOG_STATIC_IDS, Player.Backpack.Serial)
    if log != None:
        Items.UseItem(axe)
        Target.WaitForTarget(4000)
        Target.WaitForTarget(10000, False)
        Target.TargetExecute(log.Serial)
            
# Makes a box around where player is standing and chops trees inside. The
# size of the box is determined by tileRange.
# You will need an axe equipped I believe.
def run_lumberjacking_loop(
    # Makes a square tileRange * tileRange and will search for trees inside of it. So,
    # all you have to do is place yourself near a bunch of trees and hit the hotkey that
    # runs this function.
    tileRange = 10, 
    
    # If this limit is reached, the script just stops apparently.
    weightLimit = 350, 
    
    # Flag that will convert the logs into boards. I think you need an axe.
    cutLogsToBoards = False, 
    
    # After chopping wood, you can drop the wood on teh ground. Useful i you are just gaining skill.
    dropOnGround = False,
    
    # If you have a beetle
    packAnimalNames = []
    ):
        
    global tileinfo, treenumber, treeposx, treeposy, treeposz, treegfx, blockcount, TREE_STATIC_IDS, AXE_STATIC_IDS, CHOP_DELAY

    Misc.SendMessage("--> Avvio Patramie", 77)  
    Misc.SendMessage("Eqipping Axe", 123)
    
#    originalItemsInHands = [None, None]
    axe = find_first_in_hands_by_id(AXE_STATIC_IDS)
    #axe = find_in_container_by_id(AXE_STATIC_IDS, Player.Backpack)
#    if axe == None:
#        axe = find_first_item_by_id(AXE_STATIC_IDS, Player.Backpack)
#        if axe == None:
#            Misc.SendMessage("You dont have an axe foo", 38)
#            sys.exit()
#        originalItemsInHands = swap_weapon(axe)

    ScanStatic(tileRange)
    i = 0
    Misc.SendMessage("Total tree number {}".format(treenumber))
    while i < treenumber:
        Misc.SendMessage("Moving to a tree")
        #go_to_tile(treeposx[i] - 1, treeposy[i] - 1, 88.0)
        cut_drop_and_move_boards(axe, cutLogsToBoards, dropOnGround, packAnimalNames)
        go_to_tile(treeposx[i] - 1, treeposy[i] - 1, 5.0)
        CutTree(i, axe, weightLimit)
        cut_drop_and_move_boards(axe, cutLogsToBoards, dropOnGround, packAnimalNames)
        
#        logs = find_first_in_container_by_ids(LOG_STATIC_IDS, Player.Backpack)
#        if logs != None and dropOnGround:
#            Player.HeadMessage(48, "Dropping Logs on ground")
#            Items.MoveOnGround(logs,0,Player.Position.X - 1, Player.Position.Y + 1, 0)
#        elif logs != None and cutLogsToBoards:
#            Items.UseItem(axe)
#            Target.WaitForTarget(10000, False)
#            Target.TargetExecute(logs.Serial)
#            
#        packAnimals = get_friends_by_names(friendNames = packAnimalNames, range = 2)
#        if len(packAnimals) > 0:
#            for packAnimal in packAnimals:
#                print(packAnimal.Name, packAnimal.Backpack.Weight)
#                if packAnimal.Backpack.Weight < 1350:
#                    for boardStaticID in BOARD_STATIC_IDS:
#                        move_item_to_container_by_id(boardStaticID, Player.Backpack, packAnimal.Backpack.Serial)
                    
        i = i + 1
        Misc.Pause(500)
        
    #treeposx = []
    #treeposy = []
    #treeposz = []
    #treegfx = []
    #treenumber = 0

#    Misc.SendMessage("Re-qeuipping shitter", 123) 
    
#    if originalItemsInHands[0] != None:
#        Misc.Pause(1000)
#        swap_weapon(originalItemsInHands[0])
#        Misc.Pause(4000)
#        
#    if originalItemsInHands[1] != None:
#        Misc.Pause(1000)
#        swap_weapon(originalItemsInHands[1])
#        Misc.Pause(4000)
        
def cut_drop_and_move_boards(axe, cutLogsToBoards = False, dropOnGround = False, packAnimalNames = []):
    global treenumber, treeposx, treeposy, treeposz, treegfx, blockcount, TREE_STATIC_IDS, AXE_STATIC_IDS, CHOP_DELAY
    #logs = find_first_in_container_by_ids(LOG_STATIC_IDS, Player.Backpack)
    
    for logStaticID in LOG_STATIC_IDS:
        logs = find_all_in_container_by_id(logStaticID, containerSerial = Player.Backpack.Serial)
        for log in logs:
            if dropOnGround:
                Player.HeadMessage(48, "Dropping Logs on ground")
                Items.MoveOnGround(log, 0, Player.Position.X - 1, Player.Position.Y + 1, 0)
            elif cutLogsToBoards:
                Items.UseItem(axe)
                Target.WaitForTarget(10000, False)
                Target.TargetExecute(log.Serial)
                
    packAnimals = get_friends_by_names(friendNames = packAnimalNames, range = 2)
    if len(packAnimals) > 0:
        for packAnimal in packAnimals:
            print(packAnimal.Name, packAnimal.Backpack.Weight)
            if packAnimal.Backpack.Weight < 1350:
                for itemStaticID in BOARD_STATIC_IDS:
                    move_item_to_container_by_id(itemStaticID , Player.Backpack.Serial, packAnimal.Backpack.Serial)    
            
            
# Variation of above that will get kindling usinga knife
def get_kindling_in_area(tileRange = 10, weightLimit = 350):
    global treenumber, treeposx, treeposy, DAGGER_STATIC_IDS
    
    Misc.SendMessage("Getting Kindling", 123)
    dagger = find_first_in_container_by_ids(DAGGER_STATIC_IDS, Player.Backpack)
    
    ScanStatic(tileRange)
    i = 0
    Misc.SendMessage("Total tree number {}".format(treenumber))
    while i < treenumber:
        Misc.SendMessage("Moving to a tree")
        go_to_tile(treeposx[i] - 1, treeposy[i] - 1, 88.0)
        CutTree(i, dagger, weightLimit)
        
        i = i + 1
        Misc.Pause(500)
        
    treeposx = []
    treeposy = []
    treeposz = []
    treegfx = []
    treenumber = 0

    Misc.SendMessage("All done", 123) 
    
def run_mining_loop(
    # Required. Your fire beetles name.
    forgeAnimalName = None,
    
    # Required. One or more blue beetle names.
    packAnimalNames = []):
    
    def getMinerTool():
        for minerToolStaticID in MINER_TOOLS_STATIC_IDS:
            miningTool = find_in_container_by_id(minerToolStaticID, Player.Backpack.Serial)
            if miningTool is not None:
                return miningTool    

    def smelt_ore(forgeAnimalName):
        forgeAnimals = get_friends_by_names(friendNames = [forgeAnimalName], range = 2)
        if len(forgeAnimals) > 0:
            for oreId in ORE_STATIC_IDS:
                ores = find_all_in_container_by_id(oreId, Player.Backpack.Serial)
                for ore in ores:
                    Journal.Clear()
                    Items.UseItem(ore)
                    Target.WaitForTarget(5000, True)
                    Target.TargetExecute(forgeAnimals[0])
                    Misc.Pause(PAUSE_DELAY_MS)
                    if Journal.Search("There is not enough metal-bearing ore in this pile to make an ingot."):
                        print(ore)
                        print(ore.Serial)
                        #Items.DropItemGroundSelf(ore, ore.Amount)
                        #Items.MoveOnGround(ore, 0, Player.Position.X - 1, Player.Position.Y + 1, 0)
                        #Items.MoveOnGround(ore, 0, Player.Position.X -1 , Player.Position.Y , 0)
                        tileX, tileY, tileZ = get_tile_in_front()
                        Items.MoveOnGround(ore, 0, tileX, tileY , 0)
                        Misc.Pause(PAUSE_DELAY_MS)
            Misc.Pause(PAUSE_DELAY_MS)     
        else:
            print("No forge animal found")


    def move_ingots_to_pack_animal(packAnimalNames):    
        packAnimals = get_friends_by_names(friendNames = packAnimalNames, range = 2)
        if len(packAnimals) > 0:
            for packAnimal in packAnimals:
                print(packAnimal.Name, packAnimal.Backpack.Weight)
                if packAnimal.Backpack.Weight < 1350:
                    for itemStaticID in INGOT_STATIC_IDS + STONE_STATIC_IDS + SAND_STATIC_IDS:
                        move_item_to_container_by_id(itemStaticID, Player.Backpack.Serial, packAnimal.Backpack.Serial)                
                        
    def readJournal():
        if Journal.Search('no metal') or Journal.Search('t mine that') or Journal.Search('no sand'):
            Journal.Clear()
            return True
        else:
            Journal.Clear()
            return False
            
    # Gets the tile serial. This isnt a trivial task.
    # Searching by cave floor tile id. Then doing an item search.
    # The cave floor tile is apparently an item with a serial. That is
    # how we get the serial.
    # The tile serial is provided to Target execute. We cant just use
    # the x,y coords because it doesnt work. It just says you cant mine there.
    # Also cant use target relative.
    def get_tile_in_front_serial():
        tileX, tileY, tileZ = get_tile_in_front()
        #tileinfo = Statics.GetStaticsLandInfo(tileX, tileY, Player.Map)

        filter = Items.Filter()
        # 0x053B is Cave floor
        # 0x0018 is Sand
        filter.Graphics = List[Int32]((0x053B))
        filter.OnGround = True
        filter.RangeMax = 1
        items = Items.ApplyFilter(filter)
        for item in items:
            if item.Position.X == tileX and item.Position.Y == tileY:
                return item.Serial, tileX, tileY, tileZ 
        return None, tileX, tileY, tileZ 
                
    while True:
        smelt_ore(forgeAnimalName)
        #Misc.Pause(250)
        move_ingots_to_pack_animal(packAnimalNames)
        #Misc.Pause(250)
        
        miningTool = getMinerTool()
        Journal.Clear()
        Items.UseItem(miningTool)
        Target.WaitForTarget(5000, True)
        #Target.TargetExecuteRelative(Player.Serial, 1)
    #    tileX, tileY, tileZ = get_tile_in_front()
    #    tileinfo = Statics.GetStaticsLandInfo(tileX, tileY, Player.Map)
        #Target.TargetExecute(tileX, tileY, tileZ, tileinfo.StaticID)
        
        tileSerial, tileX, tileY, tileZ  = get_tile_in_front_serial()
        if tileSerial is not None:
            Target.TargetExecute(tileSerial)
        else:
            Target.TargetExecute(tileX, tileY, tileZ)
        #Target.TargetExecute(tileX, tileY, tileZ)
        #print("TILE", tileX, tileY, tileZ)
        #print("PLAYER", Player.Position.X, Player.Position.Y, Player.Position.Z)
        
        Misc.Pause(PAUSE_DELAY_MS)
        
        #smelt_ore()
        #move_ingots_to_pack_animal()
        
        boolMove = readJournal()
        if boolMove:
            move(1)
            

        Misc.Pause(PAUSE_DELAY_MS)
        
# Auto fishes in all the lands. Works on a boat. Works on a dock.
# If you are on a boat, you can use the moveTiles param to move boat after each fishing attempt.
# It will say forward one X number of times.
# Can automatically cut fish. Can automatically store fish in hold.
def run_fishing_loop(
    # How many tiles in front of character to fish
    fishRange = 4, 
    
    # If on a boat, tells the tiller to move forward this many times.
    moveTiles = 2, 
    
    # How long to pause between casts
    fishDelayMs = 10000,
    
    # 0 = Do nothing, leave in backpack
    # 1 = cut fish with dagger to reduce weight, makes lots of fish steaks
    # 2 = place fish in cargo hold of ship, have to be standing near cargo hold
    fishHandling = 0,
    
    # Will not do any fishHandling operations on this fish. Leaves it in backpack. Useful for fishing quests.
    fishToKeep = None
):
    
    rightHand = Player.GetItemOnLayer("RightHand")
    if rightHand == None:
        print("Need a fishing pole")
        return False
        
    while True:
        
        # Cut fish they are heavy
        if fishHandling == 1:
            dagger = find_first_in_container_by_ids(DAGGER_STATIC_IDS)
            if dagger is not None:
                fishies = find_all_in_container_by_ids(FISH_STATIC_IDS)
                for fish in fishies:
                    if fishToKeep is not None and fish.Name.lower().find(fishToKeep.lower()) > -1:
                        Player.HeadMessage(28, "Keeping fish {} item id {}".format(fish.Name, fish.ItemID))
                        continue
                    print("Cutting fish {} item id {}".format(fish.Name, fish.ItemID))
                    Items.UseItem(dagger)
                    Target.WaitForTarget(1000, False)
                    Target.TargetExecute(fish)
            else:
                print("You have elected to cut fish however no dagger was found in backpack.")
                return
        elif fishHandling == 2:
            fishies = find_all_in_container_by_ids(FISH_STATIC_IDS)
            fil = Items.Filter()
            fil.Name = "cargo hold"
            fil.RangeMax = 3
            hatches = Items.ApplyFilter(fil)
            if len(hatches) > 0:
                for fish in fishies:
                    if fishToKeep is not None and fish.Name.lower().find(fishToKeep.lower()) > -1:
                        Player.HeadMessage(28, "Keeping fish {} item id {}".format(fish.Name, fish.ItemID))
                        continue
                    print("Moving fish {} item id {}".format(fish.Name, fish.ItemID))                        
                    move_item_to_container(fish, hatches[0].Serial)
                    
        Target.Cancel()
        Items.UseItem(rightHand)
        Target.WaitForTarget(2000, False)
        x, y, z = get_tile_in_front(fishRange)
        
        # The people who made this game made some questionable decisions.
        # If we are in britain, the water tile is the land tile.
        # If we are in tokumo, the water tile is a static tile on top of land tile.
        # So, we will look for something with the "Wet" flag and go from there.
        fished = False
        
        #print("------------- TILE INFO -----------------")
        tileInfoList = Statics.GetStaticsTileInfo(x, y, Player.Map)
        #print("TileInfo Len = {}".format(len(tileInfoList)))
        if len(tileInfoList) > 0:
            for tileInfo in tileInfoList:
                #print("TileInfo 1 StaticID = {}, StaticZ = {}".format(tileInfo.StaticID, tileInfo.StaticZ))
                val = Statics.GetTileFlag(tileInfo.StaticID,"Wet")
                #print("Is Wet = {}".format(val))
                if Statics.GetTileFlag(tileInfo.StaticID,"Wet") == True:
                    print("TargetExecute(x = {}, y = {}, staticZ = {}, staticId = {})".format(x, y, tileInfo.StaticZ, tileInfo.StaticID))
                    Target.TargetExecute(x, y, tileInfo.StaticZ, tileInfo.StaticID)
                    fished = True
                    Misc.Pause(fishDelayMs)
                    break

        if not fished:
            #print("------------- LAND INFO -----------------")                    
            landInfo = Statics.GetStaticsLandInfo(x,y,Player.Map)
            if landInfo is not None:
                #print("LandInfo StaticID = {}, StaticZ = {}".format(landInfo.StaticID, landInfo.StaticZ))
                val = Statics.GetLandFlag(landInfo.StaticID,"Wet")
                #print("Is Wet = {}".format(val))     
                if Statics.GetLandFlag(landInfo.StaticID,"Wet"):
                    #print("TargetExecute(x = {}, y = {}, staticZ = {})".format(x, y, landInfo.StaticZ))
                    Target.TargetExecute(x, y, landInfo.StaticZ)
                    Misc.Pause(fishDelayMs)
                    fished = True
                else:
                    print("This tile is not wet")

        for i in range(0, moveTiles):
            Player.ChatSay("forward one")
            Misc.Pause(500)
