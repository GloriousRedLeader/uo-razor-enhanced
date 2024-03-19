# Took some of this from Smaptastic from the UOAlive scripts channel on discord March 12th 2024.
# Not sure if he/she/they/them/thee/thy/thine has a github.
# I have made a few changes from original script. First, I removed 95% of the stuff
# and am just focusing on pet heals.
# 
# Known Issues: Most likely doesnt play nice with heal agent or other scripts that 
# block actions, e.g. "You must wait to do this". No idea how that stuff works.


Timer.Create("vet_bot_pet_warning", 1)

# Bandages the pet if youre close enough and its either poisoned or below the 
# specified health percentage.
def vetPet( healthPercent, petSerials, bandageContainerSerial, bandageDelayMs ):
    #global petID
    #global petSerial
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

    #if petID:
        #print("healthPercent {}".format(healthPercent))
        #print("healthPercent {}".format(healthPercent))
        if getHealthPercent(pet) < healthPercent or pet.Poisoned or pet.Hits == 0:
            #if runToPet and Player.DistanceTo(petID) > 2:
            #    pathFindToPet()
            if Player.DistanceTo(pet) <= 2 and not Player.BuffsExist('Veterinary'):
            
            
                if pet.Hits == 0:
                    Player.HeadMessage(48, "Rezzing {}".format(pet.Name))
                else:
                    Player.HeadMessage(48, "Bandaging {}".format(pet.Name))

                bandage = Items.FindByID(0x0E21, 0, bandageContainerSerial)
                #Items.UseItem(bandage, petSerial)
                Items.UseItem(bandage)
                Target.WaitForTarget(3000)
                Target.TargetExecute(pet)
                Misc.Pause(bandageDelayMs)
                
                #return True
        #return False
    #return False
    
    if Timer.Check("vet_bot_pet_warning") == False:
        if not atLeastOnePetFound:
            Player.HeadMessage(38, "Could not find any pets.")
        elif atLeastOnePetMissing:
            Player.HeadMessage(38, "At least one pet missing.")
        Timer.Create("vet_bot_pet_warning", 3000)

# Returns a current HP percentage value. Works for pets, but does quite a bit of rounding for them, as
# pet max HP is always considered to be 25, and they decrease as fractions of that. (i.e., 23/25 is 92%)
def getHealthPercent( mobForHP ):
    if mobForHP:
        if mobForHP.HitsMax <= 0:
            return 0
        healthPercent = 100 * mobForHP.Hits / mobForHP.HitsMax
        return healthPercent
    

def run_vet_bot(petSerials, bandageContainerSerial, healthPercent = 95, bandageDelayMs = 2000):
    Timer.Create("vet_bot_ping_delay", 1000)

    # This outer while just keeps the script running constantly. Its a wrapper to keep the script going but inactive when dead.
    while True:

        # This is the main loop.
        while not Player.IsGhost:
            
            if Timer.Check("vet_bot_ping_delay") == False:
                Player.HeadMessage(78, "Vetbot Running")
                Timer.Create("vet_bot_ping_delay", 3000)

            vetPet(healthPercent, petSerials, bandageContainerSerial, bandageDelayMs)
            Misc.Pause(500)
            continue

        # If you're a ghost, the script just pauses for a second then checks again on whether you're a ghost.
        Misc.Pause(1000)
        continue