# Heal Pet by Smaptastic
# Heals/cures your pet based on settings you define (use magery, use bandaids, etc)
# Loops automatically, so you can just leave it running in the background.
# Automatically detects your pet(s) (can handle multiple pets) and range checks them.
# Will not cast magery spells while you are running (assuming you hold RMB to run)
# May only work with Windows; I don't have the means of testing anything else.

from AutoComplete import *
from System import Byte
from System.Collections.Generic import List
import random
import ctypes
from ctypes import wintypes
user32 = ctypes.WinDLL('user32', use_last_error=True)
user32.GetAsyncKeyState.restype = wintypes.SHORT
user32.GetAsyncKeyState.argtypes = [wintypes.INT]

'''
****************************************************************************************************************************
CORE SETTINGS:

Edit the settings below prior to running. It is set up to be reasonably functional out of the box, but it is set up with
my personal settings. You may use different skills than me, so make sure to go through these.

****************************************************************************************************************************
'''
# Stash Gold? Uses Bag of Sending to stash gold when you're near your weight cap

stashGold = True

# Use Magery? This will cast Cure, Heal, and Greater Heal on yourself as appropriate.
# In emergencies, it will cast on your pet. This script assumes you have enough Magery skill to cast each.
useMagery = True
# !!! currently using an experimental timer to heal pet to near full if it hits 50%, instead of casting individual heals every time it hits 50% !!!

# Use Magery at high pet HP? This will use Magery even if your pet is at high HP. Useful if not using Vet or if you want to
# auto-cast Magery heals at your pet from a distance even if Vet is on.
useMageryHighHP = False 
# !!! currently using an experimental timer to heal pet to near full if it hits 50%, instead of casting individual heals every time it hits 50% !!!

# Use magery for healing and curing yourself? (Buff options are below - not impacted by this)
useMagerySelf = True

# Use Vet? This script is premised on using veterinary to heal your pet. It will also use Magery in emergencies.
useVet = False

# Bandage container. If you keep your bandages in your main backpack, don't change this. Default: Player.Backpack.Serial
# If you change it, put in the serial number of your bandage container.
bandageSerial = Player.Backpack

# Use Spellweaving?
useGiftRenewal = True  # On pet
useGiftLife = False    # On pet !!! NOT USED !!!
useGiftLifeSelf = True # On self...

# Kill Them With Magic? True/False? (Healing will be prioritized unless it has been disabled completely)
#useMageryKill = Misc.ReadSharedValue("useMageryKill") 
# !!! This is now off by default, toggled on by a separate script that can be triggered with a keybind !!!

'''
****************************************************************************************************************************
SPELL SETTINGS: 
****************************************************************************************************************************
'''

lmc = Player.LowerManaCost
fc = Player.FasterCasting
fc_offset = 250 * fc
latency = 350


# Gift of Life Calculations
cost = 70
reduction = cost * lmc / 100
actual = cost - reduction

delay = 4000 #enter the casting delay for the spell here (this is BADDDDD and i should make functions for these redundant calculations)
wait = delay + latency - fc_offset

# Arcane Empowerment Calculations

aeCost = 50
aeReduction = aeCost * lmc / 100
aeActual = aeCost - aeReduction

aeDelay = 2400
aeWait = aeDelay + latency - fc_offset

# Thunderstorm Calculations
tsCost = 32
tsReduction = tsCost * lmc / 100
tsActual = tsCost - tsReduction

tsDelay = 700
tsWait = tsDelay + latency - fc_offset

# Wildfire Calculations
wfCost = 50
wfReduction = wfCost * lmc / 100
wfActual = wfCost - wfReduction

wfDelay = 1800
wfWait = wfDelay + latency - fc_offset

# Word of Death Calculations

wdCost = 50
wdReduction = wdCost * lmc / 100
wdActual = wdCost - wdReduction

wdDelay = 3000
wdWait = wdDelay + latency - fc_offset




'''
****************************************************************************************************************************
KILL SETTINGS:
****************************************************************************************************************************
'''

