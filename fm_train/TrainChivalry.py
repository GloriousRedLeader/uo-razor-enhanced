# GRL DID NOT WRITE THIS SCRIPT!
# Not written by me. Credit goes to wherever this came from. 
# Im hosting for safekeeping.

Misc.SendMessage("Training Chiv")

while Player.GetRealSkillValue("Chivalry") < 100:
    skillValue = Player.GetRealSkillValue("Chivalry")
    
    if skillValue < 90:
        Spells.CastChivalry("Holy Light")
    elif skillValue < 100:
        Spells.CastChivalry("Nobile Sacrifice")
    else:
        break
        
    Misc.Pause(2000)
    Player.HeadMessage(888, "Your skill is {}".format(skillValue))        

Misc.SendMessage("Done training")