from Scripts.fm_core.core_gathering import run_fishing_loop

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