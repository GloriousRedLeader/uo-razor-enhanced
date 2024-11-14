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
