# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-11-10
# Use at your own risk. 

from Scripts.fm_core.core_items import REAGENT_STATIC_IDS
from Scripts.fm_core.core_player import move_all_items_by_ids_to_container

# Moves reagents from one container to another. Prompts for containers.

move_all_items_by_ids_to_container(REAGENT_STATIC_IDS)