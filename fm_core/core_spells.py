# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-03-26
# Use at your own risk. 

# This stuff is used to detect keypresses like mouse for movement
user32 = ctypes.WinDLL('user32', use_last_error=True)
user32.GetAsyncKeyState.restype = wintypes.SHORT
user32.GetAsyncKeyState.argtypes = [wintypes.INT]

# Got the delay values from ServUO Github

# Necro
WITHER_DELAY = 2250
POISON_STRIKE_DELAY = 2000
STRANGLE_DELAY = 2250
EVIL_OMEN_DELAY = 1000
CORPSE_SKIN_DELAY = 1750
CONDUIT_DELAY = 2250
CURSE_WEAPON_DELAY = 1000
SPIRIT_SPEAK_DELAY = 999

# Spellweaving
WILDFIRE_DELAY = 2500
THUNDERSTORM_DELAY = 1500
ARCANE_EMPOWERMENT_DELAY = 3000
GIFT_OF_RENEWAL_DELAY = 3000
WORD_OF_DEATH_DELAY = 3500

# Magery
GREATER_HEAL_DELAY = 1250
ARCH_CURE_DELAY = 1250
POISON_FIELD_DELAY = 1500
POISON_DELAY = 1000
DEATH_RAY_DELAY = 2250
CURSE_DELAY = 1250


# Chivalry
CONSECRATE_WEAPON_DELAY = 500
DIVINE_FURY_DELAY = 1000
CLOSE_WOUNDS_DELAY = 1500
ENEMY_OF_ONE_DELAY = 500
CLEANSE_BY_FIRE_DELAY = 1000
REMOVE_CURSE_DELAY = 1500