# List of things you don't want to instruct your pet to attack. This does not guarantee they won't attack (due to guard aggro),
# But you won't TELL your pet to attack them at least.
# Also applies to Discord.
dontKillList = ['a dog', 'a cat', 'a sheep', 'a horse', 'a pack llama', 'a pack horse']
summonsToIgnore = ["a reaper", "a rising colossus", "a nature's fury", "a blade spirit"]
healersToIgnore = ["healer", "priest of mondain"]

# Set to True to disable "Attacking (Creature Name)" message every time you attack a new creature
reduceMessageSpam = False

# The max number of mobs you want to aggro at once (if you have aggroed more than this it will stop until some are dead/gone)
# Does not account for mobs that attack you while you already have others aggroed, so you might end up with more.
aggroCap = 10

# Attack while mounted? True/False.
mountedAttacks = False

# Kill unicorns? Included exclusively for unicorn farming.
killUnicorns = False
unicornList = ["a unicorn", "a ki-rin", "cu sidhe"]

# Strings to check to see if a mobile is someone else's pet.
mobileStrings = ["loyalty", "bonded"]

# Gather Mobs? True/False?
gatherMobs = False

'''
*******************************
END OF SETTINGS
*******************************
'''
def isMoving():
    return (user32.GetAsyncKeyState(0x02) & 0x8000 or # right mouse key
            user32.GetAsyncKeyState(0x57) & 0x8000 or  # W key
            user32.GetAsyncKeyState(0x41) & 0x8000 or  # A key
            user32.GetAsyncKeyState(0x53) & 0x8000 or  # S key
            user32.GetAsyncKeyState(0x44) & 0x8000)    # D key
    
def playerPercentHP():
    healthPercent = 100 * Player.Hits / Player.HitsMax
    return healthPercent

def getManaPercent():
    manaPercent = 100 * Player.Mana / Player.ManaMax
    return manaPercent

# Cures your pet using Magery using Arch Cure if its HP is less than the specified percentage.
# Won't activate if you currently have a bandage rolling on the pet.
def curePets(healthPercent):
    if isMoving() or not useMagery or Player.Mana < 15 or Timer.Check("spellTimer") or Player.BuffsExist("Veterinary"):
        return False
    global petIDs
    global petSerials
    rebuildPetList()
    if not petIDs:
        return False
    for i in petIDs:
        if Player.DistanceTo(i) > 10 or not i.Poisoned or (mobilePercentHP(i) >= healthPercent):
            return False
        castAtTarget("Arch Cure", 4, i.Serial, 1)
        return True
    return False

# Heals the pet using magery if it is below the specified health percentage. Requires useMagery to be true to have any effect.
def healPets(healthPercent):
    if isMoving() or Player.Mana < 15 or not useMagery or Timer.Check("spellTimer"):
        return False
    global petIDs
    global petSerials
    rebuildPetList()
    if not petIDs:
        return False
    for i in petIDs:
        if Player.DistanceTo(i) > 10 or i.IsGhost or i.Poisoned or (mobilePercentHP(i) >= healthPercent):
            return False
        if useGiftRenewal and not Timer.Check("Gift of Renewal"):
            spellWeavetAtTarget("Gift of Renewal", 4, i.Serial, -1)
            Timer.Create("Gift of Renewal", 150000)
            return True            
        castAtTarget("Greater Heal", 4, i.Serial, -1)
        return True
    return False

# Bandages the pet if you're close enough and it's either poisoned or below the specified health percentage.
def vetPets(healthPercent):
    if not useVet or Player.BuffsExist("Veterinary"):
        return False
    global petIDs
    global petSerials
    rebuildPetList()
    if not petIDs:
        return False
    for i in petIDs:
        if Player.DistanceTo(i) > 2:
            continue
        if (mobilePercentHP(i) >= healthPercent) and not i.Poisoned:
            continue
        bandage = Items.FindByID(0x0E21, 0, bandageSerial)
        Items.UseItem(bandage, i)
        Misc.Pause(250)
        return True
    return False

# Automatically calculates your faster casting by spell level, with some buffer built in (to accommodate lag)
def fcDelay(spellLevel):
    fc = int((((3 + spellLevel) / 4) * 1000) - (((Player.FasterCasting) * .25) * 1000) + 1500)
    if fc < 2000:
        fc = 2000
    return fc

