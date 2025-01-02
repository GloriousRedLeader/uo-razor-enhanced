# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-03-26
# Use at your own risk. 

# Player related functions like looking through items in backpack or equipped items.

from Scripts.fm_core.core_items import INSTRUMENT_STATIC_IDS
from Scripts.fm_core.core_items import GOLD_STATIC_IDS
from Scripts.fm_core.core_mobiles import get_friends_by_names

# Gets a list of items by item id
def find_all_in_container_by_id(itemID, containerSerial = Player.Backpack.Serial):
    return Items.FindAllByID(itemID, -1, containerSerial, 1)

# Gets a list of items by multiple item ids
def find_all_in_container_by_ids(itemIDs, containerSerial = Player.Backpack.Serial):
    items = []
    for itemID in itemIDs:
        items = items + Items.FindAllByID(itemID, -1, containerSerial, 1)
    return items
    
# Gets one item by item name from backpack
def find_first_in_container_by_name(itemName, containerSerial = Player.Backpack.Serial):
    return Items.FindByName(itemName, -1, containerSerial, 1)

# Takes a list of itemIDs and returns the first one it finds.
def find_first_in_container_by_ids(itemIDs, containerSerial = Player.Backpack.Serial):
    for itemID in itemIDs:
        item = find_in_container_by_id(itemID, containerSerial)
        if item != None:
            return item
    return None

# Method liberated (CREDIT AUTHOR)
# This one is pretty much called by all the other functions.
# Finds one instance of itemID in containerSerial
# Note that itemID can be a single itemID or a list of itemID
def find_in_container_by_id(itemID, containerSerial = Player.Backpack.Serial, color = -1, ignoreContainer = []):
    ignoreColor = False
    if color == -1:
        ignoreColor = True
        
    container = Items.FindBySerial(containerSerial)

    if isinstance( itemID, int ):
        foundItem = next( ( item for item in container.Contains if ( item.ItemID == itemID and ( ignoreColor or item.Hue == color ) ) ), None )
    elif isinstance( itemID, list ):
        foundItem = next( ( item for item in container.Contains if ( item.ItemID in itemID and ( ignoreColor or item.Hue == color ) ) ), None )
    else:
        raise ValueError( 'Unknown argument type for itemID passed to FindItem().', itemID, container )

    if foundItem != None:
        return foundItem

    #subcontainers = [ item for item in container.Contains if ( item.IsContainer and not item.Serial in ignoreContainer ) ]
    #for subcontainer in subcontainers:
    #    foundItem = find_in_container_by_id( itemID, subcontainer, color, ignoreContainer )
    #    if foundItem != None:
    #        return foundItem

# checks list of itemids and returns first one that matches
# one in either hand.
def find_first_in_hands_by_id(itemIDs):
    for itemID in itemIDs:
        item = find_in_hands_by_id(itemID)
        if item != None:
            return item
    return None    

# Returns a single item based on an item id
# Fix this trash.
def find_in_hands_by_id(itemID): 
    leftHand = Player.GetItemOnLayer("LeftHand")
    if leftHand != None and leftHand.ItemID == itemID:
        return leftHand
    rightHand = Player.GetItemOnLayer("RightHand")
    if rightHand != None and rightHand.ItemID == itemID:
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
            item = find_in_container_by_id(itemID)
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

# Moves all items matching type of itemID from sourceSerial container
# to destinationSerial container    
def move_item_to_container_by_id(itemID, sourceSerial, destinationSerial):
    while True:
        item = find_in_container_by_id(itemID, sourceSerial, color = -1, ignoreContainer = [])
        if item is not None:
            move_item_to_container(item, destinationSerial)
        else:
            break
# item is an instance of Item
# destinationSerial is container serial
# Moves one stack of the item
def move_item_to_container(item, destinationSerial):
    Items.Move(item, destinationSerial, item.Amount)
    Misc.Pause(800)
    
# Nice utility to just move junk from one bag to another.
def move_all_items_from_container(sourceSerial, destinationSerial):
    for item in Items.FindBySerial(sourceSerial).Contains:
        Player.HeadMessage(455, "Junking item {}".format(item.Name))
        Items.Move(item, destinationSerial, item.Amount)
        Misc.Pause(800)
        
