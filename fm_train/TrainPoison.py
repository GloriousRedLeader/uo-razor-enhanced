# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-03-26
# Use at your own risk. 

# I am just storing this here for safekeeping. This script is from on UO Alive Discord
# Original Author may be Firebottle, posted on 3/17/2023


#0 - 30: Train at an NPC Thief Guildmaster
#30 - 40: Apply Lesser Poison
#40 - 70: Apply Poison
#70 - 92: Apply Greater Poison
#92 - 100: Apply Deadly Poison

POISON_KEG_SERIALS = [0x4023D4E5, 0x40D4A14A, 0x40D4A1A9]
MAX_LEVEL = 100

for kegSerial in POISON_KEG_SERIALS:
    
    weapon = Player.GetItemOnLayer('RightHand')
    while Player.GetSkillValue("Poisoning") < MAX_LEVEL:

        poison = Items.FindByID( 0x0F0A, -1, Player.Backpack.Serial )
        if poison == None:
            Player.HeadMessage(58, "No more poisons, making one")
            Items.UseItem(kegSerial)
            Misc.Pause(1000)

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
        Misc.Pause(8000)
        