# Automatically calculates your faster cast recovery, with some buffer built in (to accommodate lag)
def fcrDelay():
    fcr = int(((6 - Player.FasterCastRecovery) / 4) * 1000)
    if fcr < 1:
        fcr = 1
    return fcr

# Returns a current HP percentage value. Works for pets, but does quite a bit of rounding for them, as
# pet max HP is always considered to be 25, and they decrease as fractions of that. (i.e., 23/25 is 92%)
def mobilePercentHP(mobToCheck):
    healthPercent = 4 * mobToCheck.Hits
    return healthPercent
    
# Gets a list of non-human innocent mobiles for use in finding our pet.
def findInnocents():
    innocentListFilter = Mobiles.Filter()
    innocentListFilter.RangeMax = 15
    innocentListFilter.Notorieties = List[Byte](bytes([1, 2]))
    innocentListFilter.CheckIgnoreObject = True
    innocentListFilter.IsHuman = False
    innocentMobilesList = Mobiles.ApplyFilter(innocentListFilter)
    return innocentMobilesList

# This returns a list of innocents you can rename, which should be all of your pets.
# Does not detect pets outside of 15 blocks.    
def findMyPets():
    global petIDs
    global petSerials
    petIDs = []
    petSerials = []
    allPets = findInnocents()
    if not allPets:
        return False
    for i in allPets:
        if i.CanRename:
            petIDs.append(i)
    if not petIDs:
        return False
    for i in petIDs:
        petSerials.append(i.Serial)

# This rebuilds the petIDs list with the mobile info of each pet, from the initially-stored serials.
def rebuildPetList():
    global petSerials
    global petIDs
    petIDs = []
    if not petSerials:
        return False
    for i in petSerials:
        petToAdd = None
        petToAdd = Mobiles.FindBySerial(i)
        if petToAdd:
            petIDs.append(petToAdd)

# targetSerial can be ignored or sent as None for targetless spells.
# poisonCheck values: 1 (target must be poisoned; i.e., casting cure), -1 (target must not be poisoned; i.e., casting poison or heal)
# Omitting poisonCheck or setting to any other value ignores target poison state.
def castAtTarget(spellName, spellLevel, targetSerial=None, poisonCheck=0):
    Target.Cancel()
    Spells.CastMagery(spellName)
    Target.WaitForTarget(fcDelay(spellLevel))
    if not targetSerial:
        Timer.Create("spellTimer", fcrDelay())
        Target.Cancel()
        return True
    targetMobile = None
    targetMobile = Mobiles.FindBySerial(targetSerial)
    if not targetMobile:
        Target.Cancel()
        return False
    if Player.DistanceTo(targetMobile) > 10:
        Target.Cancel()
        return False
    if poisonCheck == 1 and not targetMobile.Poisoned:
        Target.Cancel()
        return False
    if poisonCheck == -1 and targetMobile.Poisoned:
        Target.Cancel()
        return False
    confirmTarget = None
    confirmTarget = Mobiles.FindBySerial(targetSerial)
    if not confirmTarget:
        Target.Cancel()
        return False
    if Target.HasTarget():
        Target.TargetExecute(targetSerial)
        Timer.Create("spellTimer", fcrDelay())
    Misc.Pause(250)
    Target.Cancel()
    return True
    
    # targetSerial can be ignored or sent as None for targetless spells.
# poisonCheck values: 1 (target must be poisoned; i.e., casting cure), -1 (target must not be poisoned; i.e., casting poison or heal)
# Omitting poisonCheck or setting to any other value ignores target poison state.
def spellWeavetAtTarget(spellName, spellLevel, targetSerial=None, poisonCheck=0):
    Target.Cancel()
    Spells.CastSpellweaving(spellName)
    Target.WaitForTarget(fcDelay(spellLevel))
    if not targetSerial:
        Timer.Create("spellTimer", fcrDelay())
        Target.Cancel()
        return True
    targetMobile = None
    targetMobile = Mobiles.FindBySerial(targetSerial)
    if not targetMobile:
        Target.Cancel()
        return False
    if Player.DistanceTo(targetMobile) > 10:
        Target.Cancel()
        return False
    if poisonCheck == 1 and not targetMobile.Poisoned:
        Target.Cancel()
        return False
    if poisonCheck == -1 and targetMobile.Poisoned:
        Target.Cancel()
        return False
    confirmTarget = None
    confirmTarget = Mobiles.FindBySerial(targetSerial)
    if not confirmTarget:
        Target.Cancel()
        return False
    if Target.HasTarget():
        Target.TargetExecute(targetSerial)
        Timer.Create("spellTimer", fcrDelay())
    Misc.Pause(250)
    Target.Cancel()
    return True
   