# Casts a spell. Blocks until spell is complete, or a small buffer has elapsed.
# It is possible the spell fizzled or there was some latency. 
# Some spells require a target.
# Considers faster casting and protection as best it can. 
# Also will pause for the correct amount of time for casting recovery so we can chain call this safely.
# Wont cast while moving.
def cast_spell(
    # Spell from Magery, Spellweaving, Necromancy, Chivalry
    spellName, 
    
    # Optional mobile target, otherwise spell specific logic
    target = None
):
    # Player is moving.
    if user32.GetAsyncKeyState(0x02) & 0x8000:
        return
        
    if Player.BuffsExist("Meditation"):
        return
    
    if spellName == "Wildfire":
        Spells.CastSpellweaving(spellName)
        Target.WaitForTarget(get_fc_delay(spellName, WILDFIRE_DELAY))
    elif spellName == "Thunderstorm":
        Spells.CastSpellweaving(spellName)
        Misc.Pause(get_fc_delay(spellName, THUNDERSTORM_DELAY)) 
    elif spellName == "Word of Death":
        Spells.CastSpellweaving(spellName)
        Target.WaitForTarget(get_fc_delay(spellName, WORD_OF_DEATH_DELAY))
    elif spellName == "Arcane Empowerment":
        Spells.CastSpellweaving(spellName)    
        Target.WaitForTarget(get_fc_delay(spellName, ARCANE_EMPOWERMENT_DELAY))
    elif spellName == "Wither":
        Spells.CastNecro(spellName)
        Misc.Pause(get_fc_delay(spellName, WITHER_DELAY)) 
    elif spellName == "Conduit":
        Spells.CastMastery(spellName)
        Target.WaitForTarget(get_fc_delay(spellName, CONDUIT_DELAY))
    elif spellName == "Corpse Skin":
        Spells.CastNecro(spellName)
        Target.WaitForTarget(get_fc_delay(spellName, CORPSE_SKIN_DELAY))
    elif spellName == "Evil Omen":
        Spells.CastNecro(spellName)
        Target.WaitForTarget(get_fc_delay(spellName, EVIL_OMEN_DELAY))
    elif spellName == "Strangle":
        Spells.CastNecro(spellName)
        Target.WaitForTarget(get_fc_delay(spellName, STRANGLE_DELAY))
    elif spellName == "Poison Strike":
        Spells.CastNecro(spellName)
        Target.WaitForTarget(get_fc_delay(spellName, POISON_STRIKE_DELAY))
    elif spellName == "Curse Weapon":
        Spells.CastNecro(spellName)
        Misc.Pause(get_fc_delay(spellName, CURSE_WEAPON_DELAY))        
    elif spellName == "Spirit Speak":
        Player.UseSkill("Spirit Speak")
        Misc.Pause(get_fc_delay(spellName, SPIRIT_SPEAK_DELAY))
    elif spellName == "Poison Field":
        Spells.CastMagery(spellName)
        Target.WaitForTarget(get_fc_delay(spellName, POISON_FIELD_DELAY))
    elif spellName == "Poison":
        Spells.CastMagery(spellName)
        Target.WaitForTarget(get_fc_delay(spellName, POISON_DELAY))
    elif spellName == "Death Ray":
        Spells.CastMastery(spellName)
        Target.WaitForTarget(get_fc_delay(spellName, DEATH_RAY_DELAY))
    elif spellName == "Curse":
        Spells.CastMagery(spellName)
        Target.WaitForTarget(get_fc_delay(spellName, CURSE_DELAY))
        Target.TargetExecute(target)
    elif spellName == "Arch Cure":
        Spells.CastMagery(spellName)
        Target.WaitForTarget(get_fc_delay(spellName, ARCH_CURE_DELAY))
    elif spellName == "Greater Heal":
        Spells.CastMagery(spellName)
        Target.WaitForTarget(get_fc_delay(spellName, GREATER_HEAL_DELAY))
    elif spellName == "Remove Curse":
        Spells.CastChivalry(spellName)
        Target.WaitForTarget(get_fc_delay(spellName, REMOVE_CURSE_DELAY))
    elif spellName == "Close Wounds":
        Spells.CastChivalry(spellName)
        Target.WaitForTarget(get_fc_delay(spellName, CLOSE_WOUNDS_DELAY))        
    elif spellName == "Divine Fury":
        Spells.CastChivalry(spellName)
        Misc.Pause(get_fc_delay(spellName, DIVINE_FURY_DELAY))            
    elif spellName == "Consecrate Weapon":
        Spells.CastChivalry(spellName)
        Misc.Pause(get_fc_delay(spellName, CONSECRATE_WEAPON_DELAY))            
    elif spellName == "Enemy of One":
        Spells.CastChivalry(spellName)
        Misc.Pause(get_fc_delay(spellName, ENEMY_OF_ONE_DELAY))            
    elif spellName == "Meditation":
        Player.HeadMessage(58, "Stand still - meditating!")
        Player.HeadMessage(38, "Stand still - meditating!")
        Player.UseSkill(spellName)

    if target is not None:
        Target.TargetExecute(target)
    
    Misc.Pause(get_fcr_delay())
    
# Considers FC jewelry and protection spell. Add a buffer for lag.
def get_fc_delay(
    # Spell from Magery, Spellweaving, Necromancy, Chivalry
    spellName,
    
    # Constants defined above for each spell
    baseDelayMs):
        
    return baseDelayMs + 250
    
# Completely stolen from Omniwraith and his lazy mage
def get_fcr_delay():
    fcr = int(((6 - Player.FasterCastRecovery) / 4) * 1000)
    if fcr < 1:
        fcr = 1
    return fcr    
    

# Make sure a spell gets cast
# DEPRECATED: Maybe dont use this. Ive got it baked into the recall
# function (fm_core.core_rails) which is the only place you really need it
# (maybe).
def cast_until_works(castFunc, delayBetweenAttemptsMs = 1000, maxAttempts = -1):
    while maxAttempts != 0:
        Journal.Clear()
        castFunc()
        Misc.Pause(1000)
        if (Journal.Search("You have not yet recovered") 
            or Journal.Search("You are already casting a spell") 
            or Journal.Search("This book needs time to recharge")
            or Journal.Search("That location is blocked")
            or Journal.Search("You must have at least")
        ):
            Misc.SendMessage("Waiting to retry")
            Misc.Pause(delayBetweenAttemptsMs)
            maxAttempts = maxAttempts - 1
        else:
            break
