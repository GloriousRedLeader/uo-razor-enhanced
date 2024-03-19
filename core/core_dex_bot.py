from Scripts.core.core_mobiles import get_mobs_exclude_serials
from Scripts.core.core_player import find_instrument
from Scripts.core.core_spells import cast_until_works
import sys

# Good resources:
# https://github.com/dorana/RazorEnhancedScripts/blob/master/RazorScripts/SampMaster.cs
# https://github.com/hampgoodwin/razorenhancedscripts/tree/master
# https://github.com/ScriptB3ast/razor-enhanced/blob/master/items_useSkinningKnife.py
# https://github.com/matsamilla/Razor-Enhanced/blob/master/resource_LumberjackingScanTile.py
# https://github.com/YulesRules/Ultima-Online-Razor-Enhanced-Pathfinding/blob/main/PathfindingMain.py

def run_dex_bot(
    # Either 1 or 2 for primary or secondary, or set to 0 to disable weapon ablity
    # This is controlled by the shared variable: dex_loop_special_ability_type
    specialAbilityType = 0,

    # Time between special ability activations. Make smaller when youve got the mana to attack
    # more frequently. This is the default value. It is reccommended to override
    # with the shared variable: dex_loop_special_ability_delay_ms
    specialAbilityDelayMs = 1000,

    # Flag whether to discord target, 1 means yes, 0 means no, any other value is undefined.
    # What you see below is the default value. It is reccomended to set this value using
    # the shared variable: dex_loop_special_ability_type. When set this will search for
    # a random instrument in your pack and use that. No guarantees.
    useDiscord = 0,

    # The time in miliseconds to wait between discord attempts. Probably a more dynamic
    # way of doing this but I dont care. This is the default value. You can change it here
    # or better yet it is recommended to use the shared variable: dex_loop_discord_delay_ms
    discordDelayMs = 10000,

    # Flag that tells us to use the Chiv consecrate weapon ability. This is the default
    # value. It is recommended to use the shared value: dex_loop_use_consecrate_weapon
    useConsecrateWeapon = 0,

    # Delay in miliseconds before recasting consecrate weapon. This is the default value.
    # It is recommended to use the shared variable: dex_loop_consecrate_weapon_delay_ms
    consecrateWeaponDelayMs = 10000,

    # Flag with a value of 1 means to periodically cast divine fury, otherwise it is
    # disabled. This is the default value. Recommended to use the shared 
    # variable: dex_loop_use_divine_fury
    useDivineFury = 0,

    # Time in miliseconds between activations of divine fury. This is the default value.
    # It is recommended to use the shard variable: dex_loop_divine_fury_delay_ms
    divineFuryDelayMs = 10000,
    
    # Whether to enable the Bushido skill Confidence. Typically lasts ~5 seconds
    # and lets us restore health and stamina maybe.
    useConfidence = 0,
    
    # Recast confidence after this many miliseconds
    confidenceDelayMs = 5000,
    
    # Use the bushido lightning strike skill. Note that this is exclusive
    # with weapon special abilities so you cant have both. Single target damage.
    # This uses the specialAbilityDelayMs timer since those are the same.
    useLightningStrike = 0,

    # Whether we should invoke the honor virtue before attacking something. I think
    # the target needs to be at full health for this to work. Maybe not all servers
    # are up to date with this. Default value is 0 which means dont honor target.
    # Useful for Bushido I think, who knows.
    # Refer to the dex_loop_use_honor shared variable.
    useHonor = 0):

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
    
    while not Player.IsGhost:
        
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
            elif useLightningStrike == 1:
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

                Player.Attack(nearest)
            
        Misc.Pause(500)