def healSelf( healthPercent ):
    if isMoving() or Player.Mana < 10 or not useMagerySelf or Timer.Check("spellTimer"):
        return False
    if playerPercentHP() < healthPercent and not Player.Poisoned:
        if Player.HitsMax - Player.Hits > 25 and Player.Mana > 15:
            Target.Cancel()
            Spells.CastMagery('Greater Heal')
            Target.WaitForTarget(fcDelay(4))
            if not Player.Poisoned:
                Target.TargetExecute(Player.Serial)
                Timer.Create("spellTimer", fcrDelay())
        elif Player.Mana > 10:
            Target.Cancel()
            Spells.CastMagery('Heal')
            Target.WaitForTarget(fcDelay(1), True)
            if not Player.Poisoned:
                Target.TargetExecute(Player.Serial)
                Timer.Create("spellTimer", fcrDelay())
        else:
            return False
        Target.Cancel()
        Misc.Pause(250)
        return True
    return False

def cureSelf():
    if isMoving() or Player.Mana < 15 or not useMagerySelf:
        return False
    if Player.Poisoned:
        Target.Cancel()
        Spells.CastMagery('Arch Cure')
        Target.WaitForTarget(fcDelay(4))
        if Player.Poisoned:
            Target.TargetExecute(Player.Serial)
            Timer.Create("spellTimer", fcrDelay())
        Target.Cancel()
        return True
    return False
    
def stashGold():
    if Player.MaxWeight - Player.Weight >= 20:
        return False
    bagItem = None
    goldStack = None
    bagItem = Items.FindByName("a bag of sending", -1, Player.Backpack.Serial, 2, True)
    goldStack = Items.FindByID(0x0EED, 0x0000, Player.Backpack.Serial, True, True)
    if not bagItem or not goldStack:
        return False
    Items.UseItem(bagItem.Serial)
    Target.WaitForTarget(2000)
    Target.TargetExecute(goldStack)
    Misc.Pause(200)
    return True

def usePriority():
    if useMagerySelf:
        if cureSelf():
            return True
        if healSelf(75):
            return True
    if vetPets(80):
        return True
    if curePets(50):
        return True
    if healPets(50):
        Timer.Create("recentlyInjured", 5000)
        return True
    if curePets(95):
        return True
    if useMageryHighHP or Timer.Check("recentlyInjured"):
        if healPets(80):
            return True
    if vetPets(90):
        return True
    return False
    
# Finds all enemies around. Can adjust range and whether you want to attack hostiles only or any gray, as well as range.
# Default settings are attack any gray, 10 range.
def findEnemies(hostilesOnly=True, innocentsIncluded=False, maxRange=10):
    enemyFilter = Mobiles.Filter()
    enemyFilter.RangeMax = maxRange
    if innocentsIncluded:
        enemyFilter.Notorieties = List[Byte](bytes([1, 2, 3, 4, 5, 6]))
    elif not hostilesOnly:
        enemyFilter.Notorieties = List[Byte](bytes([3, 4, 5, 6]))
    else:
        enemyFilter.Notorieties = List[Byte](bytes([4, 5, 6]))
    enemyFilter.IsGhost = False
    enemyFilter.Friend = False
    enemyFilter.CheckLineOfSight = True
    enemyFilter.CheckIgnoreObject = True
    enemyList = []
    enemyList = Mobiles.ApplyFilter(enemyFilter)
    if not enemyList:
        return False
    enemyListPython = [x for x in enemyList]
    return enemyListPython

