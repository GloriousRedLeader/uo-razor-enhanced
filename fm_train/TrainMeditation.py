# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-11-14
# Use at your own risk. 

while Player.GetSkillValue("Meditation") < Player.GetSkillCap('Meditation'):
    Spells.CastMagery("Earthquake")
    Misc.Pause(5000)
    Player.UseSkill("Meditation")
    Misc.Pause(3000)
#    while Player.BuffsExist('Meditation') and Player.Mana != Player.ManaMax:
#        Misc.Pause(1000)
    

