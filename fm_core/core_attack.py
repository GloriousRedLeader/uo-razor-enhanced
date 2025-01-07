# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-03-26
# Use at your own risk. 

from Scripts.fm_core.core_mobiles import get_mobs_exclude_serials
from Scripts.fm_core.core_mobiles import get_friends_by_names
from Scripts.fm_core.core_mobiles import get_blues_in_range
from Scripts.fm_core.core_mobiles import get_mobile_percent_hp
from Scripts.fm_core.core_mobiles import get_pets
from Scripts.fm_core.core_player import find_instrument
from Scripts.fm_core.core_player import use_bag_of_sending
from Scripts.fm_core.core_spells import cast_until_works
from Scripts.fm_core.core_spells import cast_spell
from Scripts.fm_core.core_rails import is_player_moving
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

# 88 - blue     PET LOOP
# 78 - green    DEX LOOP
# 48 - organge  RAIL LOOP                  
# 253 - yellow  GPH
# 455 - white   PLAYER / ITEMS

def run_dex_loop(

    # Give it a fun name in case you have different versions, e.g.
    # DexLoop Single Targert, DexLoop AOE, etc.
    loopName = "DexLoop",

    # This is my special convention. It represents abilities that are toggled and
    # activated by next auto attack. These are what the possible values are:
    # 0 - Disabled, dont do anything
    # 1 - Use primary ability whatever it may be
    # 2 - Use secondary ability whatever it may be
    # 3 - Use lightning strike (bushido)
    # 4 - Use focus attack (ninjitsu)
    # 5 - Momentum strike (bushido)
    specialAbilityType = 0,

    # Time between special ability activations. Make smaller when youve got the mana to attack
    # more frequently. This is the default value. 
    specialAbilityDelayMs = 1000,
    
    # This causes insane damage when combined with weapon specials.
    # Buff lasts for only a few seconds but at least there is a buff.
    useShieldBash = 0,
    
    # The warrior mastery. Gives a resist debuff according to weapon type.
    # Looks like it lasts about 7 seconds at least in pvp. The debuff said
    # "-10% physical resist" when I used my physical damage sword.
    useOnslaught = 0,
    
    # May need to adjust. Cant tell if this is higher in pvm.
    onslaughtDelayMs = 8000,
    
    # Whether to use a bard ability.  When set this will search for
    # a random instrument in your pack and use that. No guarantees.
    # 0 = No ability
    # 1 = Discord the target
    # 2 = Peacemake self (aoe peacemake)
    bardAbility = 0,
    
    # The time in miliseconds to wait between discord attempts. Probably a more dynamic
    # way of doing this but I dont care. This is the default value. 
    bardDelayMs = 10000,

    # Flag that tells us to use the Chiv consecrate weapon ability. This is the default
    # value (0 = disabled, 1 = enabled)
    useConsecrateWeapon = 0,

    # Delay in miliseconds before recasting consecrate weapon. This is the default value.
    consecrateWeaponDelayMs = 10000,
    
    # Necro spell. Uses buff for recast tracking.
    useCurseWeapon = 0,

    # Flag with a value of 1 means to periodically cast divine fury, otherwise it is
    # disabled. This is the default value.
    useDivineFury = 0,

    # Time in miliseconds between activations of divine fury. This is the default value.
    divineFuryDelayMs = 10000,
    
    # Checks for the buff, if it doesnt exist, casts it.
    useEnemyOfOne = 0,
    
    # Whether to enable the Bushido skill Confidence. Typically lasts ~5 seconds
    # and lets us restore health and stamina maybe.
    #useConfidence = 0,
    # Whether to use a bushido skill. These are the mutually exclusive stances only.
    # 0 = No stance, do nothing
    # 1 = Confidence, restores stats when parry
    # 2 = Evasion, can parry magic, good
    # 3 = Counter Attack, more dps
    bushidoStance = 0,
    
    # Recast confidence after this many miliseconds
    #confidenceDelayMs = 5000,
    # Recast whatever stance above after this many miliseconds
    bushidoStanceDelayMs = 5000,

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
    
    # Whether we should use mirror images. This is a nice defnese move you can
    # use instealth to absorb a hit when you miss on a shadow strike
    useMirrorImage = 0,
    
    # Cast mirror images this often. They disappear something like every 30 - 60 seconds.
    mirrorImageDelayMs = 10000,   
    
    # Chiv spell
    useRemoveCurse = 0,
    
    # Paladin spell for curing poisons, only works on self.
    useCleanseByFire = 0,
   
    # how many tiles to look for enemies and attack them
    attackRange = 6,
    
    # If greater than 0 will attempt to use bag of sending when this much gold is present. Default is 0, no bag of sending usage.
    minGold = 0,
    
    # This will stop character from auto attacking if disabled.
    # Adding this while I level my vet skill so I dont kill things
    # too quickly.
    shouldAttack = True):

    # These are fairly static controls. Adjust as needed based on latency.

    journalEntryDelayMilliseconds = 200
    actionDelayMs = 1000
    #actionDelayMs = 250
    lastHonoredSerial = None
    onslaughtActive = False

    # Initial timer creation, not super important.

    Timer.Create( 'dexPingTimer', 1 )
    Timer.Create( 'dexSpecialAbilityDelayTimer', 1000 )
    Timer.Create( 'dexOnslaughtTimer', 1 )
    Timer.Create( 'dexBardTimer', 1 )
    Timer.Create( 'dexConsecrateWeaponTimer', 2000 )
    Timer.Create( 'dexDivineFuryTimer', 3000 )
    Timer.Create( 'dexBushidoStanceTimer', 1 )
    Timer.Create( 'petCommandTimer', 1500 )
    Timer.Create( 'dexMirrorImageTimer', 8000 )
    
    # Always enable on start
    Misc.SetSharedValue("core_loops_enabled", 1)
    
    while not Player.IsGhost:
        
        if Misc.ReadSharedValue("core_loops_enabled") != 1:
            Misc.Pause(500)
            if Timer.Check( 'dexPingTimer' ) == False:
                Player.HeadMessage( 78, "{} Paused...".format(loopName) )
                Timer.Create( 'dexPingTimer', 1000)
            continue
        
        if Timer.Check( 'dexPingTimer' ) == False:
            Player.HeadMessage( 78, "{} Running...".format(loopName) )
            Timer.Create( 'dexPingTimer', 3000 )
            
        if minGold > 0 and Player.Gold >= minGold:
            use_bag_of_sending(minGold)

        if not Player.Visible:
            Misc.Pause(500)
            continue

        heal_player_and_friends(useCleanseByFire = useCleanseByFire, useRemoveCurse = useRemoveCurse)
            
        eligible = get_mobs_exclude_serials(attackRange, namesToExclude = ["a horde minion"])
        if len(eligible) > 0:   
            nearest = Mobiles.Select(eligible, 'Nearest')
            if Mobiles.FindBySerial(nearest.Serial) is not None and Player.DistanceTo(nearest)<=10:            
                Target.SetLast(nearest)
            
                if useEnemyOfOne == 1 and not Player.BuffsExist("Enemy Of One"):
                    Spells.CastChivalry("Enemy Of One")
                    Misc.Pause(actionDelayMs)            
                elif useConsecrateWeapon == 1 and Timer.Check( 'dexConsecrateWeaponTimer' ) == False:
                    cast_until_works(lambda: Spells.CastChivalry("Consecrate Weapon"))
                    Timer.Create( 'dexConsecrateWeaponTimer', consecrateWeaponDelayMs )
                    Misc.Pause(actionDelayMs)
                elif useDivineFury == 1 and Timer.Check( 'dexDivineFuryTimer' ) == False:
                    cast_until_works(lambda: Spells.CastChivalry("Divine Fury"))
                    Timer.Create( 'dexDivineFuryTimer', divineFuryDelayMs )
                    Misc.Pause(actionDelayMs)
                elif useMirrorImage == 1 and Timer.Check( 'dexMirrorImageTimer' ) == False:
                    cast_until_works(lambda: Spells.CastNinjitsu("Mirror Image"))
                    Timer.Create( 'dexMirrorImageTimer', mirrorImageDelayMs )
                    Misc.Pause(actionDelayMs)
                elif useCurseWeapon == 1 and not Player.BuffsExist("Curse Weapon"):
                    cast_until_works(lambda: Spells.CastNecro("Curse Weapon"))
                    Misc.Pause(actionDelayMs)            
                    
                if bushidoStance == 1 and Timer.Check( 'dexBushidoStanceTimer' ) == False:
                    cast_until_works(lambda: Spells.CastBushido("Confidence", True))
                    Timer.Create( 'dexBushidoStanceTimer', bushidoStanceDelayMs )
                    Misc.Pause(actionDelayMs)
                elif bushidoStance == 2 and Timer.Check( 'dexBushidoStanceTimer' ) == False:
                    cast_until_works(lambda: Spells.CastBushido("Evasion", True))
                    Timer.Create( 'dexBushidoStanceTimer', bushidoStanceDelayMs )
                    Misc.Pause(actionDelayMs)
                elif bushidoStance == 3 and Timer.Check( 'dexBushidoStanceTimer' ) == False:
                    Timer.Create( 'dexBushidoStanceTimer', bushidoStanceDelayMs )
                    Spells.CastBushido("Counter Attack", True)
                    Misc.Pause(actionDelayMs)
                    
                if onslaughtActive == True:
                    if Journal.Search("You deliver an onslaught of sword strikes"):
                        onslaughtActive = False
                        
                # Weapon abilities, only one allowed at a time.
                if onslaughtActive == False and useOnslaught == 1 and Timer.Check( 'dexOnslaughtTimer' ) == False:
                    Journal.Clear()
                    Spells.CastMastery("Onslaught")
                    Misc.Pause(100)
                    if Journal.Search("You ready an onslaught"):
                        onslaughtActive = True
                        Timer.Create( 'dexOnslaughtTimer', onslaughtDelayMs )   
                        
                elif onslaughtActive == False and Timer.Check( 'dexSpecialAbilityDelayTimer' ) == False:
                
                    if useShieldBash == 1 and not Player.BuffsExist("Shield Bash") and Player.Mana > 22:
                        Spells.CastMastery("Shield Bash")
                        Misc.Pause(1000)
                        
                    if useShieldBash == 0 or (useShieldBash == 1 and Player.BuffsExist("Shield Bash")):
                    #if True:
                        if specialAbilityType == 1:
                            if not Player.HasPrimarySpecial:
                                Player.WeaponPrimarySA()
                        elif specialAbilityType == 2:
                            if not Player.HasSecondarySpecial:
                                Player.WeaponSecondarySA()
                        elif specialAbilityType == 3:
                            if not Player.BuffsExist("Lightning Strike"):
                                Spells.CastBushido("Lightning Strike", True)
                        elif specialAbilityType == 4:
                            print("This needs work, there is no buff for focus attack. TODO")
                            print(Player.BuffsExist("Focus Attack"))
                            if not Player.BuffsExist("Focus Attack"):
                                Spells.CastNinjitsu("Focus Attack", True)
                        elif specialAbilityType == 5:
                            print("This needs work, there is no buff for momentum strike. TODO")
                            if not Player.BuffsExist("Momentum Strike"):
                                Spells.CastBushido("Momentum Strike", True)
                        else:
                            pass
                            #Player.HeadMessage( 78, 'No weapon special selected' )
                        Timer.Create( 'dexSpecialAbilityDelayTimer', specialAbilityDelayMs )   
            
        #eligible = get_mobs_exclude_serials(attackRange, namesToExclude = ["a horde minion"])
        #if len(eligible) > 0:   
        #    nearest = Mobiles.Select(eligible, 'Nearest')
            #if Mobiles.FindBySerial(nearest.Serial) is not None and Player.DistanceTo(nearest)<=12:            
                #Target.SetLast(nearest)
                
                if useHonor == 1 and nearest.Serial != lastHonoredSerial:
                    Player.HeadMessage(78, "Honoring {}".format(nearest.Name))
                    Player.InvokeVirtue("Honor");
                    Target.WaitForTarget(3000, True);
                    Target.TargetExecute(nearest);
                    lastHonoredSerial = nearest.Serial
                
                if bardAbility == 1 and Timer.Check( 'dexBardTimer' ) == False:
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
                    Timer.Create( 'dexDiscordTimer', bardDelayMs )
                    Player.HeadMessage(78, "Discorded {}".format(nearest.Name))
                    
                elif bardAbility == 2 and Timer.Check( 'dexBardTimer' ) == False:
                    Player.UseSkill("Peacemaking")
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
                    #Target.Self()
                    Timer.Create( 'dexBardTimer', bardDelayMs )
                    Player.HeadMessage(78, "Peacemaking {}".format(nearest.Name))
                    
                if usePets == 1 and Timer.Check('petCommandTimer') == False:
                    if Player.DistanceTo(nearest)<=6:
                        Player.ChatSay("All Kill")
                        Target.WaitForTarget( 2000, True )
                        Target.TargetExecute( nearest )
                    else:
                        Player.ChatSay("All Follow Me")
                    Timer.Create( 'petCommandTimer', petCommandDelayMs )

                if shouldAttack == True:
                    #if useShieldBash == 1 and not Player.BuffsExist("Shield Bash") and Player.Mana > 22:
                    #    Spells.CastMastery("Shield Bash")
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
    
    # Whether the infected strike abiltiy is primary, second, or disabled (0)
    poisonAbility = 0,
    
    # Whether we should invoke the honor virtue before attacking something. I think
    # the target needs to be at full health for this to work. Maybe not all servers
    # are up to date with this. Default value is 0 which means dont honor target.
    # Useful for Bushido I think, who knows.
    # Refer to the dex_loop_use_honor shared variable.
    useHonor = 0,
    
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
    
    # Whether to use a bushido skill. These are the mutually exclusive stances only.
    # 0 = No stance, do nothing
    # 1 = Confidence, restores stats when parry
    # 2 = Evasion, can parry magic, good
    # 3 = Counter Attack, more dps
    # 4 = focus attack
    # 5 = momentum strike
    bushidoStance = 0,
    
    # Recast whatever stance above after this many miliseconds
    bushidoStanceDelayMs = 5000,    
    
    # Whether we should use mirror images. This is a nice defnese move you can
    # use instealth to absorb a hit when you miss on a shadow strike
    useMirrorImage = 0,
    
    # Cast mirror images this often. They disappear something like every 30 - 60 seconds.
    mirrorImageDelayMs = 10000):

    # These are fairly static controls. Adjust as needed based on latency.
    #journalEntryDelayMilliseconds = 200
    actionDelayMs = 650
    lastHonoredSerial = None
    lastPoisonedSerial = None

    # Initial timer creation, not super important.
    Timer.Create( 'dexPingTimer', 1 )
    Timer.Create( 'dexConsecrateWeaponTimer', 2000 )
    Timer.Create( 'dexDivineFuryTimer', 3000 )
    Timer.Create( 'dexMirrorImageTimer', 1 )
    Timer.Create( 'dexBushidoStanceTimer', 1 )
    
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
        
        if useConsecrateWeapon == 1 and Timer.Check( 'dexConsecrateWeaponTimer' ) == False:
            cast_until_works(lambda: Spells.CastChivalry("Consecrate Weapon"))
            Timer.Create( 'dexConsecrateWeaponTimer', consecrateWeaponDelayMs )
            Misc.Pause(actionDelayMs)
        elif useDivineFury == 1 and Timer.Check( 'dexDivineFuryTimer' ) == False:
            cast_until_works(lambda: Spells.CastChivalry("Divine Fury"))
            Timer.Create( 'dexDivineFuryTimer', divineFuryDelayMs )
            Misc.Pause(actionDelayMs)
        elif useMirrorImage == 1 and Timer.Check( 'dexMirrorImageTimer' ) == False and not Player.Visible:
            cast_until_works(lambda: Spells.CastNinjitsu("Mirror Image"))
            Timer.Create( 'dexMirrorImageTimer', mirrorImageDelayMs )
            Misc.Pause(actionDelayMs)
            
        if bushidoStance == 1 and Timer.Check( 'dexBushidoStanceTimer' ) == False:
            cast_until_works(lambda: Spells.CastBushido("Confidence", True))
            Timer.Create( 'dexBushidoStanceTimer', bushidoStanceDelayMs )
            Misc.Pause(actionDelayMs)
        elif bushidoStance == 2 and Timer.Check( 'dexBushidoStanceTimer' ) == False:
            cast_until_works(lambda: Spells.CastBushido("Evasion", True))
            Timer.Create( 'dexBushidoStanceTimer', bushidoStanceDelayMs )
            Misc.Pause(actionDelayMs)
        elif bushidoStance == 3 and Timer.Check( 'dexBushidoStanceTimer' ) == False:
            Timer.Create( 'dexBushidoStanceTimer', bushidoStanceDelayMs )
            Spells.CastBushido("Counter Attack", True)
            Misc.Pause(actionDelayMs)
            
        # Excluding player from targeting his mirror images (they disrupt this script)
        eligible = get_mobs_exclude_serials(6, namesToExclude = [Player.Name, "a reaper"])
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
                    
                # Either poison or SS strike, priority to poison
                if lastPoisonedSerial != nearest.Serial and poisonAbility != 0 and not nearest.Poisoned:
                    Player.HeadMessage(68, "Applying Poisin.")
                    if poisonAbility == 1 and not Player.HasPrimarySpecial:
                        Player.WeaponPrimarySA( )
                    elif poisonAbility == 2 and not Player.HasSecondarySpecial:
                        Player.WeaponSecondarySA()
                        
                    lastPoisonedSerial = nearest.Serial

                else:
                        
                    #if not Player.HasSecondarySpecial and Player.Mana >= ssManaCost:
                    if ssAbility == 1:
                        #if not Player.HasPrimarySpecial:
                        if not Player.HasSpecial:
                            Player.WeaponPrimarySA( )
                    elif ssAbility == 2:
                        #if not Player.HasSecondarySpecial:
                        if not Player.HasSpecial:
                            Player.WeaponSecondarySA( )

                #Misc.Pause(250)
                
                if Player.Visible:
                    Player.HeadMessage(68, "Visible, so attack")
                    Player.Attack(nearest)
                else:
                    if Player.HasSpecial:
                        #if Player.DistanceTo(nearest)<=1:
                        #    Spells.CastBushido("Confidence", 1)
                        Player.Attack(nearest)
                        Player.HeadMessage(68, "Hidden, yes special, yes attack")
                    else:
                        Player.HeadMessage(38, "Hidden, no special, no attack")
                        Target.Cancel()
            
        Misc.Pause(500)
        
