# Razor Enhanced Scripts for Ultima Online by
#	GRL  
#	https://github.com/GloriousRedLeader/uo-razor-enhanced
#	2024-03-26
# Use at your own risk. 

from Scripts.fm_core.core_mobiles import get_mobs_exclude_serials
from Scripts.fm_core.core_player import find_instrument
from Scripts.fm_core.core_spells import cast_until_works
import sys

# These are loops that will run on your character that find nearest enemies,
# attack them, use spells and abilities, etc. Pick the one that you like the best
# and use it. Most common ones are things that discord, consecrate weapon,
# attack nearest, etc. Theres a lot of options so be sure to enable what you need.

# Advanced configuration:
#
# All loop functions in this framework should honor a shared variable that 
# will pause the loops. Anything that loops should do this. They should respond to the
# change within 1000ms. You can pause all scripts by setting this vairable:
#
#   core_loops_enabled
#       (1) Enabled
#       (0) Disabled
#
# This will not stop the script, it will just sit in a loop and wait until the variable
# is once again set to 1. This is useful for teleporting and use with other scripts at the same time.
# You could also just manually stop / start your attack loop script. 
# But if youre playing different characters on different servers with different 
# script names, that becomes hard to track. So instead we can use this shared variable.

# Good resources:
# https://github.com/dorana/RazorEnhancedScripts/blob/master/RazorScripts/SampMaster.cs
# https://github.com/hampgoodwin/razorenhancedscripts/tree/master
# https://github.com/ScriptB3ast/razor-enhanced/blob/master/items_useSkinningKnife.py
# https://github.com/matsamilla/Razor-Enhanced/blob/master/resource_LumberjackingScanTile.py
# https://github.com/YulesRules/Ultima-Online-Razor-Enhanced-Pathfinding/blob/main/PathfindingMain.py

