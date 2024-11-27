# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-11-21
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
from Scripts.fm_core.core_player import move_item_to_container
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

# Loots items near player into pack animal
PACK_ANIMAL_NAMES = ["one", "two", "three", "four"]

Timer.Create( 'pingTimer', 1 )



#item = Items.FindBySerial(0x4003E0B4)
#item = Items.FindBySerial(0x40E2C44B)

#print(item)
#print(item.IsContainer)
#print(item.Weight)
#print(item.Contains)
#print(item.Contains.Count)
#sys.exit()

#List[Item]()

while True:
    
    if Timer.Check( 'pingTimer' ) == False:
        Player.HeadMessage( 118, "Ground Looter Running...")
        Timer.Create( 'pingTimer', 3000)
        
    filter = Items.Filter()
    # 0x053B is Cave floor
    # 0x0018 is Sand
    #filter.Graphics = List[Int32]((0x053B))
    filter.Movable = 1
    filter.OnGround = True
    filter.RangeMax = 2
    items = Items.ApplyFilter(filter)

    packAnimals = get_friends_by_names(friendNames = PACK_ANIMAL_NAMES, range = 2)
    for item in items:
      
        if len(packAnimals) > 0:
            for packAnimal in packAnimals:
                print("Animal: {}, Weight: {}, Items: {}".format(packAnimal.Name, packAnimal.Backpack.Weight, packAnimal.Backpack.Contains.Count))
                if packAnimal.Backpack.Weight + item.Weight < 1350:
                    if item.IsContainer:
                        if item.Contains.Count + packAnimal.Backpack.Contains.Count < 125:
                            print("Moving container {}".format(item.Name))
                            move_item_to_container(item, packAnimal.Backpack.Serial)
                            break
                        else:
                            print("Not moving container because there are too many items in the container")
                    else:
                        print("Moving container {}".format(item.Name))
                        move_item_to_container(item, packAnimal.Backpack.Serial)
                        break
                else:
                    print("Not moving item {} because it is too heavy".format(item.Name))
    Misc.Pause(650)                    
