# Razor Enhanced Scripts for Ultima Online by
#	GRL  
#	https://github.com/GloriousRedLeader/uo-razor-enhanced
#	2024-03-26
# Use at your own risk. 

from Scripts.fm_core.core_pets import run_vet_loop

# Put your serials here!
petSerials = [0x007B83C9, 0x007B8E89]

# Read up on the options avaialble in the run_vet_loop function.
run_vet_loop (
    petSerials,
    containerSerial = 0x4139FCCE,
    healthPercent = 95,
    bandageDelayMs = 1500,
    healSpellName = "Close Wounds"
)