# Necro / Poison / Chiv / Archer
def run_archery_loop (

    # activated by next auto attack. These are what the possible values are:
    # 0 - Disabled, dont do anything
    # 1 - Use primary ability whatever it may be
    # 2 - Use secondary ability whatever it may be
    # 3 - Flaming Shot (Archery Mastery)
    specialAbilityType = 0,
    
    # Time between special ability activations. Make smaller when youve got the mana to attack
    # more frequently. This is the default value. 
    specialAbilityDelayMs = 1000,
    
    # Whether the infected strike abiltiy is primary, second, or disabled (0)
    # Works only with elven composite longbow for serpent arrow
    poisonAbility = 0,
    
    # Whether we should invoke the honor virtue before attacking something. I think
    # the target needs to be at full health for this to work. Maybe not all servers
    # are up to date with this. Default value is 0 which means dont honor target.
    # Useful for Bushido I think, who knows.
    # Refer to the dex_loop_use_honor shared variable.
    useHonor = 0,
    
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
    #useConfidence = 0,
    # Whether to use a bushido skill. These are the mutually exclusive stances only.
    # 0 = No stance, do nothing
    # 1 = Confidence, restores stats when parry
    # 2 = Evasion, can parry magic, good
    # 3 = Counter Attack, more dps
    bushidoStance = 0,
    
    # Recast confidence after this many miliseconds
    #confidenceDelayMs = 5000,
    # Recast whatever stance above after this many miliseconds
    bushidoStanceDelayMs = 5000):

    # These are fairly static controls. Adjust as needed based on latency.
    #journalEntryDelayMilliseconds = 200
    actionDelayMs = 650
    lastHonoredSerial = None
    lastPoisonedSerial = None

    # Initial timer creation, not super important.
    Timer.Create( 'dexPingTimer', 1 )
    Timer.Create( 'dexConsecrateWeaponTimer', 2000 )
    Timer.Create( 'dexDivineFuryTimer', 3000 )
    Timer.Create( 'dexSpecialAbilityDelayTimer', 1000 )
    Timer.Create( 'dexBushidoStanceTimer', 4000 )
    
    # Always enable on start
    Misc.SetSharedValue("core_loops_enabled", 1)
    
    while not Player.IsGhost:
        
        if Misc.ReadSharedValue("core_loops_enabled") != 1:
            Misc.Pause(500)
            Player.HeadMessage( 48, 'Archery Loop Paused...' )
            Timer.Create( 'dexPingTimer', 2000 )
            continue
        
        if Timer.Check( 'dexPingTimer' ) == False:
            Player.HeadMessage( 78, 'Archery Loop Running...' )
            Timer.Create( 'dexPingTimer', 3000 )
        
        if useConsecrateWeapon == 1 and Timer.Check( 'dexConsecrateWeaponTimer' ) == False:
            cast_until_works(lambda: Spells.CastChivalry("Consecrate Weapon"))
            Timer.Create( 'dexConsecrateWeaponTimer', consecrateWeaponDelayMs )
            Misc.Pause(actionDelayMs)
        elif useDivineFury == 1 and Timer.Check( 'dexDivineFuryTimer' ) == False:
            cast_until_works(lambda: Spells.CastChivalry("Divine Fury"))
            Timer.Create( 'dexDivineFuryTimer', divineFuryDelayMs )
            Misc.Pause(actionDelayMs)
            
        if bushidoStance == 1 and Timer.Check( 'dexBushidoStanceTimer' ) == False:
            cast_until_works(lambda: Spells.CastBushido("Confidence", True))
            Timer.Create( 'dexBushidoStanceTimer', bushidoStanceDelayMs )
            Misc.Pause(actionDelayMs)
        elif bushidoStance == 2 and Timer.Check( 'dexBushidoStanceTimer' ) == False:
            cast_until_works(lambda: Spells.CastBushido("Evasion", True))
            Timer.Create( 'dexBushidoStanceTimer', bushidoStanceDelayMs )
            Misc.Pause(actionDelayMs)
        elif bushidoStance == 3 and Timer.Check( 'dexBushidoStanceTimer' ) == False:
            Timer.Create( 'dexBushidoStanceTimer', bushidoStanceDelayMs )
            Spells.CastBushido("Counter Attack", True)
            Misc.Pause(actionDelayMs)
     
        # Excluding player from targeting his mirror images (they disrupt this script)
        eligible = get_mobs_exclude_serials(10, namesToExclude = [Player.Name, "a reaper"])
        if len(eligible) > 0:   
            nearest = Mobiles.Select(eligible, 'Nearest')
            if Mobiles.FindBySerial(nearest.Serial) is not None and Player.DistanceTo(nearest)<= 10:            
            #while Mobiles.FindBySerial(nearest.Serial) is not None and Player.DistanceTo(nearest)<=6:                
                Target.SetLast(nearest)
                
                if useHonor == 1 and nearest.Serial != lastHonoredSerial:
                    Player.HeadMessage(307, "Honoring this fucker {}".format(nearest.Name))
                    Player.InvokeVirtue("Honor");
                    Target.WaitForTarget(3000, True);
                    Target.TargetExecute(nearest);
                    lastHonoredSerial = nearest.Serial
                    
                # Either poison or SS strike, priority to poison
                if lastPoisonedSerial != nearest.Serial and poisonAbility != 0 and not nearest.Poisoned:
                    Player.HeadMessage(68, "Applying Poisin.")
                    if poisonAbility == 1 and not Player.HasPrimarySpecial:
                        Player.WeaponPrimarySA( )
                    elif poisonAbility == 2 and not Player.HasSecondarySpecial:
                        Player.WeaponSecondarySA()
                    lastPoisonedSerial = nearest.Serial
                else:
                    if Timer.Check( 'dexSpecialAbilityDelayTimer' ) == False:
                        if specialAbilityType == 1:
                            #if not Player.HasPrimarySpecial:
                            if not Player.HasSpecial:
                                Player.WeaponPrimarySA( )
                        elif specialAbilityType == 2:
                            #if not Player.HasSecondarySpecial:
                            if not Player.HasSpecial:
                                Player.WeaponSecondarySA( )
                        Timer.Create( 'dexSpecialAbilityDelayTimer', specialAbilityDelayMs )  
                #Misc.Pause(250)
                Player.Attack(nearest)
                
            
        Misc.Pause(500)

        

