def Meditate():
    if Player.Mana != Player.ManaMax:
        Player.UseSkill("Meditation")

    #print("Pausing while we meditate")
    #Misc.Pause(10000)
    while Player.BuffsExist('Meditation') and Player.Mana != Player.ManaMax:
        Misc.Pause(1000)
        
while True:
    
    if Player.Mana <= 35:
        Meditate()
    else:    
        
        Spellweaving = Player.GetSkillValue('Spell Weaving')
        if Spellweaving < 20 and Player.Mana > 20:
            Spells.CastSpellweaving('Arcane Circle')
            #Spells.CastSpellweaving('Gift of Renewal')
            #Target.WaitForTarget(4000, False)
            #Target.Self()
            Misc.Pause(2000)
            
        if Spellweaving >= 20 and Spellweaving < 36 and Player.Mana > 20:
            Spells.CastSpellweaving('Immolating Weapon')
            Misc.Pause(2200)   
       
        if Spellweaving >= 36 and Spellweaving < 58  and Player.Mana > 35:
            Spells.CastSpellweaving('Reaper Form')
            Misc.Pause(4000)  
           
        if Spellweaving >= 58 and Spellweaving < 74  and Player.Mana > 35:
            Spells.CastSpellweaving('Essence Of Wind')
            Misc.Pause(5000)

        if Spellweaving >= 74 and Spellweaving < 92  and Player.Mana > 35:
            Spells.CastSpellweaving('Wildfire')
            Target.WaitForTarget(4000,False)
            Target.Self()
            Misc.Pause(5000) 

        if Spellweaving >= 92 and Spellweaving != Player.GetSkillCap('Spell Weaving') and Player.Mana > 35:
            if Player.Hits < 50:
                Spells.CastSpellweaving('Gift Of Renewal')
                Target.WaitForTarget(4000,False)
                Target.Self()
                Misc.Pause(2000)
            else:
                Spells.CastSpellweaving('Word Of Death')
                Target.WaitForTarget(4000,False)
                Target.Self()
            Misc.Pause(2000)            
       
        if Spellweaving == Player.GetSkillCap('Spell Weaving'):
            Misc.ScriptStopAll()
            
        Misc.Pause(500)