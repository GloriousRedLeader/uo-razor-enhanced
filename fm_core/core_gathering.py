from Scripts.fm_core.core_player import find_first_in_container_by_ids, find_first_in_hands_by_id
from Scripts.fm_core.core_player import move_all_items_from_container
from Scripts.fm_core.core_player import move_item_to_container_by_id
from Scripts.fm_core.core_rails import go_to_tile
from Scripts.fm_core.core_mobiles import get_friends_by_names
from Scripts.fm_core.core_items import AXE_STATIC_IDS, LOG_STATIC_IDS, TREE_STATIC_IDS, DAGGER_STATIC_IDS, BOARD_STATIC_IDS
from System.Collections.Generic import List
import sys

# All credit to: https://github.com/hampgoodwin/razorenhancedscripts/blob/master/LumberjackingScanTile.py
# Note I did modify this and make it much worse. Use the one linked above.

Misc.Resync()

# Pastrami
CHOP_DELAY = 2000

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
    logs = find_first_item_by_id(LOG_STATIC_IDS, Player.Backpack)
    if logs != None:
        Items.UseItem(axe)
        Target.WaitForTarget(4000)
        Target.WaitForTarget(10000, False)
        Target.TargetExecute(logs.Serial)
            
# Makes a box around where player is standing and chops trees inside. The
# size of the box is determined by tileRange.
# You will need an axe equipped I believe.
def chop_trees_in_area(
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
        
    Misc.Resync()
    global tileinfo, treenumber, treeposx, treeposy, treeposz, treegfx, blockcount, TREE_STATIC_IDS, AXE_STATIC_IDS, CHOP_DELAY
    
    
    
    #tileinfo = List[Statics.TileInfo]
    #treeposx = []
    #treeposy = []
    #treeposz = []
    #treegfx = []
    #treenumber = 0
    #blockcount = 0    
                
#    packAnimals = get_friends_by_names(friendNames = packAnimalNames, range = 2)
#    if len(packAnimals) > 0:
#        for packAnimal in packAnimals:
#            print(packAnimal.Name, packAnimal.Backpack.Weight)
#            if packAnimal.Backpack.Weight < 1350:
#                for boardStaticID in BOARD_STATIC_IDS:
#                    move_item_to_container_by_id(boardStaticID, Player.Backpack, packAnimal.Backpack.Serial)
#    return

    Misc.SendMessage("--> Avvio Patramie", 77)  
    Misc.SendMessage("Eqipping Axe", 123)
    
    originalItemsInHands = [None, None]
    axe = find_first_in_hands_by_id(AXE_STATIC_IDS)
    if axe == None:
        axe = find_first_item_by_id(AXE_STATIC_IDS, Player.Backpack)
        if axe == None:
            Misc.SendMessage("You dont have an axe foo", 38)
            sys.exit()
        originalItemsInHands = swap_weapon(axe)

    ScanStatic(tileRange)
    i = 0
    Misc.SendMessage("Total tree number {}".format(treenumber))
    while i < treenumber:
        Misc.SendMessage("Moving to a tree")
        #go_to_tile(treeposx[i] - 1, treeposy[i] - 1, 88.0)
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

    Misc.SendMessage("Re-qeuipping shitter", 123) 
    
    if originalItemsInHands[0] != None:
        Misc.Pause(1000)
        swap_weapon(originalItemsInHands[0])
        Misc.Pause(4000)
        
    if originalItemsInHands[1] != None:
        Misc.Pause(1000)
        swap_weapon(originalItemsInHands[1])
        Misc.Pause(4000)
        
def cut_drop_and_move_boards(axe, cutLogsToBoards = False, dropOnGround = False, packAnimalNames = []):
    global treenumber, treeposx, treeposy, treeposz, treegfx, blockcount, TREE_STATIC_IDS, AXE_STATIC_IDS, CHOP_DELAY
    logs = find_first_in_container_by_ids(LOG_STATIC_IDS, Player.Backpack)
    if logs != None and dropOnGround:
        Player.HeadMessage(48, "Dropping Logs on ground")
        Items.MoveOnGround(logs,0,Player.Position.X - 1, Player.Position.Y + 1, 0)
    elif logs != None and cutLogsToBoards:
        Items.UseItem(axe)
        Target.WaitForTarget(10000, False)
        Target.TargetExecute(logs.Serial)
        
    packAnimals = get_friends_by_names(friendNames = packAnimalNames, range = 2)
    if len(packAnimals) > 0:
        for packAnimal in packAnimals:
            print(packAnimal.Name, packAnimal.Backpack.Weight)
            if packAnimal.Backpack.Weight < 1350:
                for boardStaticID in BOARD_STATIC_IDS:
                    move_item_to_container_by_id(boardStaticID, Player.Backpack, packAnimal.Backpack.Serial)    
        
            
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