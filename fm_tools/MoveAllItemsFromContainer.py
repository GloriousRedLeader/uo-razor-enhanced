# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-03-26
# Use at your own risk. 

# Moves all number of items from container 1 to container 2

from Scripts.fm_core.core_player import move_all_items_from_container


sourceSerial = Target.PromptTarget("Pick source container")
destinationSerial = Target.PromptTarget("Pick target container")

# have to do this or it wont find items
Items.UseItem(sourceSerial)
Misc.Pause(650)
Items.UseItem(destinationSerial)
Misc.Pause(650)
    
move_all_items_from_container(sourceSerial, destinationSerial)