# This is just some buffs that do not do any targetting.
# Targetting may cause interference with pet vet bandage loop.        
def run_buff_loop_only (
    # This is my special convention. It represents abilities that are toggled and
    # activated by next auto attack. These are what the possible values are:
    # 0 - Disabled, dont do anything
    # 1 - Use primary ability whatever it may be
    # 2 - Use secondary ability whatever it may be
    # 3 - Use lightning strike (bushido)
    # 4 - Use focus attack (ninjitsu)
    # 5 - Use momentum strike (Bushido)
    specialAbilityType = 0,

    # Time between special ability activations. Make smaller when youve got the mana to attack
    # more frequently. This is the default value. 
    specialAbilityDelayMs = 1000,
    
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
    #useConfidence = 0,
    # Whether to use a bushido skill. These are the mutually exclusive stances only.
    # 0 = No stance, do nothing
    # 1 = Confidence, restores stats when parry
    # 2 = Evasion, can parry magic, good
    # 3 = Counter Attack, more dps
    bushidoStance = 0,
    
    # Recast confidence after this many miliseconds
    #confidenceDelayMs = 5000,
    # Recast whatever stance above after this many miliseconds
    bushidoStanceDelayMs = 5000,
    
    # Periodically tell your pets to guard you. This will also tell your pets to follow
    # you when there are no bad guys around.
    usePets = 0,
    
    # Limits pet commands since it spams the world.
    petCommandDelayMs = 2500,
    
    # Whether we should use mirror images. This is a nice defnese move you can
    # use instealth to absorb a hit when you miss on a shadow strike
    useMirrorImage = 0,
    
    # Cast mirror images this often. They disappear something like every 30 - 60 seconds.
    mirrorImageDelayMs = 10000):

    # These are fairly static controls. Adjust as needed based on latency.

    journalEntryDelayMilliseconds = 200
    actionDelayMs = 650
    lastHonoredSerial = None

    # Initial timer creation, not super important.

    Timer.Create( 'dexPingTimer', 1 )
    Timer.Create( 'dexSpecialAbilityDelayTimer', 1000 )
    Timer.Create( 'dexConsecrateWeaponTimer', 2000 )
    Timer.Create( 'dexDivineFuryTimer', 3000 )
    Timer.Create( 'dexBushidoStanceTimer', 1 )
    Timer.Create( 'petCommandTimer', 1500 )
    Timer.Create( 'dexMirrorImageTimer', 8000 )
    
    # Always enable on start
    Misc.SetSharedValue("core_loops_enabled", 1)
    
    while not Player.IsGhost:
        
        if Misc.ReadSharedValue("core_loops_enabled") != 1:
            Misc.Pause(500)
            if Timer.Check( 'dexPingTimer' ) == False:
                Player.HeadMessage( 78, 'DexxerLoop Paused...' )
                Timer.Create( 'dexPingTimer', 1000)
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
        elif useDivineFury == 1 and Timer.Check( 'dexDivineFuryTimer' ) == False:
            cast_until_works(lambda: Spells.CastChivalry("Divine Fury"))
            Timer.Create( 'dexDivineFuryTimer', divineFuryDelayMs )
            Misc.Pause(actionDelayMs)
        elif useMirrorImage == 1 and Timer.Check( 'dexMirrorImageTimer' ) == False:
            cast_until_works(lambda: Spells.CastNinjitsu("Mirror Image"))
            Timer.Create( 'dexMirrorImageTimer', mirrorImageDelayMs )
            Misc.Pause(actionDelayMs)
            
        if bushidoStance == 1 and Timer.Check( 'dexBushidoStanceTimer' ) == False:
            cast_until_works(lambda: Spells.CastBushido("Confidence", True))
            Timer.Create( 'dexBushidoStanceTimer', bushidoStanceDelayMs )
            Misc.Pause(actionDelayMs)
        elif bushidoStance == 2 and Timer.Check( 'dexBushidoStanceTimer' ) == False:
            cast_until_works(lambda: Spells.CastBushido("Evasion", True))
            Timer.Create( 'dexBushidoStanceTimer', bushidoStanceDelayMs )
            Misc.Pause(actionDelayMs)
        elif bushidoStance == 3 and Timer.Check( 'dexBushidoStanceTimer' ) == False:
            Timer.Create( 'dexBushidoStanceTimer', bushidoStanceDelayMs )
            Spells.CastBushido("Counter Attack", True)
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
            elif specialAbilityType == 4:
                print("This needs work, there is no buff for focus attack. TODO")
                print(Player.BuffsExist("Focus Attack"))
                if not Player.BuffsExist("Focus Attack"):
                    Spells.CastNinjitsu("Focus Attack", True)
            elif specialAbilityType == 5:
                if not Player.BuffsExist("Momentum Strike"):
                    Spells.CastBushido("Momentum Strike", True)
            else:
                Player.HeadMessage( 78, 'No weapon special selected' )
            Timer.Create( 'dexSpecialAbilityDelayTimer', specialAbilityDelayMs )   
            
        #eligible = get_mobs_exclude_serials(6)
        eligible = get_mobs_exclude_serials(6, namesToExclude = [Player.Name, "a reaper"])
        if len(eligible) > 0:   
            nearest = Mobiles.Select(eligible, 'Nearest')
            if Mobiles.FindBySerial(nearest.Serial) is not None and Player.DistanceTo(nearest)<=12:            
                
                if usePets == 1 and Timer.Check('petCommandTimer') == False:
                    if Player.DistanceTo(nearest)<=6:
                        Player.ChatSay("All Guard Me")
                    else:
                        Player.ChatSay("All Follow Me")
                    Timer.Create( 'petCommandTimer', petCommandDelayMs )
                    
        else:
            if usePets == 1 and Timer.Check('petCommandTimer') == False:
                Player.ChatSay("All Follow Me")
                Timer.Create( 'petCommandTimer', petCommandDelayMs )                                

                #Player.Attack(nearest)
            
        Misc.Pause(500)
        