# Prompts for an item type
# Source is that items container
# Destination is prompt
# Moves all items with that ItemID
def move_all_items_of_type_to_container():
    itemSerial = Target.PromptTarget("Which item type? Click one.")
    destinationSerial = Target.PromptTarget("Pick target container")

    Items.UseItem(destinationSerial)
    Misc.Pause(650)

    item = Items.FindBySerial(itemSerial)
    if item is not None:
        sourceSerial = Items.FindBySerial(item.Container).Serial
        move_item_to_container_by_id(item.ItemID, sourceSerial, destinationSerial)

        
# Provide list of item ids.
# Prompt for source container.
# Prompt for destination container.
def move_all_items_by_ids_to_container(itemIDs):
    sourceSerial = Target.PromptTarget("Pick source container")
    destinationSerial = Target.PromptTarget("Pick target container")
    
    Items.UseItem(sourceSerial)
    Misc.Pause(650)
    Items.UseItem(destinationSerial)
    Misc.Pause(650)

    for itemID in itemIDs:
        move_item_to_container_by_id(itemID, sourceSerial, destinationSerial)

# Enter number of items to move via chat
# Prompt for source container
# Prompt for destination container
# Moves that number of items from source to destination
def move_number_of_items_from_container():
    print("How many items?")
    Journal.Clear()
    while True:
        res = Journal.GetTextByName(Player.Name)
        if len(res) > 0:
            maxNum = int(res[0])
            break
        Misc.Pause(250)    
    
    source = Target.PromptTarget("Pick source container")
    destination = Target.PromptTarget("Pick target container")
    
    Items.UseItem(source)
    Misc.Pause(650)
    Items.UseItem(destination)
    Misc.Pause(650)

    currentNum = 0
    for item in Items.FindBySerial(source).Contains:
        Player.HeadMessage(455, "Moving item #{}: {}".format(currentNum, item.Name))
        Items.Move(item, destination, item.Amount)
        Misc.Pause(650)
        if currentNum >= maxNum:
            Player.HeadMessage(455, "Done. Moved {}/{}".format(currentNum, maxNum))
            return
        currentNum = currentNum + 1            

# Commenting out, dont think this works or its used
# Prompt for source container (must be a pack animal)
# Drops everything on the ground. May not work.
#def drop_all_items_from_container_to_floor():
#    source = Target.PromptTarget("Pick source container")
#    container = Mobiles.FindBySerial(source)
#
#    for item in Items.FindBySerial(container.Serial).Contains:        
#        Player.HeadMessage(455, "Moving item #{}: {}".format(currentNum, item.Name))
#        Items.DropItemGroundSelf(item, item.Amount())
#        Misc.Pause(650)

# Provide pack animal names as an array
# Drops their backpack to the floor
def drop_all_items_from_pack_animal_to_floor(packAnimalNames = []):
    currentNum = 0        
    packAnimals = get_friends_by_names(friendNames = packAnimalNames, range = 2)
    if len(packAnimals) > 0:
        for packAnimal in packAnimals:
            for item in Mobiles.FindBySerial( packAnimal.Serial ).Backpack.Contains:
                Player.HeadMessage(455, "Moving item #{} {}".format(currentNum, item.Name))
                Items.MoveOnGround(item, 0, Player.Position.X - 1, Player.Position.Y + 1, 0)
                Misc.Pause(650)
                currentNum = currentNum + 1
                
def use_bag_of_sending(
    # Threshold for a single gold stack before sending
    minGold = 50000):

    bag = find_first_in_container_by_name("a bag of sending", containerSerial = Player.Backpack.Serial)
    if bag is not None:
        goldPiles = find_all_in_container_by_ids(GOLD_STATIC_IDS)
        for goldPile in goldPiles:
            if goldPile.Amount >= minGold:
                Items.UseItem(bag)
                Target.WaitForTarget(1000, False)
                Target.TargetExecute(goldPile)
    else:
        print("No bag of sending found!")