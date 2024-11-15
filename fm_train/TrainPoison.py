# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-11-14
# Use at your own risk. 

# I am just storing this here for safekeeping. This script is from on UO Alive Discord
# Original Author may be Firebottle, posted on 3/17/2023

# Set the MAX_LEVEL value based on the poison you are training. See below.
# Put kegs in your backpack.
# Put one empty bottle in your backpack.
# Equip a dagger or fencing weapon that can be poisoned.

#0 - 30: Train at an NPC Thief Guildmaster
#30 - 40: Apply Lesser Poison
#40 - 70: Apply Poison
#70 - 92: Apply Greater Poison
#92 - 100: Apply Deadly Poison

from Scripts.fm_core.core_player import find_all_in_container_by_id
from Scripts.fm_core.core_player import find_all_in_container_by_ids
from Scripts.fm_core.core_items import KEG_STATIC_IDS
from Scripts.fm_core.core_items import POISON_POTION_STATIC_ID


#POISON_KEG_SERIALS = [0x407FC64D]
MAX_LEVEL = 100

#def find_all_in_container_by_id(itemID, containerSerial = Player.Backpack.Serial):
#kegs = find_all_in_container_by_id()
kegs = find_all_in_container_by_ids(KEG_STATIC_IDS, containerSerial = Player.Backpack.Serial)
for keg in kegs:
    print(keg)
    
#for kegSerial in POISON_KEG_SERIALS:
weapon = Player.GetItemOnLayer('RightHand')
while Player.GetSkillValue("Poisoning") < MAX_LEVEL:
    for keg in kegs:
        poison = Items.FindByID( POISON_POTION_STATIC_ID, -1, Player.Backpack.Serial )
        if poison == None:
            Player.HeadMessage(58, "No more poisons, making one")
            #Items.UseItem(kegSerial)
            Items.UseItem(keg)
            Misc.Pause(1000)
#0x0F0E - empty
# 0x0F0A - poison
        poison = Items.FindByID( POISON_POTION_STATIC_ID, -1, Player.Backpack.Serial )
        if poison == None:
            Player.HeadMessage(38, "No more poisons, quitting")
            break;
            
        while Player.Poisoned:
            Spells.CastMagery('Arch Cure')
            Target.WaitForTarget(5000,True)
            Target.Self()
            Misc.Pause(1000)
            Player.EquipItem(weapon)
            Misc.Pause(1000)

        while Player.Hits < Player.HitsMax:
            Spells.CastMagery('Greater Heal')
            Target.WaitForTarget(5000,True)
            Target.Self()
            Misc.Pause(1000)
            Player.EquipItem(weapon)
            Misc.Pause(1000)
            
        #Misc.Pause(2000)

        if poison != None:
            Misc.Pause(1000)
            Player.UseSkill("Poisoning")
            Misc.Pause(1000)
            Target.WaitForTarget(10000, False)
            Target.TargetExecute(poison)
            Target.WaitForTarget(10000, False)
            Target.TargetExecute(weapon)
            Misc.Pause(8000)
        

