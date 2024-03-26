# Razor Enhanced Scripts for Ultima Online by
#	GRL  
#	https://github.com/GloriousRedLeader/uo-razor-enhanced
#	2024-03-26
# Use at your own risk. 

# Took some of this from Smaptastic from the UOAlive scripts channel on discord March 12th 2024.
# Not sure if he/she/they/them/thee/thy/thine has a github.
# I have made a few changes from original script. First, I removed 95% of the stuff
# and am just focusing on pet heals.
# 
# Known Issues: Most likely doesnt play nice with heal agent or other scripts that 
# block actions, e.g. "You must wait to do this". No idea how that stuff works.

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

Timer.Create("vetLoopPetWarning", 1)

# Bandages the pet if youre close enough and its either poisoned or below the 
# specified health percentage.
# You should not use this method, instead use run_vet_bot() below which will
# loop and do all the good stuff.
def vet_pets( healthPercent, petSerials, containerSerial, bandageDelayMs, healSpellName = None ):

    atLeastOnePetFound = False
    atLeastOnePetMissing = False
    
    pets = []
    for petSerial in petSerials:
        pet = Mobiles.FindBySerial(petSerial)
        if pet == None:
            atLeastOnePetMissing = True
            continue
        atLeastOnePetFound = True
        pets.append(pet)
    pets.sort(key = lambda pet: pet.Hits)
    
    for pet in pets:

        petCurrentHealthPercent = getHealthPercent(pet)
        if petCurrentHealthPercent < healthPercent or pet.Poisoned or pet.Hits == 0:
            #if runToPet and Player.DistanceTo(petID) > 2:
            #    pathFindToPet()
            if Player.DistanceTo(pet) <= 2 and not Player.BuffsExist('Veterinary'):
                if pet.Hits == 0:
                    Player.HeadMessage(48, "Rezzing {}".format(pet.Name))
                else:
                    Player.HeadMessage(48, "Bandaging {}".format(pet.Name))

                bandage = Items.FindByID(0x0E21, 0, containerSerial)
                #Items.UseItem(bandage, petSerial)
                Items.UseItem(bandage)
                Target.WaitForTarget(3000)
                Target.TargetExecute(pet)
                Misc.Pause(bandageDelayMs)
                
        # Heal with spell
        if petCurrentHealthPercent < 50 and healSpellName != None and not pet.Poisoned and pet.Hits > 0:
            Spells.Cast(healSpellName)
            Target.WaitForTarget(3000)
            Target.TargetExecute(pet)
                
                
                #return True
        #return False
    #return False
    
    if Timer.Check("vetLoopPetWarning") == False:
        if not atLeastOnePetFound:
            Player.HeadMessage(38, "Could not find any pets.")
        elif atLeastOnePetMissing:
            Player.HeadMessage(38, "At least one pet missing.")
        Timer.Create("vetLoopPetWarning", 3000)

# Returns a current HP percentage value. Works for pets, but does quite a bit of rounding for them, as
# pet max HP is always considered to be 25, and they decrease as fractions of that. (i.e., 23/25 is 92%)
# This method was completely hijacked from Smaptastic. All credit to them.
def getHealthPercent(mobForHP):
    if mobForHP:
        if mobForHP.HitsMax <= 0:
            return 0
        healthPercent = 100 * mobForHP.Hits / mobForHP.HitsMax
        return healthPercent
        
# Will look through your bags, find a leash, and leash all the pets 
# around you.
def leash_pets (
    # An array of serials for your pets. You must provide this.
    # To get the serials you can use razor and press "Inspect Entities",
    # but really all of these programs have this feature and most clients
    # to too.
    petSerials = [],
    
    # Container where your bandages live. Defautls to player backpack.
    containerSerial = Player.Backpack.Serial):

    leash = Items.FindByID(0x1374, 0, containerSerial)
    if leash == None:
        Player.HeadMessage(38, "You do not have a leash in backpack.")
        return False
    
    atLeastOnePetFound = False
    atLeastOnePetMissing = False
    
    pets = []
    for petSerial in petSerials:
        pet = Mobiles.FindBySerial(petSerial)
        if pet == None:
            atLeastOnePetMissing = True
            continue
        atLeastOnePetFound = True
        pets.append(pet)
    
    for pet in pets:
        if Misc.ReadSharedValue("core_loops_enabled") != 1:
            Player.HeadMessage( 48, "Skipping pet {} because framework is paused".format(pet.Name))
            break
            
        if Player.DistanceTo(pet) <= 5:
            Items.UseItem(leash)
            Target.WaitForTarget(3000)
            Target.TargetExecute(pet)
            Misc.Pause(1000)
            
    if not atLeastOnePetFound:
        Player.HeadMessage(38, "Could not find any pets.")
    elif atLeastOnePetMissing:
        Player.HeadMessage(38, "At least one pet missing.")

# This is the public API you should use when running a pet heal bot
# in the background.
def run_vet_loop (
    
    # An array of serials for your pets. You must provide this.
    # To get the serials you can use razor and press "Inspect Entities",
    # but really all of these programs have this feature and most clients
    # to too.
    petSerials = [], 
    
    # Container where your bandages live. Defautls to player backpack.
    containerSerial = Player.Backpack, 
    
    # Only bandage things when their health is below this percent.
    healthPercent = 95, 
    
    # Wait this long in between bandage attempts. This is a dumb
    # program, it doesn't know when fingers slip, or even whether
    # fingers can slip bandaging an aneemal.
    bandageDelayMs = 2000,
    
    # Optionally provide a heal spell name if you really want to get serious
    # Currently will only use this if pet is < 50% health. Can have things like
    # "Greater Heal" or "Close Wounds".
    healSpellName = None):
        
    # This is just a head message to let us know the application is running.
    Timer.Create("vetLoopTimer", 1000)

    # Always enable on start
    Misc.SetSharedValue("core_loops_enabled", 1)
    
    while True:
        while not Player.IsGhost:
            
            if Misc.ReadSharedValue("core_loops_enabled") != 1:
                Misc.Pause(500)
                Player.HeadMessage( 48, 'Vet Loop Paused...' )
                Timer.Create( 'vetLoopTimer', 2000 )
                continue            
            
            if Timer.Check("vetLoopTimer") == False:
                Player.HeadMessage(78, "Vet Loop Running")
                Timer.Create("vetLoopTimer", 3000)

            vet_pets(healthPercent, petSerials, containerSerial, bandageDelayMs, healSpellName)
            Misc.Pause(500)
            continue

        # If youre a ghost, the script just pauses for a second then checks again on whether youre a ghost.
        Misc.Pause(1000)
        continue