# Will cast AOE at player location and single target spells on closest mobs. Can also focus
# a specific mob if you want to focus on a boss.
# Set preferred delays in between each spell. Your main nukes should have no delay really.
def run_mage_loop2(

    # Give it a fun name in case you have different versions, e.g.
    # Mage AOE Loop or Mage Single Target Loop
    loopName = "Mage Loop",

    # How to pick your target for single target spells.
    # 0 = Nearest enemy. Default.
    # 1 = Prompt for target once at start of script. Useful for bosses.
    mobSelectMethod = 0,
    
    # 0 = Heal only names in friendNames, 1 = heal any blue in range
    friendSelectMethod = 0,
    
    # Names of pets or blue characters you want to heal, cure if they are in range.
    # Note that you still need to enable useCure / useGreaterHeal etc.
    friendNames = [],
    
    # Buffer in MS between attacks, otherwise we get "You have not yet recovered"
    actionDelayMs = 1000,
    
    # Only look for mobs and pets/friends inside of this range. IF they are farther, then
    # dont heal them / dont attack them.
    range = 8,
    
    # Use Arcane Empowerment (spell weaving) 0 = disabled, 1 = enabled
    useArcaneEmpowerment = 0,
    
    # Time in millesconds between casts of arcane empowerment.
    arcaneEmpowermentDelayMs = 35000,

    # Whether to use this spell 0 = disabled, 1 = enabled
    usePoisonStrike = 0,
    
    # Lower number like 10 means to spam repeatadly, number of MS in between usages
    poisonStrikeDelayMs = 10,
    
    # Whether to use this spell 0 = disabled, 1 = enabled
    useStrangle = 0,
    
    # Change to an appropriate value for strangle spell, number of MS in between usages
    strangleDelayMs = 60000,
    
    # Whether to use this spell 0 = disabled, 1 = enabled
    useCorpseSkin = 0,
    
    # Change to an appropriate value, number of MS in between usages
    corpseSkinDelayMs = 60000,
    
    # Whether to use this spell before applying each dot and curse 0 = disabled, 1 = enabled
    useEvilOmenBeforeDotsAndCurses = 0,
    
    # Whether to use the magery curse spell, 0 = disabled, 1 = enabled
    useCurse = 0,
    
    # How often to cast this spell in millesconds
    curseDelayMs = 60000,
    
    # Whether to use the magery spell poison, will only cast if poison is not on target 0 = disabled, 1 = enabled
    usePoison = 0,
    
    # How often we can cast poison in milliseconds
    poisonDelayMs = 30000,
    
    # Magery poison field spell 0 = disabled, 1 = enabled
    usePoisonField = 0,
    
    # How often to cast this spell in milliseconds
    poisonFieldDelayMs = 10000,
    
    # Toggles death ray. Requires magery mastery. There is no timer because this remains
    # active until you move or you are interrupted or the creature dies. It will attempt to
    # reapply immediately. 0 = disabled, 1 = enabled
    useDeathRay = 0,
    
    # Will use shadow word death on eligible targets until they die. This is more of a toggle.
    # 0 = disabled, 1 = enabled
    useWordOfDeath = 0,
    
    # Whether to use this spell 0 = disabled, 1 = enabled
    useWildfire = 0,
    
    # Lower number like 10 means to spam repeatadly, number of MS in between usages
    wildfireDelayMs = 10000,
    
    # Whether to use the thunderstorm spellweaving spell.
    useThunderstorm = 0,
    
    # Time in milliseconds before recasting
    thunderstormDelayMs = 10000,
    
    # Whether to use this spell 0 = disabled, 1 = enabled
    useWither = 0,
    
    # Change to an appropriate value for strangle spell, number of MS in between usages
    witherDelayMs = 5000,
    
    # Whether to cure yourself or your pet
    useCure = 0,
    
    # Whether to heal yourself or your pet
    useGreaterHeal = 0,
    
    # Necro heal
    useSpiritSpeak = 0,
    
    # Necro mastery for aoe damage, looks for buff. If no buff, casts it.
    useConduit = 0,
    
    # Only heal things that are below this percent HP
    healThreshold = 0.70    
):
    
    Timer.Create( 'magePingTimer', 1 )
    Timer.Create( 'arcaneEmpowermentTimer', 1 )
    Timer.Create( 'poisonStrikeTimer', 1000 )
    Timer.Create( 'strangleTimer', 1 )
    Timer.Create( 'corpseSkinTimer', 1 )
    Timer.Create( 'wildfireTimer', 1 )
    Timer.Create( 'witherTimer', 1 )
    Timer.Create( 'thunderstormTimer', 1 )
    Timer.Create( 'curseTimer', 1 )
    Timer.Create( 'poisonTimer', 1 )
    Timer.Create( 'poisonFieldTimer', 1 )

    Misc.SetSharedValue("core_loops_enabled", 1)
    
    if mobSelectMethod == 1:
        MSG = "Select an enemy to attack"
        Player.HeadMessage(118, MSG)
        mob = Mobiles.FindBySerial(Target.PromptTarget(MSG))
        
    Player.ChatSay("All Guard Me")
    
    while not Player.IsGhost:
        
        if Misc.ReadSharedValue("core_loops_enabled") != 1:
            Misc.Pause(500)
            if Timer.Check( 'magePingTimer' ) == False:
                Player.HeadMessage( 128, "{} Paused...".format(loopName) )
                Timer.Create( 'magePingTimer', 1000)
            continue
        
        if Timer.Check( 'magePingTimer' ) == False:
            Player.HeadMessage( 128, "{} Running...".format(loopName) )
            Timer.Create( 'magePingTimer', 3000 )

        if not Player.Visible:
            Misc.Pause(500)
            continue  

        if useArcaneEmpowerment == 1 and Timer.Check( 'arcaneEmpowermentTimer' ) == False and not Player.BuffsExist("Arcane Empowerment"):
            Spells.CastSpellweaving("Arcane Empowerment")    
            Misc.Pause(4000)    
            Timer.Create( 'arcaneEmpowermentTimer', arcaneEmpowermentDelayMs )
            continue
            
        # Continue loop before doing harmul actions, focus on healing/curing.
        heal_player_and_friends(friendSelectMethod = friendSelectMethod, friendNames = friendNames, range = range, actionDelayMs = actionDelayMs, healThreshold = healThreshold, useCure = useCure, useGreaterHeal = useGreaterHeal, useSpiritSpeak = useSpiritSpeak)
        
        
        numEligibleMobs = 0
        
        # Single target spells below. Need to find a target
        mobToAttack = None
        if mobSelectMethod == 1:
            mobToAttack = mob
        else:
            eligible = get_mobs_exclude_serials(range, checkLineOfSight = True, namesToExclude = [Player.Name])
            numEligibleMobs = len(eligible)
            if len(eligible) > 0:   
                nearest = Mobiles.Select(eligible, 'Nearest')
                if Mobiles.FindBySerial(nearest.Serial) is not None and Player.DistanceTo(nearest) <= range: 
                    mobToAttack = nearest
        
        if mobToAttack != None:
            
            # Buffs
            if useConduit == 1 and not Player.BuffsExist("Condit") and numEligibleMobs > 1:
                Spells.CastMastery("Conduit")
                Target.WaitForTarget(2000, False)
                Target.TargetExecute(mobToAttack)
                
            # Continue loop before doing harmul actions, focus on healing/curing.
            heal_player_and_friends(friendSelectMethod = friendSelectMethod, friendNames = friendNames, range = range, actionDelayMs = actionDelayMs, healThreshold = healThreshold, useCure = useCure, useGreaterHeal = useGreaterHeal, useSpiritSpeak = useSpiritSpeak)
            
            # Aoe
            if useWildfire == 1 and Timer.Check( 'wildfireTimer' ) == False:
                Spells.CastSpellweaving("Wildfire")
                Target.WaitForTarget(2000, False)
                Target.TargetExecute(Player.Position.X, Player.Position.Y, Player.Position.Z)
                Timer.Create( 'wildfireTimer', wildfireDelayMs )
                Misc.Pause(actionDelayMs)
            elif useThunderstorm == 1 and Timer.Check( 'thunderstormTimer' ) == False:
                Spells.CastSpellweaving("Thunderstorm")
                Timer.Create( 'thunderstormTimer', thunderstormDelayMs ) 
                Misc.Pause(actionDelayMs)      
            elif useWither == 1 and Timer.Check( 'witherTimer' ) == False:
                Spells.CastNecro("Wither")
                Timer.Create( 'witherTimer', witherDelayMs ) 
                Misc.Pause(actionDelayMs)  
            elif usePoisonField == 1 and Timer.Check( 'poisonFieldTimer' ) == False:
                Spells.CastMagery("Poison Field")
                Target.WaitForTarget(3000, False)
                Target.TargetExecute(mobToAttack)
                Timer.Create( 'poisonFieldTimer', poisonFieldDelayMs) 
                Misc.Pause(actionDelayMs)  
            
            # Continue loop before doing harmul actions, focus on healing/curing.
            #heal_player_and_friends(friendSelectMethod, friendNames, range, actionDelayMs, healThreshold, useCure, useGreaterHeal)
            heal_player_and_friends(friendSelectMethod = friendSelectMethod, friendNames = friendNames, range = range, actionDelayMs = actionDelayMs, healThreshold = healThreshold, useCure = useCure, useGreaterHeal = useGreaterHeal, useSpiritSpeak = useSpiritSpeak)
                
            # Curses (this is weird, but use word of death instead of curses if you can)
            if useWordOfDeath == 1 and mobToAttack is not None and mobToAttack.Hits is not None and mobToAttack.Hits > 0 and mobToAttack.HitsMax is not None and mobToAttack.HitsMax > 0 and mobToAttack.Hits / mobToAttack.HitsMax < 0.30:
                Spells.CastSpellweaving("Word of Death")
                Target.WaitForTarget(3500, False)
                Target.TargetExecute(mobToAttack)
                Misc.Pause(actionDelayMs) 
            elif useCorpseSkin == 1 and Timer.Check( 'corpseSkinTimer' ) == False:
                if useEvilOmenBeforeDotsAndCurses == 1:
                    Spells.CastNecro("Evil Omen")
                    Target.WaitForTarget(1500, False)
                    Target.TargetExecute(mobToAttack)
                    Misc.Pause(actionDelayMs)
                Spells.CastNecro("Corpse Skin")
                Target.WaitForTarget(1500, False)
                Target.TargetExecute(mobToAttack)
                Timer.Create( 'corpseSkinTimer', corpseSkinDelayMs )
                Misc.Pause(actionDelayMs)
            elif useStrangle == 1 and Timer.Check( 'strangleTimer' ) == False:
                if useEvilOmenBeforeDotsAndCurses == 1:
                    Spells.CastNecro("Evil Omen")
                    Target.WaitForTarget(1500, False)
                    Target.TargetExecute(mobToAttack)
                    Misc.Pause(actionDelayMs)
                Spells.CastNecro("Strangle")
                Target.WaitForTarget(3000, False)
                Target.TargetExecute(mobToAttack)
                Timer.Create( 'strangleTimer', strangleDelayMs ) 
                Misc.Pause(actionDelayMs)   
            elif usePoison == 1 and Timer.Check( 'poisonTimer' ) == False and not mobToAttack.Poisoned:
                if useEvilOmenBeforeDotsAndCurses == 1:
                    Spells.CastNecro("Evil Omen")
                    Target.WaitForTarget(1500, False)
                    Target.TargetExecute(mobToAttack)
                    Misc.Pause(actionDelayMs)
                Spells.CastMagery("Poison")
                Target.WaitForTarget(2000, False)
                Target.TargetExecute(mobToAttack)
                Timer.Create( 'poisonTimer', poisonDelayMs) 
                Misc.Pause(actionDelayMs)        
            elif useCurse == 1 and Timer.Check( 'curseTimer' ) == False:
                if useEvilOmenBeforeDotsAndCurses == 1:
                    Spells.CastNecro("Evil Omen")
                    Target.WaitForTarget(1500, False)
                    Target.TargetExecute(mobToAttack)
                    Misc.Pause(actionDelayMs)
                Spells.CastMagery("Curse")
                Target.WaitForTarget(2000, False)
                Target.TargetExecute(mobToAttack)
                Timer.Create( 'curseTimer', curseDelayMs) 
                Misc.Pause(actionDelayMs)       
                
            heal_player_and_friends(friendSelectMethod = friendSelectMethod, friendNames = friendNames, range = range, actionDelayMs = actionDelayMs, healThreshold = healThreshold, useCure = useCure, useGreaterHeal = useGreaterHeal, useSpiritSpeak = useSpiritSpeak)
                
            # Nukes    
            if useDeathRay == 1 and not Player.BuffsExist("Death Ray") and Player.BuffsExist("Arcane Empowerment"):
                Spells.CastMastery("Death Ray")
                Target.WaitForTarget(3500, False)
                Target.TargetExecute(mobToAttack)
                Misc.Pause(actionDelayMs)                
            elif useWordOfDeath == 1 and mobToAttack is not None and mobToAttack.Hits is not None and mobToAttack.Hits > 0 and mobToAttack.HitsMax is not None and mobToAttack.HitsMax > 0 and mobToAttack.Hits / mobToAttack.HitsMax < 0.30:
                Spells.CastSpellweaving("Word of Death")
                Target.WaitForTarget(3500, False)
                Target.TargetExecute(mobToAttack)
                Misc.Pause(actionDelayMs)
            elif usePoisonStrike == 1  and Timer.Check( 'poisonStrikeTimer' ) == False:
                Spells.CastNecro("Poison Strike")
                Target.WaitForTarget(3000, False)
                Target.TargetExecute(mobToAttack)
                Timer.Create( 'poisonStrikeTimer', poisonStrikeDelayMs )
                Misc.Pause(actionDelayMs)


