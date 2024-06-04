import sys
print("Training Ninjitsu")

while True:
    if not Player.Visible:
        Player.Walk("North")
        Player.Walk("North")
        Player.Walk("East")
        Player.Walk("East")
        Player.Walk("East")
        Player.Walk("South")
        Player.Walk("South")
        Player.Walk("West")
        Player.Walk("West")
        Player.Walk("West")
        
    Misc.Pause(400)
    
sys.exit()

# At 50 do this
#while not Player.IsGhost:  
MAX_LEVEL = 85
while Player.GetSkillValue("Ninjitsu") < MAX_LEVEL: 
    if Player.Visible:
        Target.Cancel()        
        Player.UseSkill("Hiding")
        Misc.Pause(3000)
        
    elif not Player.Visible: 
        Spells.CastNinjitsu("Shadowjump")
        Target.WaitForTarget(3000, False)
        #Target.TargetExecuteRelative(Player.Serial,-1)
        Target.TargetExecuteRelative(Player.Serial,1)
        
    if not Player.Visible:
        Player.Walk("North")
        Player.Walk("North")
  
    if not Player.Visible:    
        Player.Walk("South")
        Player.Walk("South")
        
    Misc.Pause(400)

sys.exit()


# at 40 do this

while not Player.IsGhost:  
    Spells.CastNinjitsu("Mirror Image")
    Misc.Pause(5000)

sys.exit()

