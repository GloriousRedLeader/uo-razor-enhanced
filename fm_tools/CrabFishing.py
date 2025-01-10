# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-03-26
# Use at your own risk. 


from System.Collections.Generic import List
import sys
import time
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
from Scripts.fm_core.core_items import LOBSTER_TRAP_STATIC_IDS
from Scripts.fm_core.core_items import DEPLOYED_LOBSTER_TRAP_STATIC_ID


traps = []
trapItems = find_all_in_container_by_ids(LOBSTER_TRAP_STATIC_IDS)
for trapItem in trapItems:
    if trapItem.Name == "empty lobster trap":
        traps.append(trapItem)
#traps = Items.FindByName("empty lobster trap", -1, Player.Backpack.Serial, 1)

waitMs = 65000
maxTraps = 19
actualTraps = len(traps)

Player.HeadMessage(38, "Stand in middle of cargo hold")
Misc.Pause(500)
Player.HeadMessage(38, "You have {}/{} lobster traps". format(actualTraps, maxTraps))

trapNum = 1
for trap in traps:
    
    Target.Cancel()
    print(trap.Name)
    if trap.Name != "empty lobster trap":
        continue
    Items.UseItem(trap)
    Target.WaitForTarget(2000)
    if trapNum == 1:
        x = Player.Position.X + 6
        y = Player.Position.Y - 6
        z = Player.Position.Z
    elif trapNum == 2:
        x = Player.Position.X + 6
        y = Player.Position.Y - 4
        z = Player.Position.Z
    elif trapNum == 3:
        x = Player.Position.X + 6
        y = Player.Position.Y - 2
        z = Player.Position.Z        
    elif trapNum == 4:
        x = Player.Position.X + 6
        y = Player.Position.Y
        z = Player.Position.Z
    elif trapNum == 5:
        x = Player.Position.X + 6
        y = Player.Position.Y + 2
        z = Player.Position.Z    
    elif trapNum == 6:
        x = Player.Position.X + 6
        y = Player.Position.Y + 4
        z = Player.Position.Z        
    elif trapNum == 7:
        x = Player.Position.X + 6
        y = Player.Position.Y + 6
        z = Player.Position.Z                
    elif trapNum == 8:
        x = Player.Position.X + 4
        y = Player.Position.Y + 6
        z = Player.Position.Z   
    elif trapNum == 9:
        x = Player.Position.X + 2
        y = Player.Position.Y + 6
        z = Player.Position.Z    
    elif trapNum == 10:
        x = Player.Position.X + 0
        y = Player.Position.Y + 6
        z = Player.Position.Z    
    elif trapNum == 11:
        x = Player.Position.X - 2
        y = Player.Position.Y + 6
        z = Player.Position.Z    
    elif trapNum == 12:
        x = Player.Position.X - 4
        y = Player.Position.Y + 6
        z = Player.Position.Z    
    elif trapNum == 13:
        x = Player.Position.X - 6
        y = Player.Position.Y + 6
        z = Player.Position.Z    
    elif trapNum == 14:
        x = Player.Position.X - 6
        y = Player.Position.Y + 4
        z = Player.Position.Z          
    elif trapNum == 15:
        x = Player.Position.X - 6
        y = Player.Position.Y + 2
        z = Player.Position.Z    
    elif trapNum == 16:
        x = Player.Position.X - 6
        y = Player.Position.Y
        z = Player.Position.Z
    elif trapNum == 17:
        x = Player.Position.X - 6
        y = Player.Position.Y - 2
        z = Player.Position.Z  
    elif trapNum == 18:
        x = Player.Position.X - 6
        y = Player.Position.Y - 4
        z = Player.Position.Z   
    elif trapNum == 19:
        x = Player.Position.X - 6
        y = Player.Position.Y - 6
        z = Player.Position.Z            
    else:
        
        break

    #location = Player.Position.
    Target.TargetExecute(x,y,z)
    Misc.Pause(650)
    
    trapNum = trapNum + 1
    if trapNum > maxTraps or trapNum > actualTraps:
        Player.HeadMessage(38, "all traps out")
        break

start = time.time()

Player.HeadMessage(38, "All traps deployed, now we wait")
Misc.Pause(waitMs)

Player.HeadMessage(38, "Time to collect traps")
filter = Items.Filter()
filter.Graphics = List[Int32]((DEPLOYED_LOBSTER_TRAP_STATIC_ID)) # This filter doesnt work
filter.Movable = 0
filter.OnGround = True
filter.RangeMax = 7
items = Items.ApplyFilter(filter)

for item in items:
    if item.ItemID == DEPLOYED_LOBSTER_TRAP_STATIC_ID:
        Items.UseItem(item)
        print("Clicking item {}".format(item.Name))
        Misc.Pause(650)

Player.HeadMessage(38, "Time to let the crabs out of the traps")
Misc.Pause(2000)

trapItems = find_all_in_container_by_ids(LOBSTER_TRAP_STATIC_IDS)
for trapItem in trapItems:
    if trapItem.Name != "empty lobster trap":
        Items.UseItem(trapItem)
        Misc.Pause(650)
        Target.Cancel()
        
Player.HeadMessage(38, "Move crabs to hold")
Misc.Pause(2000)

fishies = find_all_in_container_by_ids(FISH_STATIC_IDS)
fil = Items.Filter()
fil.Name = "cargo hold"
fil.RangeMax = 3
hatches = Items.ApplyFilter(fil)
if len(hatches) > 0:
    for fish in fishies:
        print("Moving fish {} item id {}".format(fish.Name, fish.ItemID))                        
        move_item_to_container(fish, hatches[0].Serial)