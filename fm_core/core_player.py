# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-03-26
# Use at your own risk. 

# Player related functions like looking through items in backpack or equipped items.

from Scripts.fm_core.core_items import INSTRUMENT_STATIC_IDS

# Takes a list of itemIDs and returns the first one it finds.
def find_first_in_container_by_ids(itemIDs, container):
    for itemID in itemIDs:
        item = find_in_container_by_id(itemID, container)
        if item != None:
            return item
    return None

# Method liberated (CREDIT AUTHOR)
def find_in_container_by_id(itemID, container, color = -1, ignoreContainer = []):
    ignoreColor = False
    if color == -1:
        ignoreColor = True

    if isinstance( itemID, int ):
        foundItem = next( ( item for item in container.Contains if ( item.ItemID == itemID and ( ignoreColor or item.Hue == color ) ) ), None )
    elif isinstance( itemID, list ):
        foundItem = next( ( item for item in container.Contains if ( item.ItemID in itemID and ( ignoreColor or item.Hue == color ) ) ), None )
    else:
        raise ValueError( 'Unknown argument type for itemID passed to FindItem().', itemID, container )

    if foundItem != None:
        return foundItem

    subcontainers = [ item for item in container.Contains if ( item.IsContainer and not item.Serial in ignoreContainer ) ]
    for subcontainer in subcontainers:
        foundItem = find_in_container_by_id( itemID, subcontainer, color, ignoreContainer )
        if foundItem != None:
            return foundItem

# checks list of itemids and returns first one that matches
# one in either hand.
def find_first_in_hands_by_id(itemIDs):
    for itemID in itemIDs:
        item = find_in_hands_by_id(itemID)
        if item != None:
            return item
    return None    

# Returns a single item based on an item id
def find_in_hands_by_id(itemID): 
    leftHand = Player.GetItemOnLayer("LeftHand")
    if leftHand != None:
        return leftHand
    rightHand = Player.GetItemOnLayer("RightHand")
    if rightHand != None:
        return rightHand
    return None
    
# Unequips current items and returns them in an array
# Equips item provided as argument. This is useful for
# swapping items for harvesting like axes and pickaxes.
# Note: Right now it just undresses left hand. If you
# have a 2 hander or something in yoru right hand, you may 
# be effed.
def swap_weapon(newItem):
    leftHand = Player.GetItemOnLayer("LeftHand")
    if leftHand != None:
        Player.UnEquipItemByLayer("LeftHand", True)    
        Misc.Pause(1000)      
        
    rightHand = Player.GetItemOnLayer("RightHand")        
    if rightHand != None:
        Player.UnEquipItemByLayer("RightHand", True)    
        Misc.Pause(1000)      
    
    Player.EquipItem(newItem)    
    Misc.Pause(1000)      
    return [leftHand, rightHand]
    
# Liberated from another script (CREDIT AUTHOR)
# Original method name: def FindInstrument( container )
def find_instrument( container ):
    global INSTRUMENT_STATIC_IDS
    return find_first_in_container_by_ids( INSTRUMENT_STATIC_IDS, container )
    
# Give it a list of item ids and it will deposit into bank
# Gold is 0x0EED
def open_bank_and_deposit_items(itemIDs = []):
    Player.HeadMessage(48, "Depositing Items...")
    Player.ChatSay(48, 'banco')
    Misc.Pause(600)
    depositCount = 0
    for itemID in itemIDs:
        while True:
            item = find_in_container_by_id(itemID, Player.Backpack)
            if item == None:
                break
            Player.HeadMessage(48, "Depositing {}".format(item.Name))
            Items.Move(item, Player.Bank, item.Amount)
            depositCount = depositCount + 1
            Misc.Pause(600)
    Player.HeadMessage(48, "[done] Deposited {} items.".format(depositCount))
            