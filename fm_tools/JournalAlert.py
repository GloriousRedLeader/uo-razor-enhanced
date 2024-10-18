# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-03-26
# Use at your own risk. 

# This is a standalone script that will monitor exciting entries in the journal.
# If you're looking for a rare pet, just plug the name in here.
# If you're waiting for a boss to spawn during some event (e.g. SoTW on InsaneUO, 
# add the strings here.

# Configs
HOW_MANY_TIMES_TO_BEEP = 5
HOW_OFTEN_TO_PING_MS = 5000
STRINGS_TO_LOOK_FOR = [
    "The Master of the Hunt has",
    "You sense a dark presence",
    "a putrid steed",
    "a venom steed"
]

Timer.Create( 'journalAlertPingTimer', 1 )

Journal.Clear()
while True:
    
    if Timer.Check( 'journalAlertPingTimer' ) == False:
        Player.HeadMessage( 58, "Journal Alert Running...")
        Timer.Create( 'journalAlertPingTimer', HOW_OFTEN_TO_PING_MS )
    
    for search in STRINGS_TO_LOOK_FOR:
        if Journal.Search(search):
            found = Journal.GetLineText(search,False)
            Journal.Clear()
            for i in range(0, HOW_MANY_TIMES_TO_BEEP):
                Misc.Beep()
                Player.HeadMessage( 28, "^^ Journal Alert: {} ^^".format(found) )
                #Player.HeadMessage( 38, "^^ Journal Alert: {} ^^".format(found) )
                Player.HeadMessage( 48, "^^ Journal Alert: {} ^^".format(found) )
                Misc.Pause(1000) 

    Misc.Pause(1000)      