def run_dex_loop(
    # This is my special convention. It represents abilities that are toggled and
    # activated by next auto attack. These are what the possible values are:
    # 0 - Disabled, dont do anything
    # 1 - Use primary ability whatever it may be
    # 2 - Use secondary ability whatever it may be
    # 3 - Use lightning strike 
    specialAbilityType = 0,

    # Time between special ability activations. Make smaller when youve got the mana to attack
    # more frequently. This is the default value. 
    specialAbilityDelayMs = 1000,

    # Flag whether to discord target, 1 means yes, 0 means no, any other value is undefined.
    # What you see below is the default value. When set this will search for
    # a random instrument in your pack and use that. No guarantees.
    useDiscord = 0,

    # The time in miliseconds to wait between discord attempts. Probably a more dynamic
    # way of doing this but I dont care. This is the default value. 
    discordDelayMs = 10000,

    # Flag that tells us to use the Chiv consecrate weapon ability. This is the default
    # value (0 = disabled, 1 = enabled)
    useConsecrateWeapon = 0,

    # Delay in miliseconds before recasting consecrate weapon. This is the default value.
    consecrateWeaponDelayMs = 10000,

    # Flag with a value of 1 means to periodically cast divine fury, otherwise it is
    # disabled. This is the default value.
    useDivineFury = 0,

    # Time in miliseconds between activations of divine fury. This is the default value.
    divineFuryDelayMs = 10000,
    
    # Whether to enable the Bushido skill Confidence. Typically lasts ~5 seconds
    # and lets us restore health and stamina maybe.
    useConfidence = 0,
    
    # Recast confidence after this many miliseconds
    confidenceDelayMs = 5000,

    # Whether we should invoke the honor virtue before attacking something. I think
    # the target needs to be at full health for this to work. Maybe not all servers
    # are up to date with this. Default value is 0 which means dont honor target.
    # Useful for Bushido I think, who knows.
    # Refer to the dex_loop_use_honor shared variable.
    useHonor = 0,
    
    # Periodically tell your pets to guard you. This will also tell your pets to follow
    # you when there are no bad guys around.
    usePets = 0,
    
    # Limits pet commands since it spams the world.
    petCommandDelayMs = 5000,
    
    # This will stop character from auto attacking if disabled.
    # Adding this while I level my vet skill so I dont kill things
    # too quickly.
    shouldAttack = True):

    # These are fairly static controls. Adjust as needed based on latency.

    journalEntryDelayMilliseconds = 200
    actionDelayMs = 650
    lastHonoredSerial = None

    # Initial timer creation, not super important.

    Timer.Create( 'dexPingTimer', 1 )
    Timer.Create( 'dexSpecialAbilityDelayTimer', 1000 )
    Timer.Create( 'dexDiscordTimer', 5000 )
    Timer.Create( 'dexConsecrateWeaponTimer', 2000 )
    Timer.Create( 'dexDivineFuryTimer', 3000 )
    Timer.Create( 'dexConfidenceTimer', 6000 )
    Timer.Create( 'petCommandTimer', 1500 )
    
    # Always enable on start
    Misc.SetSharedValue("core_loops_enabled", 1)
    
    while not Player.IsGhost:
        
        if Misc.ReadSharedValue("core_loops_enabled") != 1:
            Misc.Pause(500)
            Player.HeadMessage( 48, 'DexxerLoop Paused...' )
            Timer.Create( 'dexPingTimer', 2000 )
            continue
        
        if Timer.Check( 'dexPingTimer' ) == False:
            Player.HeadMessage( 78, 'DexxerLoop Running...' )
            Timer.Create( 'dexPingTimer', 3000 )

        if not Player.Visible:
            Misc.Pause(500)
            continue
            
        if useConsecrateWeapon == 1 and Timer.Check( 'dexConsecrateWeaponTimer' ) == False:
            cast_until_works(lambda: Spells.CastChivalry("Consecrate Weapon"))
            Timer.Create( 'dexConsecrateWeaponTimer', consecrateWeaponDelayMs )
            Misc.Pause(actionDelayMs)
            
        if useDivineFury == 1 and Timer.Check( 'dexDivineFuryTimer' ) == False:
            cast_until_works(lambda: Spells.CastChivalry("Divine Fury"))
            Timer.Create( 'dexDivineFuryTimer', divineFuryDelayMs )
            Misc.Pause(actionDelayMs)
            
        if useConfidence == 1 and Timer.Check( 'dexConfidenceTimer' ) == False:
            cast_until_works(lambda: Spells.CastBushido("Confidence", True))
            Timer.Create( 'dexConfidenceTimer', confidenceDelayMs )
            Misc.Pause(actionDelayMs)
            
        if Timer.Check( 'dexSpecialAbilityDelayTimer' ) == False:
            if specialAbilityType == 1:
                if not Player.HasPrimarySpecial:
                    Player.WeaponPrimarySA()
            elif specialAbilityType == 2:
                if not Player.HasSecondarySpecial:
                    Player.WeaponSecondarySA()
            elif specialAbilityType == 3:
                if not Player.BuffsExist("Lightning Strike"):
                    Spells.CastBushido("Lightning Strike", True)
            else:
                Player.HeadMessage( 78, 'No weapon special selected' )
            Timer.Create( 'dexSpecialAbilityDelayTimer', specialAbilityDelayMs )   
            
        eligible = get_mobs_exclude_serials(6)
        if len(eligible) > 0:   
            nearest = Mobiles.Select(eligible, 'Nearest')
            if Mobiles.FindBySerial(nearest.Serial) is not None and Player.DistanceTo(nearest)<=12:            
                Target.SetLast(nearest)
                
                if useHonor == 1 and nearest.Serial != lastHonoredSerial:
                    Player.HeadMessage(307, "Honoring this fucker {}".format(nearest.Name))
                    Player.InvokeVirtue("Honor");
                    Target.WaitForTarget(3000, True);
                    Target.TargetExecute(nearest);
                    lastHonoredSerial = nearest.Serial
                
                if useDiscord == 1 and Timer.Check( 'dexDiscordTimer' ) == False:
                    Player.UseSkill("Discordance")
                    Misc.Pause(journalEntryDelayMilliseconds) 
                    if Journal.SearchByType( 'What instrument shall you play?', 'System' ):
                        instrument = find_instrument( Player.Backpack )
                        if instrument == None:
                            Misc.SendMessage( 'No instrument to discord with!', 38 )
                            sys.exit()
                        Target.WaitForTarget( 2000, True )
                        Target.TargetExecute( instrument )
                
                    Target.WaitForTarget( 2000, True )
                    Target.TargetExecute( nearest )
                    Timer.Create( 'dexDiscordTimer', discordDelayMs )
                    Player.HeadMessage(78, "Discorded {}".format(nearest.Name))
                    
                if usePets == 1 and Timer.Check('petCommandTimer') == False:
                    if Player.DistanceTo(nearest)<=6:
                        Player.ChatSay("All Kill")
                        Target.WaitForTarget( 2000, True )
                        Target.TargetExecute( nearest )
                    else:
                        Player.ChatSay("All Follow Me")
                    Timer.Create( 'petCommandTimer', petCommandDelayMs )

                if shouldAttack == True:
                    Player.Attack(nearest)
        else:
            if usePets == 1 and Timer.Check('petCommandTimer') == False:
                Player.ChatSay("All Follow Me")
                Timer.Create( 'petCommandTimer', petCommandDelayMs )                                

                #Player.Attack(nearest)
            
        Misc.Pause(500)
        
