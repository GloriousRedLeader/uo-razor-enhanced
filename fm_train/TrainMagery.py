# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-03-26
# Use at your own risk. 

# I am just storing this here for safekeeping. This script is from on UO Alive Discord
# Dec 18, 2023 Magery 0 - 120

CAST_TIMEOUT = 700

def SelfCast(spell, wait_for_target = True):
    Spells.CastMagery(spell)
    if wait_for_target:
        Target.WaitForTarget(10000, False)
        Target.Self()
    
def Meditate():
    if Player.Mana != Player.ManaMax:
        Player.UseSkill("Meditation")

    while Player.BuffsExist('Meditation') and Player.Mana != Player.ManaMax:
        Misc.Pause(1000)

while Player.GetSkillValue("Magery") < 120:
    if Player.Mana <= 23:
        Meditate()
    else:
        if Player.GetSkillValue("Magery") < 60:
            SelfCast("Mana Drain")
            Misc.Pause(CAST_TIMEOUT)
        elif Player.GetSkillValue("Magery") < 80:
            SelfCast("Reveal")
            Misc.Pause(CAST_TIMEOUT)
        elif Player.GetSkillValue("Magery") < 80:
            SelfCast("Mana Vampire")
            Misc.Pause(CAST_TIMEOUT)
        else:
            SelfCast("Earthquake", False)
            Misc.Pause(2500)
             