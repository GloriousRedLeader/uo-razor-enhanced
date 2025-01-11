# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-03-26
# Use at your own risk. 

from Scripts.fm_core.core_gathering import run_fishing_loop

# Auto fishes in all the lands. Works on a boat. Works on a dock.
# If you are on a boat, you can use the moveTiles param to move boat after each fishing attempt.
# It will say forward one X number of times.
# Can automatically cut fish. Can automatically store fish in hold.
run_fishing_loop(
    # How many tiles in front of character to fish
    fishRange = 4, 
    
    # If on a boat, tells the tiller to move forward this many times.
    moveTiles = 2, 
    
    # How long to pause between casts
    fishDelayMs = 10000,
    
    # 0 = Do nothing, leave in backpack
    # 1 = cut fish with dagger to reduce weight, makes lots of fish steaks
    # 2 = place fish in cargo hold of ship, have to be standing near cargo hold
    fishHandling = 0,
    
    # Will not do any fishHandling operations on this fish. Leaves it in backpack. Useful for fishing quests.
    fishToKeep = None
)