# Removes stuff you don't want to kill from all potential enemies around and returns the result as a list.
# Can adjust range and whether you want to attack hostiles only or any gray, as well as range.
# Default settings are attack any gray, 10 range.
def findTargets(hostilesOnly=True, innocentsIncluded=False, maxRange=10):
    targetList = []
    targetList = findEnemies(hostilesOnly, innocentsIncluded, maxRange)
    if not targetList:
        return False
    targetListCopy = targetList[:]
    for enemy in targetListCopy:
        nextEnemy = False
        if enemy.CanRename:
            targetList.remove(enemy)
            continue
        enemyName = enemy.Name.lower()
        enemySerial = enemy.Serial
        if any(noKill in enemyName for noKill in dontKillLower) or any(noSummon in enemyName for noSummon in summonsLower):
            if enemy in targetList:
                targetList.remove(enemy)
            continue
        for healerName in healersLower:
            if any(healerName in noHealers.lower() for noHealers in Mobiles.GetPropStringList(enemySerial)):
                if enemy in targetList:
                    targetList.remove(enemy)
                nextEnemy = True
                break
        if nextEnemy:
            continue
        for mobileString in mobileStringsLower:
            if any(mobileString in petTest.lower() for petTest in Mobiles.GetPropStringList(enemySerial)):
                if enemy in targetList:
                    targetList.remove(enemy)
                break
    return targetList

# Parses the list of possible kill targets and selects the closest one. This will be what we tell the pet to kill.
def findKillSerial():
    global currentlyAttacking
    closestSerial = None
    if currentlyAttacking:
        # First, check to see if every mob in currentlyAttacking is alive and within range. If not, remove it from currentlyAttacking.
        # currentlyAttacking is a list of living mobs we have attacked already (thus drawing their aggro).
        # We max this list out at the aggroCap variable so we don't aggro everything on the screen.
        currentlyAttackingCopy = currentlyAttacking[:]
        for i in currentlyAttackingCopy:
            mobStatusCheck = None
            mobStatusCheck = Mobiles.FindBySerial(i)
            if not mobStatusCheck:
                currentlyAttacking.remove(i)
                continue
            if Player.DistanceTo(mobStatusCheck) > 12:
                currentlyAttacking.remove(i)

    # If we've aggroed less than the max living/nearby creatures, we find the nearest and that will be our target to return.
    # We don't return targets that are already on the list.
    # The target we return is added to the list.
    if len(currentlyAttacking) >= aggroCap:
        return False
    killList = []
    killList = findTargets(False, killUnicorns, 12)
    if not killList:
        return False
    
    # If we are killing unicorns, we just got a list with all the greens/blues. We're going to have to remove the non-unicorns.
    if killUnicorns:
        killListCopy = killList[:]
        for i in killListCopy:
            if i.Notoriety >= 3:
                continue
            if not any(unicornName in i.Name.lower() for unicornName in unicornListLower):
                killList.remove(i)
                continue

    # Now we start caring about mob distance to player, so we're going to sort killList by distance.
    killList.sort(key = lambda x: Player.DistanceTo(x))
    for i in killList:
        if not i.WarMode or i.Serial not in currentlyAttacking:
            closestSerial = i.Serial
            break
        continue
    if not closestSerial:
        return False
    if closestSerial not in currentlyAttacking:
        currentlyAttacking.append(closestSerial)
    return closestSerial

# This is the function that actually gets called. It finds a target and attacks it.
def petAttack():
    killSerial = None
    killSerial = findKillSerial()
    if not killSerial:
        return False
    killTarget = Mobiles.FindBySerial(killSerial)
    if not reduceMessageSpam:
        Player.HeadMessage(65, 'Attacking ' + killTarget.Name)
    Player.Attack(killSerial)
    Misc.Pause(250)
    return True

