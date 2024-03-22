from System.Collections.Generic import List
from System import Byte
from Scripts.core.core_mobiles import get_mobs_exclude_serials

# This is a standalone script that will attack the closest gray creature with your weapon
# That is all.

eligible = get_mobs_exclude_serials(6)

if len(eligible) > 0:
    nearest = Mobiles.Select(eligible,'Nearest')
    #while Mobiles.FindBySerial(nearest.Serial) is not None and Player.DistanceTo(nearest)<=6:
    if Mobiles.FindBySerial(nearest.Serial) is not None and Player.DistanceTo(nearest)<=6:
        Misc.SendMessage(nearest)
        nearby_enemies_len = len(monster_list(1))
        #Spells.CastMastery("Shadow Strike")
        #Player.WeaponPrimarySA( )
        
#        rightHand = Player.GetItemOnLayer('RightHand')
#        if rightHand and rightHand.Serial == 0x401D95C5:
#            Player.HeadMessage(66, 'Already got the dagger Set')
#        else:
#            Player.HeadMessage(66, 'Need to find dagger')
#            wep = Items.FindBySerial( 0x401D95C5 )
#            if wep:
#                 Player.HeadMessage(66, 'Equipping Weapon')
#                 Player.EquipItem(wep) 
#            else:
#                Player.HeadMessage(66, 'NO dagger in inventory')
            
        
#        if not Player.Visible:
            #Spells.CastNinjitsu("Backstab")
#            Player.WeaponSecondarySA( )
#        elif Player.Visible:
#            Player.WeaponSecondarySA( )
        #Spells.CastChivalry("Consecrate Weapon")
        #Misc.Pause(1000)
        #Player.UseSkill("Discordance")
        #Target.WaitForTarget(10000, False)
        #Target.TargetExecute(nearest)
        #Misc.Pause(1000)
        Player.Attack(nearest)
#        Misc.Pause(250)
        #Misc.Pause(1)

#Misc.Pause(800)