# An internal function but it can be used as a main heal loop if desired.  
# casts cure on player and pet, also heals with greater heal
# if life is below threshold. Returns true if a heal / cure was attempted.
# This is so the calling function can decide whether to call this again before
# doing other stuff like continuing to attack.
def heal_player_and_friends2(

    # 0 = Heal only names in friendNames, 1 = heal any blue in range
    friendSelectMethod = 0,
    
    # Pets, friends, etc. These are names (string).
    friendNames = [],
    
    # If friends and pets are farther than this, dont bother with this.
    range = 8,

    # Buffer in MS between heal actions, otherwise we get "You have not yet recovered"
    actionDelayMs = 1000,

    # Only heal when pet/player life is below this threshold
    healThreshold = 0.7, 
    
    # Whether to cure yourself or your pet
    useCure = 0,
    
    # Whether to heal yourself or your pet (heals are mutually exclusive, only one will work, so just pick one)
    useGreaterHeal = 0,
    
    # Paladin spell for healing, only works on self. (heals are mutually exclusive, only one will work, so just pick one)
    useCloseWounds = 0,
    
    # Paladin spell for curing poisons, only works on self.
    useCleanseByFire = 0,
    
    # Chivalry spell
    useRemoveCurse = 0,
    
    # Necro heal (heals are mutually exclusive, only one will work, so just pick one)
    useSpiritSpeak = 0,
    
   
   # Provide name of player or pet to use gift of renewal.
   # This is a tricky one. Will attempt to 
   #giftOfRenwalTarget = None 
):
    didSomeHealing = False
    
    if useCure == 0 and useGreaterHeal == 0 and useCloseWounds == 0 and useCleanseByFire == 0 and useRemoveCurse == 0 and useSpiritSpeak == 0:
        return False

    while True:
        
        # Player is priority
        #while ((useCure == 1 or useCleanseByFire == 1) and Player.Poisoned) or ((useGreaterHeal == 1 or useCloseWounds == 1) and not Player.Poisoned and Player.Hits / Player.HitsMax < healThreshold and not Player.YellowHits):
        while (useCure == 1 and Player.Poisoned) or ((useGreaterHeal == 1 or useCloseWounds == 1 or useSpiritSpeak == 1) and not Player.Poisoned and Player.Hits / Player.HitsMax < healThreshold and not Player.YellowHits):
            if useCure == 1 and Player.Poisoned:
                Spells.CastMagery("Arch Cure")
                Target.WaitForTarget(3000, False)
                Target.Self()
                Misc.Pause(actionDelayMs)
