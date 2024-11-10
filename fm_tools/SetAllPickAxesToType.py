# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-11-09
# Use at your own risk. 

from Scripts.fm_core.core_player import find_first_in_container_by_ids
from Scripts.fm_core.core_player import find_first_in_hands_by_id
from Scripts.fm_core.core_player import move_all_items_from_container
from Scripts.fm_core.core_player import move_item_to_container_by_id
from Scripts.fm_core.core_player import find_in_container_by_id
from Scripts.fm_core.core_player import find_first_in_container_by_name

from Scripts.fm_core.core_player import find_all_in_container_by_id
from Scripts.fm_core.core_items import MINER_TOOLS_STATIC_IDS

# Looks for pickaxes in your backpack, sets them all to a resource type.

# Choose one:

# ORE
#RESOURCE_TYPE = 1

# ORE and STONE
RESOURCE_TYPE = 2

# STONE
#RESOURCE_TYPE = 4

for minerToolStaticID in MINER_TOOLS_STATIC_IDS:
    tools = find_all_in_container_by_id(minerToolStaticID, containerSerial = Player.Backpack.Serial)
    for tool in tools:
        Misc.WaitForContext(tool.Serial, 10000)
        Misc.ContextReply(tool.Serial, RESOURCE_TYPE)
        
