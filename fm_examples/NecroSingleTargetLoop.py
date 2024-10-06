from Scripts.fm_core.core_attack import run_mage_single_target_loop

Player.HeadMessage( 118, 'STARTING POISON STRIKE SPAM LOOP SINGLE' )

run_mage_single_target_loop(

    actionDelayMs = 1000,
    
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
    
    # Whether to cure yourself or your pet
    useCure = 0,
    
    # Whether to heal yourself or your pet
    useGreaterHeal = 0
)