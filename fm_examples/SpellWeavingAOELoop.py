from Scripts.fm_core.core_attack import run_mage_aoe_loop

Player.HeadMessage( 118, 'STARTING MAGE AOE LOOP' )

run_mage_aoe_loop(

    # Buffer in MS between attacks, otherwise we get "You have not yet recovered"
    actionDelayMs = 1000,

    # Whether to use this spell 0 = disabled, 1 = enabled
    useWildfire = 1,
    
    # Lower number like 10 means to spam repeatadly, number of MS in between usages
    wildfireDelayMs = 10000,
    
    # Whether to use this spell 0 = disabled, 1 = enabled
    useWither = 0,
    
    # Change to an appropriate value for strangle spell, number of MS in between usages
    witherDelayMs = 5000,
    
    # Whether to cure yourself or your pet
    useCure = 1,
    
    # Whether to heal yourself or your pet
    useGreaterHeal = 1
)