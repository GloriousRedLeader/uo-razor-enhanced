# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-03-26
# Use at your own risk. 

# Make sure a spell gets cast
# DEPRECATED: Maybe dont use this. Ive got it baked into the recall
# function (fm_core.core_rails) which is the only place you really need it
# (maybe).
def cast_until_works(castFunc, delayBetweenAttemptsMs = 500, maxAttempts = -1):
    while maxAttempts != 0:
        Journal.Clear()
        castFunc()
        Misc.Pause(250)
        if (Journal.Search("You have not yet recovered") 
            or Journal.Search("You are already casting a spell") 
            or Journal.Search("This book needs time to recharge")
            or Journal.Search("That location is blocked")
        ):
            Misc.SendMessage("Waiting to retry")
            Misc.Pause(delayBetweenAttemptsMs)
            maxAttempts = maxAttempts - 1
        else:
            break
