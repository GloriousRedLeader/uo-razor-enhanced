from Scripts.fm_core.core_gathering import chop_trees_in_area

# Makes a box around where player is standing and chops trees inside. The
# size of the box is determined by tileRange.
# You will need an axe equipped I believe.
chop_trees_in_area(
    # Makes a square tileRange * tileRange and will search for trees inside of it. So,
    # all you have to do is place yourself near a bunch of trees and hit the hotkey that
    # runs this function.
    tileRange = 10, 
    
    # If this limit is reached, the script just stops apparently.
    weightLimit = 350, 
    
    # Flag that will convert the logs into boards. I think you need an axe.
    cutLogsToBoards = False, 
    
    # After chopping wood, you can drop the wood on teh ground. Useful i you are just gaining skill.
    dropOnGround = False
)