#            if useCleanseByFire == 1 and Player.Poisoned:
#                Spells.CastChivalry("Cleanse by Fire")
#                Target.WaitForTarget(3000, False)
#                Target.Self()
#                Misc.Pause(actionDelayMs)                
            elif useGreaterHeal == 1 and not Player.Poisoned and Player.Hits / Player.HitsMax < healThreshold and not Player.YellowHits:
                Spells.CastMagery("Greater Heal")
                Target.WaitForTarget(3000, False)
                Target.Self()
                Misc.Pause(actionDelayMs)
            elif useCloseWounds == 1 and not Player.Poisoned and Player.Hits / Player.HitsMax < healThreshold and not Player.YellowHits:
                Spells.CastChivalry("Close Wounds")
                Target.WaitForTarget(3000, False)
                Target.Self()
                Misc.Pause(actionDelayMs)                
            elif useSpiritSpeak == 1 and not Player.Poisoned and Player.Hits / Player.HitsMax < healThreshold and not Player.YellowHits:
                Player.UseSkill("Spirit Speak")
                Misc.Pause(actionDelayMs)
            else:
                break

        if useCleanseByFire == 1 and Player.Poisoned:
            Spells.CastChivalry("Cleanse by Fire")
            Target.WaitForTarget(3000, False)
            Target.Self()
            Misc.Pause(actionDelayMs)
        elif useRemoveCurse == 1 and Player.BuffsExist("Curse"):
            Spells.CastChivalry("Remove Curse")
            Target.WaitForTarget(3000, False)
            Target.Self()
            Misc.Pause(actionDelayMs)
        
        # Now get one friend with lowest life
        if friendSelectMethod == 0: 
            friendMobiles = get_friends_by_names(friendNames, range)
        elif friendSelectMethod == 1:
            friendMobiles = get_blues_in_range(range)
            
        def sort_friends(x, y):
            if x is None or y is None:
                return False
            if x.HitsMax is None or x.HitsMax == 0 or y.HitsMax is None or y.HitsMax == 0:
                return False
            return x.Hits / x.HitsMax > y.Hits / y.HitsMax 
            
        if len(friendMobiles) > 0:
            friendMobiles.Sort(sort_friends)
            friendMobile = friendMobiles[0]
            #print("Blue Name {}".format(friendMobile.Name))
            
            if not (useCure == 1 and friendMobile.Poisoned) and not (useGreaterHeal == 1 and not friendMobile.Poisoned and friendMobile.HitsMax is not None and friendMobile.HitsMax > 0 and friendMobile.Hits / friendMobile.HitsMax < healThreshold and not friendMobile.YellowHits and friendMobile.Hits > 0):
                break
            
            if useCure == 1 and friendMobile.Poisoned:
                Spells.CastMagery("Arch Cure")
                Target.WaitForTarget(3000, False)
                Target.TargetExecute(friendMobile)
                Misc.Pause(actionDelayMs)        
            elif useGreaterHeal == 1 and not friendMobile.Poisoned and friendMobile.HitsMax is not None and friendMobile.HitsMax > 0 and friendMobile.Hits / friendMobile.HitsMax < healThreshold and not friendMobile.YellowHits and friendMobile.Hits > 0:
                Spells.CastMagery("Greater Heal")
                Target.WaitForTarget(3000, False)
                Target.TargetExecute(friendMobile)
                Misc.Pause(actionDelayMs) 
        else:
            break

    return False
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################

