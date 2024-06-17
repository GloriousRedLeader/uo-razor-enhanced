Player.HeadMessage(38, "Training Animal Taming Using Mastery")


while not Player.IsGhost:
    Spells.CastMastery("Combat Training")
    Target.WaitForTarget(10000, False)
    Target.TargetExecute(0x000E9D3F)
    Misc.Pause(5000)
    
    

