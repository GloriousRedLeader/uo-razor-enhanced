# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-03-26
# Use at your own risk. 

from Scripts.fm_core.core_mobiles import get_enemies
from Scripts.fm_core.core_player import open_bank_and_resupply
from Scripts.fm_core.core_player import move_all_items_from_container
from Scripts.fm_core.core_items import AXE_STATIC_IDS, LOG_STATIC_IDS, TREE_STATIC_IDS
from Scripts.fm_core.core_player import find_in_container_by_id
from Scripts.fm_core.core_player import open_bank_and_deposit_items
from Scripts.fm_core.core_player import move_item_to_container
from System.Collections.Generic import List
import sys
from System import Byte, Int32
import time

# PIcks up nearby items. Will prompt you for a container to put them in

Player.HeadMessage(455, "Pick up nearby items and put in container")

destinationSerial = Target.PromptTarget("Pick destination container", 38)

filter = Items.Filter()
filter.Graphics = List[Int32]((0x1BF2))
filter.Movable = 1
filter.OnGround = 1
filter.RangeMax = 2
items = Items.ApplyFilter(filter)

for item in items:
    print("Moving item", item.Name)
    move_item_to_container(item, destinationSerial)