####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################    
    
    
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################


# Will cast AOE at player location and single target spells on closest mobs. Can also focus
# a specific mob if you want to focus on a boss.
# Set preferred delays in between each spell. Your main nukes should have no delay really.
def run_mage_loop(

    # Give it a fun name in case you have different versions, e.g.
    # Mage AOE Loop or Mage Single Target Loop
    loopName = "Mage Loop",
    
    # 0 = Heal only names in friendNames, 1 = heal any blue in range, 2 = my pets only
    friendSelectMethod = 0,
    
    # Names of pets or blue characters you want to heal, cure if they are in range.
    # Note that you still need to enable useCure / useGreaterHeal etc.
    friendNames = [],
    
    # Only look for mobs and pets/friends inside of this range. IF they are farther, then
    # dont heal them / dont attack them.
    range = 8,
    
    # Use Arcane Empowerment (spell weaving) 0 = disabled, 1 = enabled
    useArcaneEmpowerment = 0,

    # Whether to use this spell 0 = disabled, 1 = enabled
    usePoisonStrike = 0,
    
    # Lower number like 10 means to spam repeatadly, number of MS in between usages
    poisonStrikeDelayMs = 8000,
    
    # Whether to use this spell 0 = disabled, 1 = enabled
    useStrangle = 0,
    
    # Change to an appropriate value for strangle spell, number of MS in between usages
    strangleDelayMs = 60000,
    
    # Whether to use this spell 0 = disabled, 1 = enabled
    useCorpseSkin = 0,
    
    # Change to an appropriate value, number of MS in between usages
    corpseSkinDelayMs = 60000,
    
    # Whether to use this spell before applying each dot and curse 0 = disabled, 1 = enabled
    useEvilOmenBeforeDotsAndCurses = 0,
    
    # Whether to use the magery curse spell, 0 = disabled, 1 = enabled
    useCurse = 0,
    
    # How often to cast this spell in millesconds
    curseDelayMs = 60000,
    
    # Whether to use the magery spell poison, will only cast if poison is not on target 0 = disabled, 1 = enabled
    usePoison = 0,
    
    # How often we can cast poison in milliseconds
    poisonDelayMs = 30000,
    
    # Magery poison field spell 0 = disabled, 1 = enabled
    usePoisonField = 0,
    
    # How often to cast this spell in milliseconds
    poisonFieldDelayMs = 10000,
    
    # Toggles death ray. Requires magery mastery. There is no timer because this remains
    # active until you move or you are interrupted or the creature dies. It will attempt to
    # reapply immediately. 0 = disabled, 1 = enabled
    useDeathRay = 0,
    
    # Will use shadow word death on eligible targets until they die. This is more of a toggle.
    # 0 = disabled, 1 = enabled
    useWordOfDeath = 0,
    
    # Whether to use this spell 0 = disabled, 1 = enabled
    useWildfire = 0,
    
    # Lower number like 10 means to spam repeatadly, number of MS in between usages
    wildfireDelayMs = 9000,
    
    # Whether to use the thunderstorm spellweaving spell. There is no delay here. Just spam.
    useThunderstorm = 0,
    
    # Whether to use this spell 0 = disabled, 1 = enabled. There is no delay here. Just spam.
    useWither = 0,
    
    # Whether to cure yourself or your pet
    useCure = 0,
    
    # Whether to heal yourself or your pet
    useGreaterHeal = 0,
    
    # Necro heal
    useSpiritSpeak = 0,
    
    # Necro mastery for aoe damage, looks for buff. If no buff, casts it.
    useConduit = 0,
    
    # When standing still, no mobes in range, not bleeding, strangled, or poisoned, will start meditating.
    useMeditation = 0,
    
    # Only heal things that are below this percent HP
    healThreshold = 0.70    
):
    
    Timer.Create( 'magePingTimer', 1 )
    Timer.Create( 'poisonStrikeTimer', 1000 )
    Timer.Create( 'strangleTimer', 1 )
    Timer.Create( 'corpseSkinTimer', 1 )
    Timer.Create( 'wildfireTimer', 1 )
    Timer.Create( 'curseTimer', 1 )
    Timer.Create( 'poisonTimer', 1 )
    Timer.Create( 'poisonFieldTimer', 1 )
    Timer.Create( 'meditationTimer', 1 )

    Player.ChatSay("All Guard Me")
    
    while not Player.IsGhost:
        
        if Timer.Check( 'magePingTimer' ) == False:
            Player.HeadMessage( 128, "{} Running...".format(loopName) )
            Timer.Create( 'magePingTimer', 3000 )

        if not Player.Visible:
            Misc.Pause(500)
            continue  
            
        if is_player_moving() or Player.BuffsExist("Meditation"):
            Misc.Pause(250)
            continue

        # This is up top so we can buff up before heals.
        if useArcaneEmpowerment == 1 and not Player.BuffsExist("Arcane Empowerment") and Player.Mana > 90:
            cast_spell("Arcane Empowerment")
            
        # Continue loop before doing harmul actions, focus on healing/curing.
        if heal_player_and_friends(friendSelectMethod = friendSelectMethod, friendNames = friendNames, range = range, healThreshold = healThreshold, useCure = useCure, useGreaterHeal = useGreaterHeal, useSpiritSpeak = useSpiritSpeak) == True:
            continue
        
        eligible = get_mobs_exclude_serials(range, checkLineOfSight = True, namesToExclude = [Player.Name])
        if len(eligible) > 0:  
            nearestMob = Mobiles.Select(eligible, 'Nearest')
            nonPoisonedMob = next((mob for mob in eligible if not mob.Poisoned and get_mobile_percent_hp(mob) > 0.5), None)
            
            if useConduit == 1 and not Player.BuffsExist("Condit") and len(eligible) > 3 and Player.DistanceTo(nearestMob) > 4:
                cast_spell("Conduit", nearestMob)
            elif useDeathRay == 1 and not Player.BuffsExist("Death Ray") and Player.BuffsExist("Arcane Empowerment") and Player.Mana > 100:
                cast_spell("Death Ray", nearestMob)                                
            elif useWordOfDeath == 1 and get_mobile_percent_hp(nearestMob) < 0.3:
                cast_spell("Word of Death", nearestMob)                
            elif useCorpseSkin == 1 and Timer.Check( 'corpseSkinTimer' ) == False and get_mobile_percent_hp(nearestMob) > 0.5:
                if useEvilOmenBeforeDotsAndCurses == 1:
                    cast_spell("Evil Omen", nearestMob)
                cast_spell("Corpse Skin", nearestMob)
                Timer.Create( 'corpseSkinTimer', corpseSkinDelayMs )
            elif useStrangle == 1 and Timer.Check( 'strangleTimer' ) == False and get_mobile_percent_hp(nearestMob) > 0.5:
                if useEvilOmenBeforeDotsAndCurses == 1:
                    cast_spell("Evil Omen", nearestMob)
                cast_spell("Strangle", nearestMob)
                Timer.Create( 'strangleTimer', strangleDelayMs ) 
            elif usePoison == 1 and Timer.Check( 'poisonTimer' ) == False and nonPoisonedMob is not None:
                if useEvilOmenBeforeDotsAndCurses == 1:
                    cast_spell("Evil Omen", nonPoisonedMob)
                cast_spell("Poison", nonPoisonedMob)
                Timer.Create( 'poisonTimer', poisonDelayMs) 
            elif useCurse == 1 and Timer.Check( 'curseTimer' ) == False and get_mobile_percent_hp(nearestMob) > 0.75:
                if useEvilOmenBeforeDotsAndCurses == 1:
                    cast_spell("Evil Omen", nearestMob)
                cast_spell("Curse", nearestMob)
                Timer.Create( 'curseTimer', curseDelayMs) 
            elif useWildfire == 1 and Timer.Check( 'wildfireTimer' ) == False:
                cast_spell("Wildfire", nearestMob)
                Timer.Create( 'wildfireTimer', wildfireDelayMs )
            elif usePoisonField == 1 and Timer.Check( 'poisonFieldTimer' ) == False and nonPoisonedMob is not None:
                cast_spell("Poison Field", nonPoisonedMob)
                Timer.Create( 'poisonFieldTimer', poisonFieldDelayMs)                 
            elif usePoisonStrike == 1  and Timer.Check( 'poisonStrikeTimer' ) == False:
                cast_spell("Poison Strike", nearestMob)
                Timer.Create( 'poisonStrikeTimer', poisonStrikeDelayMs )                
            elif useThunderstorm == 1 and Player.DistanceTo(nearestMob) < 7 and Player.Mana > 30:
                cast_spell("Thunderstorm")
            elif useWither == 1 and Player.DistanceTo(nearestMob) < 4 and Player.Mana > 20:
                cast_spell("Wither")
        elif useMeditation == 1 and Player.Mana / Player.ManaMax < 0.83 and not Player.Poisoned and not Player.BuffsExist("Bleeding") and not Player.BuffsExist("Strangle") and Timer.Check( 'meditationTimer' ) == False:
            cast_spell("Meditation")
            Timer.Create( 'meditationTimer', 10000)                
                
        Misc.Pause(100)


