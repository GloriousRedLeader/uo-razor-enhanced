# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-03-26
# Use at your own risk. 

FC_CAP_MAGERY = 2
FC_CAP_NECROMANCY = 3 if (Player.GetSkillValue("Necromancy") == 120 and Player.GetSkillValue("Necromancy") == 120 and not any(Player.GetSkillValue(skill) > 30 for skill in ["Magery", "Spellweaving", "Parrying", "Mysticism", "Chivalry", "Animal Taming", "Animal Lore", "Ninjitsu", "Bushido", "Focus", "Imbuing", "Evaluating Intelligence"])) else 2
FC_CAP_CHIVALRY = 4
FC_CAP_SPELLWEAVING = 4

# Got the delay values from ServUO Github

# Necro
CURSE_WEAPON_DELAY = 1000
EVIL_OMEN_DELAY = 1000
CORPSE_SKIN_DELAY = 1750
POISON_STRIKE_DELAY = 2000
STRANGLE_DELAY = 2250
WITHER_DELAY = 2250
CONDUIT_DELAY = 2250
SPIRIT_SPEAK_DELAY = 999

# Spellweaving
THUNDERSTORM_DELAY = 1500
WILDFIRE_DELAY = 2500
ARCANE_EMPOWERMENT_DELAY = 3000
GIFT_OF_RENEWAL_DELAY = 3000
WORD_OF_DEATH_DELAY = 3500

# Magery
POISON_DELAY = 1500
CURSE_DELAY = 1750
GREATER_HEAL_DELAY = 1750
ARCH_CURE_DELAY = 1750
POISON_FIELD_DELAY = 2000
DEATH_RAY_DELAY = 2250

# Chivalry
CONSECRATE_WEAPON_DELAY = 500
ENEMY_OF_ONE_DELAY = 500
DIVINE_FURY_DELAY = 1000
CLEANSE_BY_FIRE_DELAY = 1000
CLOSE_WOUNDS_DELAY = 1500
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
    Target.Cancel()
    
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
        Player.UseSkill(spellName)
    else:
        Player.HeadMessage(28, "That spell is not supported! Pausing.")
        Misc.Pause(1000)

    if target is not None:
        Target.TargetExecute(target)
    
    Misc.Pause(get_fcr_delay())
    
# Considers FC jewelry and protection spell. Add a buffer for lag.
def get_fc_delay(
    # Spell from Magery, Spellweaving, Necromancy, Chivalry
    spellName,
    
    # Constants defined above for each spell
    baseDelayMs):
        
    latency = 350

    if spellName in ["Wildfire", "Thunderstorm", "Arcane Empowerment", "Word of Death", "Gift of Renewal"]:
        fcOffset = 250 * (min(abs(Player.FasterCasting - 2), FC_CAP_SPELLWEAVING - 2) if Player.BuffsExist("Protection") else min(Player.FasterCasting, FC_CAP_SPELLWEAVING))    
    elif spellName in ["Arch Cure", "Greater Heal", "Poison", "Poison Field"]:
        fcOffset = 250 * (min(abs(Player.FasterCasting - 2), FC_CAP_MAGERY - 2) if Player.BuffsExist("Protection") else min(Player.FasterCasting, FC_CAP_MAGERY))
    elif spellName in ["Evil Omen", "Strangle", "Wither", "Poison Strike", "Corpse Skin"]:
        fcOffset = 250 * (min(abs(Player.FasterCasting - 2), FC_CAP_NECROMANCY - 2) if Player.BuffsExist("Protection") else min(Player.FasterCasting, FC_CAP_NECROMANCY))
    elif spellName in ["Consecrate Weapon", "Close Wounds", "Cleanse by Fire", "Enemy of One", "Divine Fury"]:
        fcOffset = 250 * (min(abs(Player.FasterCasting - 2), FC_CAP_CHIVALRY - 2) if Player.BuffsExist("Protection") else min(Player.FasterCasting, FC_CAP_CHIVALRY))
        
    
    if fcOffset is not None:
        print("spellName=", spellName, "fcOffset", fcOffset, "fc", (fcOffset / 250), "final fc delay", baseDelayMs + latency - fcOffset)
        return baseDelayMs + latency - fcOffset
        
    return baseDelayMs + latency
    
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
