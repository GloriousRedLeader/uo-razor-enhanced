from Scripts.fm_core.core_player import find_first_in_container_by_ids, find_first_in_hands_by_id
from Scripts.fm_core.core_rails import go_to_tile
from Scripts.fm_core.core_items import AXE_STATIC_IDS, LOG_STATIC_IDS, TREE_STATIC_IDS
from System.Collections.Generic import List
import sys

# All credit to: https://github.com/hampgoodwin/razorenhancedscripts/blob/master/LumberjackingScanTile.py
# Note I did modify this and make it much worse. Use the one linked above.

# Pastrami
CHOP_DELAY = 1000

# Variabili Sistema
tileinfo = List[Statics.TileInfo]
treeposx = []
treeposy = []
treeposz = []
treegfx = []
treenumber = 0
blockcount = 0

def RangeTree( spotnumber ):
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
    global treenumber, treeposx, treeposy, TREE_STATIC_IDS
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
                            Misc.SendMessage('--> Albero X: %i - Y: %i - Z: %i' % (minx, miny, tile.StaticZ), 66)
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
    global CHOP_DELAY
    global blockcount
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
    Target.TargetExecute(treeposx[spotnumber], treeposy[spotnumber], treeposz[spotnumber], treegfx[spotnumber])
    Misc.Pause(CHOP_DELAY)
    if Journal.Search("not enough wood"):
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
        CutTree(spotnumber, axe, weightLimit)
        
# Too heavy. Turn to boards. Praise Be.
def logs_to_boards(container, axe):
    logs = find_first_item_by_id(LOG_STATIC_IDS, Player.Backpack)
    if logs != None:
        Items.UseItem(axe)
        Target.WaitForTarget(4000)
        Target.WaitForTarget(10000, False)
        Target.TargetExecute(logs.Serial)
            
# Makes a box around where player is standing and chops trees inside. The
# size of the box is determined by tileRange.
# dropOnGround means we just chop and instantly drop to the floor, useful for gaining skilll
def chop_trees_in_area(tileRange = 10, weightLimit = 350, cutLogsToBoards = False, dropOnGround = False):
    global treenumber, treeposx, treeposy, AXE_STATIC_IDS
    
    Misc.SendMessage("--> Avvio Patramie", 77)  
    Misc.SendMessage("Eqipping Axe", 123)
    
    originalItemsInHands = [None, None]
    axe = find_first_in_hands_by_id(AXE_STATIC_IDS)
    if axe == None:
        axe = find_first_item_by_id(AXE_STATIC_IDS, Player.Backpack)
        if axe == None:
            Misc.SendMessage("You don't have an axe foo", 38)
            sys.exit()
        originalItemsInHands = swap_weapon(axe)

    ScanStatic(tileRange)
    i = 0
    Misc.SendMessage("Total tree number {}".format(treenumber))
    while i < treenumber:
        Misc.SendMessage("Moving to a tree")
        go_to_tile(treeposx[i] - 1, treeposy[i] - 1, 88.0)
        CutTree(i, axe, weightLimit)
        
        logs = find_first_in_container_by_ids(LOG_STATIC_IDS, Player.Backpack)
        if logs != None and dropOnGround:
            Player.HeadMessage(48, "Dropping Logs on ground")
            Items.MoveOnGround(logs,0,Player.Position.X - 1, Player.Position.Y + 1, 0)
        elif logs != None and cutLogsToBoards:
            Items.UseItem(axe)
            Target.WaitForTarget(4000)
            Target.WaitForTarget(10000, False)
            Target.TargetExecute(logs.Serial)
        i = i + 1
        Misc.Pause(500)
        
    treeposx = []
    treeposy = []
    treeposz = []
    treegfx = []
    treenumber = 0

    Misc.SendMessage("Re-qeuipping shitter", 123) 
    
    if originalItemsInHands[0] != None:
        Misc.Pause(1000)
        swap_weapon(originalItemsInHands[0])
        Misc.Pause(4000)
        
    if originalItemsInHands[1] != None:
        Misc.Pause(1000)
        swap_weapon(originalItemsInHands[1])
        Misc.Pause(4000)