# An internal function but it can be used as a main heal loop if desired.  
# casts cure on player and pet, also heals with greater heal
# if life is below threshold. Returns true if a heal / cure was attempted.
# This is so the calling function can decide whether to call this again before
# doing other stuff like continuing to attack.
# Returns True if something was healed so we can call it again. 
def heal_player_and_friends(

    # 0 = Heal only names in friendNames, 1 = heal any blue in range, 2 = my pets only
    friendSelectMethod = 0,
    
    # Pets, friends, etc. These are names (string).
    friendNames = [],
    
    # If friends and pets are farther than this, dont bother with this.
    range = 8,

    # Only heal when pet/player life is below this threshold
    healThreshold = 0.7, 
    
    # Whether to cure yourself or your pet
    useCure = 0,
    
    # Whether to heal yourself or your pet (heals are mutually exclusive, only one will work, so just pick one)
    useGreaterHeal = 0,
    
    # Paladin spell for healing, only works on self. (heals are mutually exclusive, only one will work, so just pick one)
    useCloseWounds = 0,
    
    # Paladin spell for curing poisons, only works on self.
    useCleanseByFire = 0,
    
    # Chivalry spell
    useRemoveCurse = 0,
    
    # Necro heal (heals are mutually exclusive, only one will work, so just pick one)
    useSpiritSpeak = 0,
):
    
    if useCure == 0 and useGreaterHeal == 0 and useCloseWounds == 0 and useCleanseByFire == 0 and useRemoveCurse == 0 and useSpiritSpeak == 0:
        return False

    if useCure == 1 and Player.Poisoned:
        cast_spell("Arch Cure", Player.Serial)
        return True
    elif useGreaterHeal == 1 and not Player.Poisoned and Player.Hits / Player.HitsMax < healThreshold and not Player.YellowHits:
        cast_spell("Greater Heal", Player.Serial)
        return True
    elif useCloseWounds == 1 and not Player.Poisoned and Player.Hits / Player.HitsMax < healThreshold and not Player.YellowHits:
        cast_spell("Close Wounds", Player.Serial)
        return True
    elif useSpiritSpeak == 1 and not Player.Poisoned and Player.Hits / Player.HitsMax < healThreshold and not Player.YellowHits:
        cast_spell("Spirit Speak")
        return True
    elif useCleanseByFire == 1 and Player.Poisoned:
        cast_spell("Cleanse by Fire")
        return False # Doing this on purpose, this isnt superimportant for melee.
    elif useRemoveCurse == 1 and Player.BuffsExist("Curse"):
        cast_spell("Remove Curse", Player.Serial)
        return False # Doing this on purpose, this isnt super important for melee.
        
    # Now lets heal our friends
    if friendSelectMethod == 0: 
        friendMobiles = get_friends_by_names(friendNames, range)
    elif friendSelectMethod == 1:
        friendMobiles = get_blues_in_range(range)
    elif friendSelectMethod == 2:
        friendMobiles = get_pets()
        
    def sort_friends(x, y):
        if x is None or y is None:
            return False
        if x.HitsMax is None or x.HitsMax == 0 or y.HitsMax is None or y.HitsMax == 0:
            return False
        return x.Hits / x.HitsMax > y.Hits / y.HitsMax 
        
    if len(friendMobiles) > 0:
        friendMobiles.Sort(sort_friends)
        friendMobile = friendMobiles[0]
        
        if not (useCure == 1 and friendMobile.Poisoned) and not (useGreaterHeal == 1 and not friendMobile.Poisoned and friendMobile.HitsMax is not None and friendMobile.HitsMax > 0 and friendMobile.Hits / friendMobile.HitsMax < healThreshold and not friendMobile.YellowHits and friendMobile.Hits > 0):
            return False
        
        if useCure == 1 and friendMobile.Poisoned:
            cast_spell("Arch Cure", friendMobile)
            return True
        elif useGreaterHeal == 1 and not friendMobile.Poisoned and friendMobile.HitsMax is not None and friendMobile.HitsMax > 0 and friendMobile.Hits / friendMobile.HitsMax < healThreshold and not friendMobile.YellowHits and friendMobile.Hits > 0:
            cast_spell("Greater Heal", friendMobile)
            return True

    return False