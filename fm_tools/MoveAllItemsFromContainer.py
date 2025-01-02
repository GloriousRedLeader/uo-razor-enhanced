# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-03-26
# Use at your own risk. 

# Moves all number of items from container 1 to container 2

from Scripts.fm_core.core_player import move_all_items_from_container


sourceSerial = Target.PromptTarget("Pick source container")
destinationSerial = Target.PromptTarget("Pick target container")
    
move_all_items_from_container(sourceSerial, destinationSerial)