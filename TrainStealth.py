# MUST HAVE REQUIRED NINJA TO ATTEMPT SHADOWJUMP
# best to start in an area between north south trees with visible tiles between

while not Player.IsGhost:   
    #if Player.Visible:
    #    Spells.CastNinjitsu("Mirrorimage")
        
    if Player.Visible:
        Target.Cancel()        
        Player.UseSkill("Hiding")
        #Misc.Pause(8000)
        
#    elif not Player.Visible: 
#        Spells.CastNinjitsu("Shadowjump")
#        Target.WaitForTarget(3000, False)
#        Target.TargetExecuteRelative(Player.Serial,-1)
        
#        if Journal.Search('You must be in stealth'):
#            Player.HeadMessage(38,"OH YEAH")
#            Player.UseSkill("Stealth")
#            Misc.Pause(3000)        
 
    elif not Player.Visible:
        Player.UseSkill("Stealth")
        #Misc.Pause(3000)
        
#    if not Player.Visible:
#        Player.Walk("North")
#        Player.Walk("North")
#        Misc.Pause(3000)
  
#    if not Player.Visible:    
#        Player.Walk("South")
#        Player.Walk("South")
#        Player.Walk("South")
#        Misc.Pause(3000)
        
    Misc.Pause(8000)
    
    