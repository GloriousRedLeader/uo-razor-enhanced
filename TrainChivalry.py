Misc.SendMessage("Training Chiv")

while True:
    skillValue = Player.GetRealSkillValue("Chivalry")
    if skillValue < 90:
        Spells.CastChivalry("Holy Light")
    elif skillValue < 100:
        Spells.CastChivalry("Nobile Sacrifice")
    else:
        break
        
    Misc.Pause(5000)
    Player.HeadMessage(888, "Your skill is {}".format(skillValue))        

Misc.SendMessage("Done training")