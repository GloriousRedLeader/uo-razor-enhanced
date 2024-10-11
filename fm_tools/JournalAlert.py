HOW_MANY_TIMES_TO_BEEP = 5

Player.HeadMessage(58, "SoTW boss scanner is running!")
# Real string in game: The Master of the Hunt has arrived to the South-East...

strings = [
    "The Master of the Hunt has",
    "You sense a dark presence",
    "a putrid steed",
    "a venom steed"
]

Journal.Clear()
while True:
    Misc.Pause(1000)
    for search in strings:
        #if Journal.Search("The Master of the Hunt has") or Journal.Search("You sense a dark presence"):
        if Journal.Search(search):
            Journal.Clear()
            for i in range(0, HOW_MANY_TIMES_TO_BEEP):
                Misc.Beep()
                Player.HeadMessage( 28, '^^ Boss has spawned (somewhere) ^^' )
                Player.HeadMessage( 38, '^^ Boss has spawned (somewhere) ^^' )
                Player.HeadMessage( 48, '^^ Boss has spawned (somewhere) ^^' )
                Misc.Pause(1000) 
