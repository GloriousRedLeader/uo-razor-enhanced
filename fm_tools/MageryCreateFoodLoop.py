
from Scripts.fm_core.core_player import open_bank_and_resupply
from Scripts.fm_core.core_player import move_all_items_from_container
from Scripts.fm_core.core_rails import go_to_tile
from Scripts.fm_core.core_items import AXE_STATIC_IDS, LOG_STATIC_IDS, TREE_STATIC_IDS
from Scripts.fm_core.core_player import find_in_container_by_id
from Scripts.fm_core.core_player import open_bank_and_deposit_items
from System.Collections.Generic import List
import sys
import time

Player.HeadMessage(455, "start")

AMOUNT_TO_MAKE = 100

for i in range(0, 100):
    Spells.CastMagery("Create Food")    
    Misc.Pause(3000)