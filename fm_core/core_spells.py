# Make sure a spell gets cast
def cast_until_works(castFunc, delayBetweenAttemptsMs = 500, maxAttempts = -1):
    while maxAttempts != 0:
        Journal.Clear()
        castFunc()
        Misc.Pause(250)
        if (Journal.Search("You have not yet recovered") 
            or Journal.Search("You are already casting a spell") 
            or Journal.Search("This book needs time to recharge")
        ):
            Misc.SendMessage("Waiting to retry")
            Misc.Pause(delayBetweenAttemptsMs)
            maxAttempts = maxAttempts - 1
        else:
            break
