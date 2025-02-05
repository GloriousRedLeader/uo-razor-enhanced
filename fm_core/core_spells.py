# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-03-26
# Use at your own risk. 

from Scripts.fm_core.core_mobiles import get_pets
import re

FC_CAP_MAGERY = 2
FC_CAP_NECROMANCY = 3 if (Player.GetSkillValue("Necromancy") == 120 and Player.GetSkillValue("Necromancy") == 120 and not any(Player.GetSkillValue(skill) > 30 for skill in ["Magery", "Spellweaving", "Parrying", "Mysticism", "Chivalry", "Animal Taming", "Animal Lore", "Ninjitsu", "Bushido", "Focus", "Imbuing", "Evaluating Intelligence"])) else 2
FC_CAP_CHIVALRY = 4
FC_CAP_SPELLWEAVING = 4
FC_CAP_SHIELD_BASH = 4

# Necro (taken from ServUO files)
CURSE_WEAPON_DELAY = 1000
EVIL_OMEN_DELAY = 1000
CORPSE_SKIN_DELAY = 1750
ANIMATE_DEAD_DELAY = 1750
POISON_STRIKE_DELAY = 2000
STRANGLE_DELAY = 2250
WITHER_DELAY = 2250
SUMMON_FAMILIAR_DELAY = 2250
WRAITH_FORM_DELAY = 2250

# Spellweaving (taken from ServUO files)
THUNDERSTORM_DELAY = 1500
WILDFIRE_DELAY = 2500
ARCANE_EMPOWERMENT_DELAY = 3000
GIFT_OF_RENEWAL_DELAY = 3000
WORD_OF_DEATH_DELAY = 3500

# Magery (these are all +500ms that are listed on the uo wiki)
POISON_DELAY = 1500
CURSE_DELAY = 1750
GREATER_HEAL_DELAY = 1750
ARCH_CURE_DELAY = 1750
POISON_FIELD_DELAY = 2000

# Chivalry (taken from ServUO files)
CONSECRATE_WEAPON_DELAY = 500
ENEMY_OF_ONE_DELAY = 500
DIVINE_FURY_DELAY = 1000
CLEANSE_BY_FIRE_DELAY = 1000
CLOSE_WOUNDS_DELAY = 1500
REMOVE_CURSE_DELAY = 1500

# Mastery (taken from ServUO files)
CONDUIT_DELAY = 2250
DEATH_RAY_DELAY = 2250
SHIELD_BASH_DELAY = 1000

# Skills
SPIRIT_SPEAK_DELAY = 999
MEDITATION_DELAY = 250

