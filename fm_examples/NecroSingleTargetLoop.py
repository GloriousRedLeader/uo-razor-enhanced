from Scripts.fm_core.core_attack import run_mage_loop

Player.HeadMessage( 118, 'STARTING SINGLE MAGE LOOP' )

run_mage_loop(

    # How to pick your target for single target spells.
    # 0 = Nearest enemy. Default.
    # 1 = Prompt for target once at start of script. Useful for bosses.
    mobSelectMethod = 0,
    
    # Names of pets or blue characters you want to heal, cure if they are in range.
    # Note that you still need to enable useCure / useGreaterHeal etc.
    friendNames = [],
    
    # Buffer in MS between attacks, otherwise we get "You have not yet recovered"
    actionDelayMs = 1000,
    
    # Only look for mobs and pets/friends inside of this range. IF they are farther, then
    # dont heal them / dont attack them.
    range = 10,

    # Whether to use this spell 0 = disabled, 1 = enabled
    usePoisonStrike = 1,
    
    # Lower number like 10 means to spam repeatadly, number of MS in between usages
    poisonStrikeDelayMs = 10,
    
    # Whether to use this spell 0 = disabled, 1 = enabled
    useStrangle = 1,
    
    # Change to an appropriate value for strangle spell, number of MS in between usages
    strangleDelayMs = 30000,
    
    # Whether to use this spell 0 = disabled, 1 = enabled
    useCorpseSkin = 1,
    
    # Change to an appropriate value, number of MS in between usages
    corpseSkinDelayMs = 30000,
    
    # Whether to use this spell before applying each dot and curse 0 = disabled, 1 = enabled
    useEvilOmenBeforeDotsAndCurses = 1,
    
    # Whether to use this spell 0 = disabled, 1 = enabled
    useWildfire = 0,
    
    # Lower number like 10 means to spam repeatadly, number of MS in between usages
    wildfireDelayMs = 10000,
    
    # Whether to use this spell 0 = disabled, 1 = enabled
    useWither = 0,
    
    # Change to an appropriate value for strangle spell, number of MS in between usages
    witherDelayMs = 5000,
    
    # Whether to cure yourself or your pet
    useCure = 0,
    
    # Whether to heal yourself or your pet
    useGreaterHeal = 0,
    
    # Only heal things that are below this percent HP
    healThreshold = 0
)