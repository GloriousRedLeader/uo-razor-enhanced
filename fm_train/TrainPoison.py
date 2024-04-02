# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-03-26
# Use at your own risk. 

# I am just storing this here for safekeeping. This script is from on UO Alive Discord
# Original Author may be Firebottle, posted on 3/17/2023



POISON_KEG_SERIAL = 0x40D6121B
MAX_LEVEL = 70

weapon = Player.GetItemOnLayer('RightHand')
while Player.GetSkillValue("Poisoning") < MAX_LEVEL:

    poison = Items.FindByID( 0x0F0A, -1, Player.Backpack.Serial )
    if poison == None:
        Player.HeadMessage(58, "No more poisons, making one")
        Items.UseItem(POISON_KEG_SERIAL)
        Misc.Pause(250)

    poison = Items.FindByID( 0x0F0A, -1, Player.Backpack.Serial )
    if poison == None:
        Player.HeadMessage(38, "No more poisons, quitting")
        break;
        
    while Player.Poisoned:
        Spells.CastMagery('Arch Cure')
        Target.WaitForTarget(5000,True)
        Target.Self()
        Misc.Pause(2000)
        Player.EquipItem(weapon)
        Misc.Pause(2000)

    while Player.Hits < Player.HitsMax:
        Spells.CastMagery('Greater Heal')
        Target.WaitForTarget(5000,True)
        Target.Self()
        Misc.Pause(2000)
        Player.EquipItem(weapon)
        Misc.Pause(2000)
        
    Misc.Pause(2000)

    Player.UseSkill("Poisoning")
    Misc.Pause(1000)
    Target.WaitForTarget(10000, False)

    if poison != None:
        Target.TargetExecute(poison)
    Target.WaitForTarget(10000, False)
    Target.TargetExecute(weapon)
    Misc.Pause(10000)
    