# Use this if you want to shadowstrike things all day
# Probably a good idea to be in wraith form
def run_ss_loop (

    # This isnt TOO important, just helps prevent spamming messages like 
    # You need at least x mana to do this. Meh. User should be able to figure
    # this out. I certainly do not know how to get the cost of a weapon special
    # dynamically. looking for a function like CanCast(ability)
    #ssManaCost = 10,

    # Whether shadowstrike on your weapon is primary (1) or secondary (2)
    # Setting this to 0 to disable makes no sense
    ssAbility = 1,
    
    # Whether we should invoke the honor virtue before attacking something. I think
    # the target needs to be at full health for this to work. Maybe not all servers
    # are up to date with this. Default value is 0 which means dont honor target.
    # Useful for Bushido I think, who knows.
    # Refer to the dex_loop_use_honor shared variable.
    useHonor = 0):

    # These are fairly static controls. Adjust as needed based on latency.
    #journalEntryDelayMilliseconds = 200
    #actionDelayMs = 650
    lastHonoredSerial = None

    # Initial timer creation, not super important.
    Timer.Create( 'dexPingTimer', 1 )
    
    # Always enable on start
    Misc.SetSharedValue("core_loops_enabled", 1)
    
    while not Player.IsGhost:
        
        if Misc.ReadSharedValue("core_loops_enabled") != 1:
            Misc.Pause(500)
            Player.HeadMessage( 48, 'SS Loop Paused...' )
            Timer.Create( 'dexPingTimer', 2000 )
            continue
        
        if Timer.Check( 'dexPingTimer' ) == False:
            Player.HeadMessage( 78, 'SS Loop Running...' )
            Timer.Create( 'dexPingTimer', 3000 )
            
        eligible = get_mobs_exclude_serials(6)
        if len(eligible) > 0:   
            nearest = Mobiles.Select(eligible, 'Nearest')
            if Mobiles.FindBySerial(nearest.Serial) is not None and Player.DistanceTo(nearest)<=6:            
            #while Mobiles.FindBySerial(nearest.Serial) is not None and Player.DistanceTo(nearest)<=6:                
                Target.SetLast(nearest)
                
                if useHonor == 1 and nearest.Serial != lastHonoredSerial:
                    Player.HeadMessage(307, "Honoring this fucker {}".format(nearest.Name))
                    Player.InvokeVirtue("Honor");
                    Target.WaitForTarget(3000, True);
                    Target.TargetExecute(nearest);
                    lastHonoredSerial = nearest.Serial
                    
                #if not Player.HasSecondarySpecial and Player.Mana >= ssManaCost:
                if ssAbility == 1:
                    if not Player.HasPrimarySpecial:
                        Player.WeaponPrimarySA( )
                elif ssAbility == 2:
                    if not Player.HasSecondarySpecial:
                        Player.WeaponSecondarySA( )

                Misc.Pause(250)
                
                if Player.Visible:
                    Player.HeadMessage(68, "Visible, so attack")
                    Player.Attack(nearest)
                else:
                    if Player.HasSpecial:
                        Player.Attack(nearest)
                        Player.HeadMessage(68, "Hidden, yes special, yes attack")
                    else:
                        Player.HeadMessage(38, "Hidden, no special, no attack")
        
            
        Misc.Pause(500)