# Adds delay to skill usage so we can loop it
def use_skill(
    # Meditation, Spirit Speak, etc.
    skillName
):
    Player.UseSkill(skillName)
    
    if skillName == "Meditation":
        Misc.Pause(MEDITATION_DELAY)
    elif skillName == "Spirit Speak":
        Misc.Pause(SPIRIT_SPEAK_DELAY)
    else:
        Misc.Pause(1000)

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
    target = None,
    
    # Milliseonds of extra delay when computing cast time to account for internet fuzz. Fine tune this as needed.
    latencyMs = 200
):
    Target.Cancel()
    
    if spellName == "Wildfire":
        Spells.CastSpellweaving(spellName)
        Target.WaitForTarget(get_fc_delay(WILDFIRE_DELAY, FC_CAP_SPELLWEAVING, latencyMs))
    elif spellName == "Thunderstorm":
        Spells.CastSpellweaving(spellName)
        Misc.Pause(get_fc_delay(THUNDERSTORM_DELAY, FC_CAP_SPELLWEAVING, latencyMs)) 
    elif spellName == "Word of Death":
        Spells.CastSpellweaving(spellName)
        Target.WaitForTarget(get_fc_delay(WORD_OF_DEATH_DELAY, FC_CAP_SPELLWEAVING, latencyMs))
    elif spellName == "Arcane Empowerment":
        Spells.CastSpellweaving(spellName)    
        Target.WaitForTarget(get_fc_delay(ARCANE_EMPOWERMENT_DELAY, FC_CAP_SPELLWEAVING, latencyMs))
    elif spellName == "Wither":
        Spells.CastNecro(spellName)
        Misc.Pause(get_fc_delay(WITHER_DELAY, FC_CAP_NECROMANCY, latencyMs)) 
    elif spellName == "Conduit":
        Spells.CastMastery(spellName)
        Target.WaitForTarget(get_fc_delay(CONDUIT_DELAY, FC_CAP_NECROMANCY, latencyMs))
    elif spellName == "Corpse Skin":
        Spells.CastNecro(spellName)
        Target.WaitForTarget(get_fc_delay(CORPSE_SKIN_DELAY, FC_CAP_NECROMANCY, latencyMs))
    elif spellName == "Evil Omen":
        Spells.CastNecro(spellName)
        Target.WaitForTarget(get_fc_delay(EVIL_OMEN_DELAY, FC_CAP_NECROMANCY, latencyMs))
    elif spellName == "Strangle":
        Spells.CastNecro(spellName)
        Target.WaitForTarget(get_fc_delay(STRANGLE_DELAY, FC_CAP_NECROMANCY, latencyMs))
    elif spellName == "Poison Strike":
        Spells.CastNecro(spellName)
        Target.WaitForTarget(get_fc_delay(POISON_STRIKE_DELAY, FC_CAP_NECROMANCY, latencyMs))
    elif spellName == "Curse Weapon":
        Spells.CastNecro(spellName)
        Misc.Pause(get_fc_delay(CURSE_WEAPON_DELAY, FC_CAP_NECROMANCY, latencyMs))        
    elif spellName == "Animate Dead":
        Spells.CastNecro(spellName)
        Misc.Pause(get_fc_delay(ANIMATE_DEAD_DELAY, FC_CAP_NECROMANCY, latencyMs))        
    elif spellName == "Wraith Form":
        Spells.CastNecro(spellName)
        Misc.Pause(get_fc_delay(WRAITH_FORM_DELAY, FC_CAP_NECROMANCY, latencyMs))        
    #elif spellName == "Spirit Speak":
        #Player.UseSkill("Spirit Speak")
        #Misc.Pause(get_fc_delay(SPIRIT_SPEAK_DELAY))
    elif spellName == "Poison Field":
        Spells.CastMagery(spellName)
        Target.WaitForTarget(get_fc_delay(POISON_FIELD_DELAY, FC_CAP_MAGERY, latencyMs))
    elif spellName == "Poison":
        Spells.CastMagery(spellName)
        Target.WaitForTarget(get_fc_delay(POISON_DELAY, FC_CAP_MAGERY, latencyMs))
    elif spellName == "Death Ray":
        Spells.CastMastery(spellName)
        Target.WaitForTarget(get_fc_delay(DEATH_RAY_DELAY, FC_CAP_MAGERY, latencyMs))
    elif spellName == "Curse":
        Spells.CastMagery(spellName)
        Target.WaitForTarget(get_fc_delay(CURSE_DELAY, FC_CAP_MAGERY, latencyMs))
        Target.TargetExecute(target)
    elif spellName == "Arch Cure":
        Spells.CastMagery(spellName)
        Target.WaitForTarget(get_fc_delay(ARCH_CURE_DELAY, FC_CAP_MAGERY, latencyMs))
    elif spellName == "Greater Heal":
        Spells.CastMagery(spellName)
        Target.WaitForTarget(get_fc_delay(GREATER_HEAL_DELAY, FC_CAP_MAGERY, latencyMs))
    elif spellName == "Remove Curse":
        Spells.CastChivalry(spellName)
        Target.WaitForTarget(get_fc_delay(REMOVE_CURSE_DELAY, FC_CAP_CHIVALRY, latencyMs))
    elif spellName == "Close Wounds":
        Spells.CastChivalry(spellName)
        Target.WaitForTarget(get_fc_delay(CLOSE_WOUNDS_DELAY, FC_CAP_CHIVALRY, latencyMs))        
    elif spellName == "Divine Fury":
        Spells.CastChivalry(spellName)
        Misc.Pause(get_fc_delay(DIVINE_FURY_DELAY, FC_CAP_CHIVALRY, latencyMs))            
    elif spellName == "Consecrate Weapon":
        Spells.CastChivalry(spellName)
        Misc.Pause(get_fc_delay(CONSECRATE_WEAPON_DELAY, FC_CAP_CHIVALRY, latencyMs))            
    elif spellName == "Enemy of One":
        Spells.CastChivalry(spellName)
        Misc.Pause(get_fc_delay(ENEMY_OF_ONE_DELAY, FC_CAP_CHIVALRY, latencyMs))            
    #elif spellName == "Meditation":
    #    Player.UseSkill(spellName)
    elif spellName == "Shield Bash":
        Spells.CastMastery(spellName)
        Misc.Pause(get_fc_delay(SHIELD_BASH_DELAY, FC_CAP_SHIELD_BASH, latencyMs))            
    else:
        Player.HeadMessage(28, "That spell is not supported! Pausing.")
        Misc.Pause(1000)

    if target is not None:
        Target.TargetExecute(target)
    
    Misc.Pause(get_fcr_delay(spellName))


