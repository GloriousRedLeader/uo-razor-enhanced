# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-03-26
# Use at your own risk. 

# Player related functions like looking through items in backpack or equipped items.

from Scripts.fm_core.core_items import INSTRUMENT_STATIC_IDS
from Scripts.fm_core.core_mobiles import get_friends_by_names

# Gets one item by item name from backpack
def find_first_in_container_by_name(itemName, container = Player.Backpack.Serial):
    return Items.FindByName(itemName, -1, container, 1)

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
    Player.HeadMessage(455, "[start] Depositing Items...")
    Player.ChatSay(48, 'banco')
    Misc.Pause(600)
    depositCount = 0
    for itemID in itemIDs:
        while True:
            item = find_in_container_by_id(itemID, Player.Backpack)
            if item == None:
                break
            Player.HeadMessage(455, "Depositing {}".format(item.Name))
            Items.Move(item, Player.Bank, item.Amount)
            depositCount = depositCount + 1
            Misc.Pause(600)
    Player.HeadMessage(455, "[done] Depositing {} items.".format(depositCount))
            
# This will get us items from our bank box and put them in our backpack.
# Use this to get regs, bandages, potions, etc.
# Will stop if cannot find the amount required.
def open_bank_and_resupply(
    # An array of tuples (<item id>, <amount>)
    itemsNeeded = []):

    #Player.HeadMessage(455, "[start] Resupplying...")
    Player.ChatSay(48, 'banco')
    Misc.Pause(1000)
 
    for itemID, amount in itemsNeeded:
        count = Items.ContainerCount(Player.Backpack, itemID, -1, True)
        print("Currenlty have {} / {} of itemID in backpack".format(count, amount))
    #Player.HeadMessage(455, "[done] Resupplying...")
    
def move_item_to_container_by_id(itemID, sourceContainer, destinationContainerSerial):
    while True:
        item = find_in_container_by_id(itemID, sourceContainer, color = -1, ignoreContainer = [])
        if item is not None:
            move_item_to_container(item, destinationContainerSerial)
        else:
            break
    
def move_item_to_container(item, destinationContainerSerial):
    Items.Move(item, destinationContainerSerial, item.Amount)
    Misc.Pause(800)
    
# Nice utility to just move junk from one bag to another.
def move_all_items_from_container(sourceContainerSerial, destinationContainerSerial):
    for item in Items.FindBySerial(sourceContainerSerial).Contains:
        Player.HeadMessage(455, "Junking item {}".format(item.Name))
        Items.Move(item, destinationContainerSerial, item.Amount)
        Misc.Pause(800)
        
def move_all_items_of_type_to_container():
    itemSerial = Target.PromptTarget("Which item type? Click one.")
    #source = Target.PromptTarget("Pick source container")
    destinationSerial = Target.PromptTarget("Pick target container")
    
    
    #Items.UseItem(source)
    #Misc.Pause(650)
    Items.UseItem(destinationSerial)
    Misc.Pause(650)
    
    
    
    item = Items.FindBySerial(itemSerial)
    if item is not None:
        print(item.ItemID, item.Container, item.Container)
        sourceContainer = Items.FindBySerial(item.Container)
        #move_item_to_container_by_id(itemID, sourceContainer, destinationContainerSerial):
        move_item_to_container_by_id(item.ItemID, sourceContainer, destinationSerial)
    #move_item_to_container_by_id(itemID = item.ItemID, sourceContainer = source, destinationContainerSerial = destination.Serial)   
        
def move_number_of_items_from_container():
    
    print("How many items?")
    Journal.Clear()
    while True:
        res = Journal.GetTextByName(Player.Name)
        if len(res) > 0:
            maxNum = int(res[0])
            break
        Misc.Pause(250)    
    
    #Player.HeadMessage(455, "[start] Cleaing up Britain...")
    source = Target.PromptTarget("Pick source container")
    
    destination = Target.PromptTarget("Pick target container")
    
    Items.UseItem(source)
    Misc.Pause(650)
    Items.UseItem(destination)
    Misc.Pause(650)

    #maxNum = 50
    currentNum = 0
    #items = Items.FindBySerial(source.Serial)
    for item in Items.FindBySerial(source).Contains:
        Player.HeadMessage(455, "Moving item #{}: {}".format(currentNum, item.Name))
        Items.Move(item, destination, item.Amount)
        Misc.Pause(650)
        
        if currentNum >= maxNum:
            Player.HeadMessage(455, "Done. Moved {}/{}".format(currentNum, maxNum))
            return
        currentNum = currentNum + 1            

        
def drop_all_items_from_container_to_floor():
    
    source = Target.PromptTarget("Pick source container")
    
    #Items.UseItem(source)
    #Misc.Pause(650)
    
    container = Mobiles.FindBySerial(source)
    
    

    #for item in Items.FindBySerial(source).Contains:
    for item in Items.FindBySerial(container.Serial).Contains:        
        Player.HeadMessage(455, "Moving item #{}: {}".format(currentNum, item.Name))
        Items.DropItemGroundSelf(item, item.Amount())
        Misc.Pause(650)

def drop_all_items_from_pack_animal_to_floor(packAnimalNames = []):
    currentNum = 1        
    packAnimals = get_friends_by_names(friendNames = packAnimalNames, range = 2)
    if len(packAnimals) > 0:
        for packAnimal in packAnimals:
            for item in Mobiles.FindBySerial( packAnimal.Serial ).Backpack.Contains:
                Player.HeadMessage(455, "Moving item #{} {}".format(currentNum, item.Name))
                #Items.DropItemGroundSelf(item, item.Amount)
                Items.MoveOnGround(item, 0, Player.Position.X - 1, Player.Position.Y + 1, 0)
                Misc.Pause(650)
                currentNum = currentNum + 1
