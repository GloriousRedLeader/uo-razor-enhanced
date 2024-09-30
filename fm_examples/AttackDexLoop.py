# Razor Enhanced Scripts for Ultima Online by
#	GRL  
#	https://github.com/GloriousRedLeader/uo-razor-enhanced
#	2024-03-26
# Use at your own risk. 

# This is the good stuff. This is a nice melee loop that will run in the background.
# Point your dex character at mobs and watch them die. Plenty of options for a lot of
# playstyles. Feel free to customize it even more. 
from Scripts.fm_core.core_attack import run_dex_loop

Player.HeadMessage( 78, 'STARTING DEX LOOP' )

run_dex_loop(
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
   
    # how many tiles to look for enemies and attack them
    attackRange = 6,
    
    # This will stop character from auto attacking if disabled.
    # Adding this while I level my vet skill so I dont kill things
    # too quickly.
    shouldAttack = True
)