# Considers FC jewelry and protection spell. Add a buffer for lag.
def get_fc_delay (

    # Constants defined above for each spell
    baseDelayMs,
    
    # Each spell can have a different FC cap. Use constants above.
    fcCap,
    
    # Milliseonds of extra delay when computing cast time to account for internet fuzz. Fine tune this as needed.
    latencyMs = 200
):

    latency = 100
    fcOffset = 250 * (min(max(Player.FasterCasting - 2, 0), fcCap - 2) if Player.BuffsExist("Protection") else min(Player.FasterCasting, fcCap))
    delay = baseDelayMs - fcOffset
    if delay < 250:
        delay = 250
        
    delay = delay + latencyMs
    #print("fc", Player.FasterCasting, "fcCap", fcCap, "protection", Player.BuffsExist("Protection"), "baseDelayMs", baseDelayMs, "fcOffset", fcOffset, "delay", delay)        
    return delay
    
# Completely stolen from Omniwraith and his lazy mage
def get_fcr_delay(spellName):

    fcr = int(((6 - Player.FasterCastRecovery) / 4) * 1000)
        
    if fcr < 1:
        fcr = 1

    #print("FCR", "fcr", fcr)        
    return fcr    
    
# InsaneUO specific. Summons a single familiar. Will require multiple calls
# to summon all 4. 
Timer.Create("checkSummonFamiliarTimer", 1000)
def check_summon_familiar(

    # Milliseonds of extra delay when computing cast time to account for internet fuzz. Fine tune this as needed.
    latencyMs = 200
):
    SUMMON_FAMILIAR_GUMP_ID = 0x2082496e
    
    if Timer.Check("checkSummonFamiliarTimer") == False:
        if not Gumps.HasGump(SUMMON_FAMILIAR_GUMP_ID):
            Spells.CastNecro("Summon Familiar")
            Gumps.WaitForGump(SUMMON_FAMILIAR_GUMP_ID, 1000)

        if Gumps.HasGump(SUMMON_FAMILIAR_GUMP_ID):
            petButtonMap = {}
            data = Gumps.GetGumpData(SUMMON_FAMILIAR_GUMP_ID)
            for piece in data.layoutPieces:
                match = re.match(r"button (?:\d+\s)*(\d+)", piece)
                if match is not None:
                    buttonId = int(match.group(1))
                    #print("buttonId! ", buttonId, type(buttonId))
                    if buttonId in [2, 102]:
                        petButtonMap["Shadow Wisp"] = buttonId
                    elif buttonId in [3, 103]:
                        petButtonMap["Dark Wolf"] = buttonId
                    elif buttonId in [4, 104]:
                        petButtonMap["Death Adder"] = buttonId
                    elif buttonId in [5, 105]:
                        petButtonMap["Vampire Bat"] = buttonId

            pets = get_pets(range = 15, checkLineOfSight = False)
            petNames = [pet.Name.replace(Player.Name + " ", "") for pet in pets]    
            goodPetCount = 0
            for petName in petButtonMap:
                #print("{} -> {}".format(petName, petButtonMap[petName]))
                if petButtonMap[petName] < 6:
                    Gumps.SendAction(SUMMON_FAMILIAR_GUMP_ID, petButtonMap[petName])
                    Misc.Pause(get_fc_delay (baseDelayMs = SUMMON_FAMILIAR_DELAY, fcCap = FC_CAP_NECROMANCY, latencyMs = latencyMs))
                    Misc.Pause(250) # Extra pause for create to appear in world or we get stuck in an infinite loop
                    return True
                    #break
                elif petName not in petNames:
                    Gumps.SendAction(SUMMON_FAMILIAR_GUMP_ID, petButtonMap[petName])
                    Misc.Pause(250)    
                else:
                    goodPetCount = goodPetCount + 1
                    
                if goodPetCount == 4:
                    # We have all 4 pets and they are nearby. Dont call again
                    # for this many seconds
                    Timer.Create("checkSummonFamiliarTimer", 3000)
    return False

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