# This is the function that gets called to kill enemies with magic.
def playerAttack():
    killList = []
    killList = findEnemies()
    global currentlyAttacking
    if Player.Poisoned or isMoving() or Player.Mana < 15 or Timer.Check("spellTimer") or not killList:
        return False
    # Wildfire first
    if not Timer.Check("Wildfire") or not Items.FindAllByID(0x3996,0x0000,-1,12,) or not Items.FindAllByID(0x398C,0x0000,-1,12,):
        Target.Cancel( )        
        Spells.CastSpellweaving('Wildfire')
        Misc.Pause(wfWait)
        Target.WaitForTarget(fcDelay(2))
        Target.TargetExecuteRelative(Player.Serial, 0)
        Timer.Create("spellTimer", fcrDelay())
        Timer.Create("Wildfire", 9000)
        Misc.Pause(250)
        return True
    if Player.Mana < 50:
        return False
    else:
        # Arcane Empowerment
        if not Player.BuffsExist('Arcane Empowerment'):
            Spells.CastSpellweaving('Arcane Empowerment')
            Misc.Pause(aeWait)
            Misc.Pause(250)
            return True
        if not killList:
            return False
        if len(killList) > 2:
            Spells.CastSpellweaving('Thunderstorm')
            Misc.Pause(tsWait)
            Misc.Pause(150)
#        elif len(killList) == 1 and killList[0].Notoriety > 6:
#            Target.Cancel()
#            if mobilePercentHP(killList[0]) < 20:
#                Spells.CastSpellweaving('Word Of Death')
#                Target.WaitForTarget(fcDelay(2))
#                Misc.Pause(wdWait)            
#            targetMobile = None
#            targetMobile = Mobiles.FindBySerial(killList[0].Serial)
#            if not targetMobile:
#               Target.Cancel()
#                return False
#            if Player.DistanceTo(targetMobile) > 10:
#                Target.Cancel()
#                return False
#            confirmTarget = None
#            confirmTarget = Mobiles.FindBySerial(killList[0].Serial)
#            if not confirmTarget:
#                Target.Cancel()
#                return False
#            if Target.HasTarget():
#                Target.TargetExecute(killList[0].Serial)
#                Timer.Create("spellTimer", fcrDelay())            
#            Misc.Pause(250)
#            return True
    return True

# These just do some housekeeping for our lists. Sometimes IronPython/UO gets weird about capitalizations so we convert everything
# to lowercase to avoid errors.
currentlyAttacking = []
dontKillLower = [x.lower() for x in dontKillList]
summonsLower = [x.lower() for x in summonsToIgnore]
healersLower = [x.lower() for x in healersToIgnore]
unicornListLower = [x.lower() for x in unicornList]
mobileStringsLower = [x.lower() for x in mobileStrings]
    
petIDs = []
petSerials = []

# Start up by checking to see if we have pets.
findMyPets()
if petIDs:
    for i in petIDs:
        Player.HeadMessage(65, "Pet Located: " + i.Name)
else:
    Player.HeadMessage(1100, "No pets located, starting petless.")
Player.HeadMessage(65, "Heal Pets Ready!")

# This outer while just keeps the script running constantly. It's a wrapper to keep the script going but inactive when dead.
while True:
    while not Player.IsGhost and not isMoving():
        if stashGold:
            stashGold()
        useMageryKill = Misc.ReadSharedValue("useMageryKill")
        # This is the main loop. Checks to see if you or a pet currently needs heals. Always prioritizes self heals.
        rebuildPetList()
        if usePriority():
            rebuildPetList()
            continue
        # Buffs
        if useGiftLifeSelf and not Player.BuffsExist('Gift of Life') and Player.Visible and Player.Mana > actual:
            Spells.CastSpellweaving('Gift of Life')
            Target.WaitForTarget(5000,True)
            Target.Self()
            Misc.Pause(wait)
        # Kill Mobs
        if petIDs and useMageryKill and getManaPercent() > 25:
            playerAttack()
            Misc.Pause(250) 
            continue            
        
        # If you're not a ghost but don't have pets (ie, you're riding them), keeps checking for your pet to be back out.
        if not petIDs:
            findMyPets()
            if petIDs:
                for i in petIDs:
                    Player.HeadMessage(65, "Pet Located: " + i.Name)
            Misc.Pause(400)
        continue

    # If you're a ghost, the script just pauses for a second then checks again on whether you're a ghost.
    Misc.Pause(1000)
    continue